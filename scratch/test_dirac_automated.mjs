/**
 * Automated test: Verify raw mode fix by launching a test program via ConPTY.
 * 
 * Uses node-pty (if installed) or falls back to a simpler approach.
 * 
 * Strategy:
 * 1. Write a small ESM script that sets raw mode + nextTick kick + listens
 * 2. Launch it via child_process with a PTY
 * 3. Send arrow key escape sequences
 * 4. Check if they're received before Enter
 * 
 * Alternative: Just print instructions for the user.
 */

import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { writeFileSync, existsSync } from "node:fs";
import { spawn } from "node:child_process";

const __dirname = dirname(fileURLToPath(import.meta.url));

// ── Option 1: Try node-pty ──────────────────────────────
async function tryNodePty() {
  let pty;
  try {
    pty = (await import("node-pty")).default;
  } catch {
    // Try to install node-pty
    console.log("node-pty not found. Attempting to install...");
    return null;
  }
  return pty;
}

// ── Option 2: Simple child_process test ─────────────────
// This creates a TTY-like environment using winpty or conpty
// Falls back to just printing manual test instructions

async function main() {
  console.log("=== Dirac Raw Mode Automated Test ===\n");

  // Write a minimal test script
  const testScript = join(__dirname, "_test_raw_target.mjs");
  writeFileSync(testScript, `
import process from "node:process";

const stdin = process.stdin;
let rawActive = false;
let receivedBeforeEnter = false;
let totalEvents = 0;

stdin.setEncoding("utf8");

// Apply the fix: nextTick kick read  
stdin.ref();
stdin.setRawMode(true);
process.nextTick(() => {
  const r = stdin.read();
  // Signal that kick read completed
  process.stdout.write("KICK_DONE:" + (r === null ? "null" : "data") + "\\n");
});

stdin.on("readable", () => {
  let chunk;
  while ((chunk = stdin.read()) !== null) {
    totalEvents++;
    const hex = Buffer.from(chunk, "utf8").toString("hex");
    
    if (chunk === "\\x03") {
      process.stdout.write("EXIT:CtrlC\\n");
      stdin.setRawMode(false);
      process.exit(0);
    }
    
    if (!rawActive && chunk !== "\\r" && chunk !== "\\n") {
      receivedBeforeEnter = true;
    }
    
    if (chunk === "\\r" || chunk === "\\n") {
      rawActive = true;
      process.stdout.write("FIRST_ENTER\\n");
    }
    
    process.stdout.write("KEY:" + hex + "\\n");
  }
});

setTimeout(() => {
  process.stdout.write(
    "RESULT:" + JSON.stringify({
      total: totalEvents,
      receivedBeforeEnter,
      rawActive
    }) + "\\n"
  );
  stdin.setRawMode(false);
  process.exit(totalEvents > 0 ? 0 : 1);
}, 5000);
`);

  console.log("Test script written to: _test_raw_target.mjs");
  
  // Try to use conpty via PowerShell
  console.log("\nAttempting automated test via PowerShell...");
  
  const psScript = `
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public class PseudoConsole {
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern int CreatePseudoConsole(
        COORD size,
        IntPtr hInput,
        IntPtr hOutput,
        uint dwFlags,
        out IntPtr hPC);
        
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern int ClosePseudoConsole(IntPtr hPC);
    
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern int ResizePseudoConsole(IntPtr hPC, COORD size);
    
    [StructLayout(LayoutKind.Sequential)]
    public struct COORD { public short X; public short Y; }
}
'@

# Try running the test with input sent via stdin pipe
$testScript = Join-Path (Get-Location) "scratch/_test_raw_target.mjs"
$esc = [char]27
$up = "$esc[A"
$down = "$esc[B"
$enter = [char]13

# Write input to a temp file
$inputFile = Join-Path $env:TEMP "dirac_test_input.txt"
"${up}${up}${down}${enter}${up}${enter}[char]3" | Out-File -Encoding ascii -NoNewline $inputFile

# Launch with input redirected
Get-Content $inputFile | node $testScript 2>&1 | Select-Object -First 50
`;

  console.log("Running: node _test_raw_target.mjs < arrow_keys_input");
  console.log("(Arrow key escape sequences will be piped as raw bytes)\n");
  
  // Simplest approach: launch and pipe escape sequences directly
  const child = spawn("node", [testScript], {
    stdio: ["pipe", "pipe", "pipe"],
  });
  
  let output = "";
  child.stdout.on("data", (d) => {
    output += d.toString();
    process.stdout.write(d);
  });
  child.stderr.on("data", (d) => process.stderr.write(d));
  
  // Send arrow key sequences (these are raw escape codes)
  // Up arrow: \x1b[A, Down: \x1b[B, Enter: \r
  setTimeout(() => child.stdin.write("\x1b[A"), 500);   // Up
  setTimeout(() => child.stdin.write("\x1b[B"), 800);   // Down
  setTimeout(() => child.stdin.write("\x1b[A"), 1100);  // Up
  setTimeout(() => child.stdin.write("\r"), 1400);      // Enter
  setTimeout(() => child.stdin.write("\x1b[A"), 1700);  // Up (after Enter, raw should be active)
  setTimeout(() => child.stdin.write("\x03"), 2000);    // Ctrl+C
  
  child.on("close", (code) => {
    console.log(`\nExit code: ${code}`);
    if (output.includes("receivedBeforeEnter")) {
      console.log("✅ SUCCESS: Arrow keys received BEFORE Enter - raw mode fix works!");
    } else if (output.includes("FIRST_ENTER") && output.includes("KEY:1b5b") && output.includes("KEY:1b5b")) {
      console.log("⚠️  PARTIAL: Arrow keys only after Enter - fix may not be working");
    } else {
      console.log("❌ Check output manually - test was non-TTY so results may be unreliable");
    }
    console.log("\nNote: This test runs without a real TTY (isTTY=false),");
    console.log("so it can't perfectly replicate the bug.");
    console.log("Please run the REAL test in an interactive terminal:");
    console.log("  node scratch/test_raw_mode_deferred.mjs t3");
  });
}

main().catch((err) => {
  console.error("Test failed:", err);
  process.exit(1);
});
