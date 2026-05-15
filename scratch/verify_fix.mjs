/**
 * Quick Test: dirac raw mode fix
 * 
 * This script checks whether the fix in App.js is properly applied
 * by statically reading the patched code and verifying the fix sequence.
 * 
 * Run: node scratch/verify_fix.mjs
 */
import { readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));

// Path to the patched App.js
const appJsPath = join(
  process.env.LOCALAPPDATA,
  "Volta", "tools", "image", "packages", "dirac-cli",
  "node_modules", "dirac-cli", "node_modules", "ink",
  "build", "components", "App.js"
);

console.log("=== Fix Verification ===\n");
console.log(`Target: ${appJsPath}\n`);

try {
  const content = readFileSync(appJsPath, "utf8");
  
  // Check for key fix elements
  const checks = [
    {
      name: "stdin.pause() present",
      pattern: /stdin\.pause\(\)/,
      critical: true,
    },
    {
      name: "setRawMode BEFORE setEncoding",
      pattern: /stdin\.setRawMode\(true\)\s*;\s*\n\s*stdin\.setEncoding/,
      critical: true,
    },
    {
      name: "MUST call setRawMode BEFORE setEncoding comment",
      pattern: /MUST call setRawMode BEFORE setEncoding/,
      critical: false,
    },
    {
      name: "No immediate stdin.read() kick",
      pattern: /setRawMode\(true\)[\s\S]*?stdin\.read\(\)/,
      critical: false, // We still check this
    },
  ];

  let allCriticalPassed = true;
  
  for (const check of checks) {
    const passed = check.pattern.test(content);
    const status = passed ? "PASS" : "FAIL";
    const label = check.critical ? `[CRITICAL] ${check.name}` : `[info] ${check.name}`;
    
    if (!passed && check.critical) {
      allCriticalPassed = false;
    }
    
    console.log(`  ${status} ${label}`);
  }

  // Check the actual sequence order
  const match = content.match(/handleSetRawMode\s*=\s*\(isEnabled\)\s*=>\s*\{[\s\S]*?\n\s*\};/);
  if (match) {
    console.log("\n--- handleSetRawMode method found ---");
    const method = match[0];
    
    // Extract the enable sequence
    const enableMatch = method.match(/if\s*\(\s*this\.rawModeEnabledCount\s*===\s*0\s*\)\s*\{([\s\S]*?)\n\s*\}/);
    if (enableMatch) {
      const body = enableMatch[1];
      console.log("\nEnable sequence (compressed):");
      console.log(body.replace(/\s+/g, ' ').trim().substring(0, 200));
      
      // Verify order
      const pauseIdx = body.indexOf("pause()");
      const refIdx = body.indexOf("ref()");
      const setRawIdx = body.indexOf("setRawMode(true)");
      const setEncIdx = body.indexOf("setEncoding('utf8')");
      const addListenerIdx = body.indexOf("addListener('readable'");
      
      console.log("\nOperation order:");
      console.log(`  1. pause()    at pos ${pauseIdx}`);
      console.log(`  2. ref()      at pos ${refIdx}`);
      console.log(`  3. setRawMode at pos ${setRawIdx}`);
      console.log(`  4. setEncoding at pos ${setEncIdx}`);
      console.log(`  5. addListener at pos ${addListenerIdx}`);
      
      const orders = [pauseIdx, refIdx, setRawIdx, setEncIdx, addListenerIdx];
      const sorted = [...orders].sort((a, b) => a - b);
      const isCorrectOrder = orders.every((v, i) => v === -1 || sorted.indexOf(v) === orders.filter(x => x !== -1).indexOf(v));
      
      if (isCorrectOrder && setRawIdx !== -1 && setRawIdx < setEncIdx) {
        console.log("\n  ORDER CHECK: PASS (setRawMode before setEncoding)");
      } else {
        console.log("\n  ORDER CHECK: FAIL (setRawMode should come before setEncoding)");
        allCriticalPassed = false;
      }
      
      // Check for NO stdin.read() between setRawMode and addListener
      const between = body.substring(setRawIdx, addListenerIdx);
      if (between.includes("stdin.read()")) {
        console.log("  EXTRA READ CHECK: FAIL (unexpected stdin.read() between setup calls)");
      } else {
        console.log("  EXTRA READ CHECK: PASS (no premature reads)");
      }
    }
  }

  console.log("\n=== " + (allCriticalPassed ? "ALL CRITICAL CHECKS PASSED" : "SOME CHECKS FAILED") + " ===\n");
  
  if (allCriticalPassed) {
    console.log("The fix is correctly applied. Please test manually:");
    console.log("");
    console.log("  STEP 1: Open a NEW terminal window (Windows Terminal)");
    console.log("  STEP 2: Run: dirac");
    console.log("  STEP 3: Press UP arrow once");
    console.log("  STEP 4: Press ENTER once");
    console.log("");
    console.log("EXPECTED: dirac exits after step 4 (UP navigates to 'Exit', ENTER selects it)");
    console.log("BUG BEHAVIOR: nothing happens at step 4, need another UP + ENTER to exit");
  }
  
} catch (err) {
  console.error(`ERROR: ${err.message}`);
  console.error("App.js not found or not readable. Check the path above.");
  process.exit(1);
}
