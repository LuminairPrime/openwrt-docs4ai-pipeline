/**
 * Minimal test: Does setRawMode(true) actually work on this Windows setup?
 * Tests whether arrow keys are received immediately or only after Enter.
 */
import process from "node:process";
import readline from "node:readline";

const stdin = process.stdin;
const stdout = process.stdout;

console.log("=== Raw Mode Test ===");
console.log(`isTTY: ${stdin.isTTY}`);
console.log(`has setRawMode: ${typeof stdin.setRawMode === "function"}`);
console.log(`has setRawMode on stdin: ${stdin.setRawMode ? "yes" : "no"}`);

// Check if stdin is a TTY
if (!stdin.isTTY) {
  console.log("stdin is not a TTY — raw mode won't work. Exiting.");
  process.exit(1);
}

console.log("\nSwitching to raw mode...");
stdin.setEncoding("utf8");
stdin.setRawMode(true);
stdin.resume();

let keyCount = 0;

const onReadable = () => {
  let chunk;
  while ((chunk = stdin.read()) !== null) {
    keyCount++;
    const hex = Buffer.from(chunk, "utf8").toString("hex");
    const escaped = JSON.stringify(chunk);
    console.log(`[${keyCount}] chunk=${escaped} hex=${hex}`);
    
    // Check for Enter/Return
    if (chunk === "\r" || chunk === "\n") {
      console.log("  ^^^ that was Enter/Return");
    }
    
    // Check for arrow keys
    if (chunk === "\x1b[A") console.log("  ^^^ UP ARROW");
    if (chunk === "\x1b[B") console.log("  ^^^ DOWN ARROW");
    if (chunk === "\x1b[C") console.log("  ^^^ RIGHT ARROW");
    if (chunk === "\x1b[D") console.log("  ^^^ LEFT ARROW");
    
    // Ctrl+C to exit
    if (chunk === "\x03") {
      console.log("\nCtrl+C pressed. Exiting...");
      stdin.setRawMode(false);
      process.exit(0);
    }
  }
};

stdin.on("readable", onReadable);

console.log("Raw mode active. Press arrow keys, letters, Enter. Ctrl+C to exit.");
console.log("(If you don't see output for arrow keys until Enter, raw mode failed)\n");

// Also set a timeout as safety
setTimeout(() => {
  console.log("\n\n=== Timeout reached ===");
  console.log(`Total keys received: ${keyCount}`);
  if (keyCount === 0) {
    console.log("WARNING: No keys received at all! stdin is completely dead.");
  }
  stdin.setRawMode(false);
  process.exit(1);
}, 15000);
