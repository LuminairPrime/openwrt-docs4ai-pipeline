/**
 * Diagnostic: Does setRawMode(true) need a deferred kick read?
 *
 * Tests THREE scenarios:
 *   T1: No kick read (baseline)
 *   T2: Immediate kick read (current App.js behavior)
 *   T3: nextTick kick read (proposed fix)
 *
 * Theory: On Windows/ConPTY, SetConsoleMode may return before the
 * pseudo-console driver applies the mode change. A synchronous
 * stdin.read() returns null (no data buffered), failing to trigger
 * the raw mode activation. A deferred read (nextTick) gives the
 * ConPTY a chance to apply the mode change first.
 *
 * Run: node scratch/test_raw_mode_deferred.mjs
 * MUST run in a real terminal (Windows Terminal, not piped).
 */
import process from "node:process";

const stdin = process.stdin;
const stdout = process.stdout;

// ── Test configuration ──────────────────────────────────
const TEST = process.argv[2] || "t3"; // t1=no kick, t2=immediate, t3=nextTick

if (!stdin.isTTY) {
  console.error("FATAL: stdin is not a TTY. Run this in a real terminal.");
  process.exit(1);
}

// ── Utility ─────────────────────────────────────────────
function hexOf(chunk) {
  return Buffer.from(chunk, "utf8").toString("hex");
}

function describe(chunk) {
  const name = {
    "\x1b[A": "UP", "\x1b[B": "DOWN",
    "\x1b[C": "RIGHT", "\x1b[D": "LEFT",
    "\r": "Enter(\\r)", "\n": "Enter(\\n)",
    "\x03": "Ctrl+C", "\x7f": "Backspace",
    "\t": "Tab", "\x1b": "Escape",
  }[chunk];
  return name ? `${JSON.stringify(chunk)} (${name})` : JSON.stringify(chunk);
}

// ── Cleanup ─────────────────────────────────────────────
let exited = false;
function cleanup(msg) {
  if (exited) return;
  exited = true;
  stdin.setRawMode(false);
  stdout.write(`\n${msg}\n`);
  process.exit(0);
}

// Safety timeout (15s)
setTimeout(() => cleanup("[TIMEOUT] No input received"), 15000);

// ── Test runner ─────────────────────────────────────────
const testLabels = { t1: "NO kick read", t2: "IMMEDIATE kick read", t3: "nextTick kick read" };
const testLabel = testLabels[TEST] || TEST;

stdout.write(`\n=== Raw Mode Deferred-Kick Test: ${testLabel} ===\n`);
stdout.write(`isTTY: ${stdin.isTTY}, platform: ${process.platform}\n\n`);

stdin.setEncoding("utf8");
stdin.setRawMode(true);
stdin.ref();

let rawActive = false;
let keyCount = 0;

stdin.on("readable", () => {
  let chunk;
  while ((chunk = stdin.read()) !== null) {
    if (chunk === "\x03") { cleanup("Ctrl+C - exiting."); return; }
    keyCount++;
    stdout.write(`[key #${keyCount}] ${describe(chunk)} hex=${hexOf(chunk)}\n`);

    if (!rawActive) {
      rawActive = true;
      if (chunk === "\r" || chunk === "\n") {
        stdout.write("  → First event was Enter. Raw mode likely was NOT active before this.\n");
        stdout.write("  → Arrow keys before Enter would have been lost.\n");
      } else {
        stdout.write("  → First event was NOT Enter. Raw mode IS working immediately!\n");
      }
    }
  }
});

// ── Apply kick (or not) ─────────────────────────────────
if (TEST === "t2") {
  stdout.write("Doing IMMEDIATE kick read...\n");
  const result = stdin.read();
  stdout.write(`  → result: ${result === null ? "null (no data)" : JSON.stringify(result)}\n`);
}

if (TEST === "t3") {
  stdout.write("Scheduling nextTick kick read...\n");
  process.nextTick(() => {
    const result = stdin.read();
    stdout.write(`  → [nextTick] kick read result: ${result === null ? "null (no data)" : JSON.stringify(result)}\n`);
  });
}

if (TEST === "t1") {
  stdout.write("NO kick read (baseline).\n");
}

stdout.write("\nInstructions:\n");
stdout.write("  1. Press UP arrow a few times\n");
stdout.write("  2. Press Enter\n");
stdout.write("  3. Press UP arrow again\n");
stdout.write("  4. Press Ctrl+C to exit\n");
stdout.write("\nIf you see UP arrows ONLY after Enter → raw mode is deferred (BUG)\n");
stdout.write("If you see UP arrows immediately → raw mode works fine\n\n");
