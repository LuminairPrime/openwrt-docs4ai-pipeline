/**
 * Minimal test: Does setEncoding trigger _read()?
 * (Tests the core assumption behind the fix)
 * 
 * Run: node scratch/test_setencoding_read.mjs
 */
import process from "node:process";

const stdin = process.stdin;

console.log("=== setEncoding _read() Test ===");

// Check initial state
const rs = stdin._readableState;
console.log(`BEFORE: reading=${rs?.reading}, length=${rs?.length}`);

// Call setEncoding - does NOT call read(0) first (unlike our previous diagnostic)
stdin.setEncoding('utf8');

console.log(`AFTER setEncoding: reading=${rs?.reading}, length=${rs?.length}`);

if (rs?.reading) {
  console.log("⚠️  FAIL: setEncoding triggered _read(). Fix assumption invalid.");
  console.log("    The read would be in line-buffered mode if setRawMode hasn't been called.");
} else {
  console.log("✅ PASS: setEncoding does NOT trigger _read(). Fix assumption correct.");
}

// Test 2: adding readable listener
stdin.addListener('readable', () => {});
console.log(`AFTER addListener: reading=${rs?.reading}, length=${rs?.length}`);
// Note: addListener schedules read on nextTick, so reading might still be false here

setTimeout(() => {
  console.log(`TIMEOUT: reading=${rs?.reading}, length=${rs?.length}`);
  stdin.removeAllListeners('readable');
  if (rs?.reading) {
    console.log("    read was triggered on nextTick as expected.");
  }
  process.exit(0);
}, 100);
