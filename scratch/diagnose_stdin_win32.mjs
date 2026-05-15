/**
 * Minimal reproduction: test process.stdin.setRawMode + readable listener
 * on Windows to isolate whether the bug is at the Node.js/TTY level or
 * in Ink's integration layer.
 *
 * Usage: node --experimental-vm-modules scratch/diagnose_stdin_win32.mjs
 *        or just: node scratch/diagnose_stdin_win32.mjs
 *
 * Tests:
 *   A) setRawMode(true) + 'readable' event (what Ink does)
 *   B) setRawMode(true) + resume() + 'readable' event
 *   C) setRawMode(true) + 'data' event (flowing mode alternative)
 *
 * Press q to exit.
 */

import process from 'node:process';

const MODE = process.argv[2] || 'A'; // A, B, or C

if (!process.stdin.isTTY) {
  console.error('FATAL: stdin is not a TTY. This test must run in a real terminal.');
  process.exit(1);
}

const LABELS = {
  A: 'setRawMode + readable (Ink default)',
  B: 'setRawMode + resume + readable',
  C: 'setRawMode + data event (flowing mode)',
};

console.log('');
console.log(`=== TEST ${MODE}: ${LABELS[MODE]} ===`);
console.log('Press arrow keys, letters, etc. Press "q" to exit.');
console.log('');

let keyCount = 0;
const startTime = Date.now();

function logEvent(label, data) {
  keyCount++;
  const elapsed = Date.now() - startTime;
  const bytes = [];
  for (let i = 0; i < data.length; i++) {
    bytes.push(data.charCodeAt(i).toString(16).padStart(2, '0'));
  }
  console.log(`[${elapsed}ms] ${label}: "${data}" (hex: ${bytes.join(' ')})`);
  if (data === 'q' || data === '\x03') {
    console.log('\nExiting...');
    process.stdin.setRawMode(false);
    process.exit(0);
  }
}

function runTest() {
  process.stdin.setEncoding('utf8');
  process.stdin.setRawMode(true);

  if (MODE === 'A') {
    // Ink's approach: readable listener
    process.stdin.addListener('readable', () => {
      let chunk;
      while ((chunk = process.stdin.read()) !== null) {
        logEvent('readable', chunk);
      }
    });
  } else if (MODE === 'B') {
    // Readable + explicit resume
    process.stdin.resume();
    process.stdin.addListener('readable', () => {
      let chunk;
      while ((chunk = process.stdin.read()) !== null) {
        logEvent('readable', chunk);
      }
    });
  } else if (MODE === 'C') {
    // Data event (flowing mode)
    process.stdin.on('data', (chunk) => {
      logEvent('data', chunk);
    });
  }

  // Safety timeout
  setTimeout(() => {
    console.log('\n[30s timeout reached — if no output above, stdin input was completely dead]');
    process.stdin.setRawMode(false);
    process.exit(keyCount > 0 ? 0 : 1);
  }, 30_000);
}

runTest();
