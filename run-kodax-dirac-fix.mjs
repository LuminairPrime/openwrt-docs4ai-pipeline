import { runKodaX } from './vendors/InfCodeX/dist/index.js';

async function main() {
  console.log("Starting KodaX for dirac auth fix...");
  try {
    const result = await runKodaX(
      {
        provider: 'deepseek',
        model: 'deepseek-v4-pro',
        reasoningMode: 'auto',
        permissionMode: 'auto-in-project',
        context: {
          gitRoot: 'C:\\Users\\MC\\AppData\\Local\\Volta\\tools\\image\\packages\\dirac-cli',
          executionCwd: 'C:\\Users\\MC\\AppData\\Local\\Volta\\tools\\image\\packages\\dirac-cli',
        },
        events: {
          onTextDelta: (text) => process.stdout.write(text),
          onThinkingDelta: (text) => process.stdout.write(text),
          onToolCall: (call) => console.log(`\n[Tool Call] ${call.name}(${JSON.stringify(call.input)})`),
          onToolResult: (res) => console.log(`\n[Tool Result] ${res.name} -> ${String(res.content).substring(0, 200)}...`),
          onComplete: () => console.log('\n[Complete]'),
          onError: (e) => console.error('\n[Error]', e),
        }
      },
      `BUG: dirac auth freezes on Windows. Arrow keys don't work until Enter is pressed first.

TARGET FILE: node_modules/dirac-cli/dist/cli.mjs (minified bundle)

ROOT CAUSE: The app uses Ink (React for CLIs) for the interactive auth prompt. Ink calls process.stdin.setRawMode(true) asynchronously AFTER the first render frame. Until then, stdin is in cooked/line-buffered mode, so arrow key escape sequences (like \\x1B[A) are buffered as regular text and only delivered when Enter flushes the line.

KEY CODE IN THE BUNDLE:
- Raw mode check function: function LTh(){return!!(process.stdin.isTTY&&typeof process.stdin.setRawMode=="function")}
- The auth prompt renders: "How would you like to get started?" with menu items using Ink components
- Ink's useInput hook relies on setRawMode being active

FIX - Add these 3 lines immediately BEFORE the Ink render() call that mounts the auth prompt component (the one that shows "How would you like to get started?"):
  if(process.stdin.isTTY&&typeof process.stdin.setRawMode==="function"){process.stdin.setRawMode(true);process.stdin.resume();}

If readline is already imported in the bundle, also add:
  readline.emitKeypressEvents(process.stdin)

This ensures raw mode is active before any rendering, so arrow key escape sequences are delivered immediately instead of being line-buffered.

After editing, verify the file is valid JS by running: node --check "node_modules/dirac-cli/dist/cli.mjs"

IMPORTANT: Only modify the cli.mjs file. Do not modify any other files. The fix should be minimal - just the early stdin setup before render.`
    );
    console.log("\n\nFinal message:", result.lastText);
  } catch (err) {
    console.error("Error:", err);
  }
}

main();
