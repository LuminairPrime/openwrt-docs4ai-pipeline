/**
 * Targeted diagnostic: Does setRawMode(true) need a "kick" read() before
 * arrow keys are delivered on this Windows setup?
 *
 * Theory: On Windows/ConPTY, SetConsoleMode might be deferred until the
 * first read operation. If so, arrow keys are dead until Enter triggers
 * the first read, which then activates raw mode properly.
 *
 * Run this in a REAL PowerShell/Windows Terminal window (not a pipe):
 *   node scratch/test_raw_mode_kick.mjs
 */
import process from "node:process";

const stdin = process.stdin;
const stdout = process.stdout;

// Clean up function
function cleanup() {
  stdin.setRawMode(false);
  stdout.write("\n\nTest complete.\n");
  process.exit(0);
}

// Safety timeout
setTimeout(() => {
  stdout.write("\n\n[TIMEOUT] No input received in 15 seconds.\n");
  cleanup();
}, 15000);

if (!stdin.isTTY) {
  console.log("FATAL: stdin is not a TTY. This test must run in a real terminal.");
  process.exit(1);
}

console.log("=== Raw Mode Kick Test ===");
console.log("isTTY:", stdin.isTTY);
console.log("has setRawMode:", typeof stdin.setRawMode === "function");
console.log("");

// PHASE 1: Just set raw mode, no read, and see if arrow keys arrive
console.log("Phase 1: Setting raw mode WITHOUT a kick read...");
stdin.setEncoding("utf8");
stdin.setRawMode(true);
stdin.ref();

let phase = 1;
let keyCount = 0;

stdin.on("readable", () => {
  let chunk;
  while ((chunk = stdin.read()) !== null) {
    keyCount++;
    const hex = Buffer.from(chunk, "utf8").toString("hex");
    const escaped = JSON.stringify(chunk);
    
    if (phase === 1) {
      console.log(`\n[Phase 1 - key #${keyCount}] chunk=${escaped} hex=${hex}`);
      if (chunk === "\r" || chunk === "\n") {
        console.log("  That was Enter. Now doing a READ KICK to flush any deferred mode change...");
        // PHASE 2: After first data arrives, read again to kick
        // And test if arrow keys now work
        phase = 2;
        keyCount = 0;
        console.log("\nPhase 2: Now try arrow keys again (raw mode should be active after read)");
        // Do an explicit read to ensure raw mode is applied
        const kick = stdin.read();
        console.log("  Kick read result:", kick === null ? "null (no data)" : JSON.stringify(kick));
      } else {
        console.log("  (Non-Enter key received in Phase 1 - raw mode IS working!)");
      }
    } else {
      console.log(`[Phase 2 - key #${keyCount}] chunk=${escaped} hex=${hex}`);
      if (chunk === "\x1b[A") console.log("  ^^^ UP ARROW WORKS!");
      if (chunk === "\x1b[B") console.log("  ^^^ DOWN ARROW WORKS!");
      if (chunk === "\x1b[C") console.log("  ^^^ RIGHT ARROW WORKS!");
      if (chunk === "\x1b[D") console.log("  ^^^ LEFT ARROW WORKS!");
      if (chunk === "\r" || chunk === "\n") console.log("  Enter pressed");
    }
    
    // Ctrl+C to exit
    if (chunk === "\x03") {
      console.log("\nCtrl+C - exiting.");
      cleanup();
    }
  }
});

console.log("Press arrow keys first, then Enter. If arrow keys don't show until after Enter,");
console.log("the theory is confirmed and the fix is a 'kick read' after setRawMode.\n");
