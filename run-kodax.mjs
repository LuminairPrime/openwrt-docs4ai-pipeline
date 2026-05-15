import { runKodaX } from './vendors/InfCodeX/dist/index.js';

async function main() {
  const prompt = `Bug Report: dirac CLI freezes on Windows until Enter is pressed
Symptoms
dirac auth (and likely any interactive dirac command) renders its Ink-based TUI correctly but accepts zero keyboard input until the user presses Enter. After Enter is pressed, arrow keys and all other keys start working normally. No other key — not arrows, not letters, not Escape — has any effect before that first Enter.
The prompt renders fine (box drawing, menu items, "How would you like to get started?" text), it just ignores all input until Enter flushes something.
This happens on all Node.js versions (tested 20, 22, 24) and regardless of how dirac is invoked (via Volta shim, via direct path to .cmd, via direct path to .ps1, via volta run --node XX).
Environment
- OS: Windows 11, native (not WSL)
- Shell: PowerShell (Windows Terminal)
- Node manager: Volta 2.0.2 (installed via winget install Volta.Volta)
- Node.js: 24.15.0 (installed via volta install node@24)
- dirac-cli: 0.3.41 (installed via volta install dirac-cli)
- Ink version: @jrichman/ink@7.0.0 (a fork, specified as "ink": "npm:@jrichman/ink@7.0.0" in dirac's cli/package.json)
Volta shims are at C:\\Users\\MC\\AppData\\Local\\Volta\\bin\\dirac.cmd. The installed package lives at C:\\Users\\MC\\AppData\\Local\\Volta\\tools\\image\\packages\\dirac-cli\\. Ink is externalized from the esbuild bundle (not inlined), so it's loaded at runtime from node_modules\\dirac-cli\\node_modules\\ink\\.
What we know about the architecture
1. esbuild externalizes ink — confirmed in vendors/dirac/cli/esbuild.mts line 272. The bundle (dist/cli.mjs) does NOT contain Ink's code. It imports it at runtime from node_modules.
2. Ink's useInput hook (node_modules/ink/build/hooks/use-input.js) gets setRawMode from StdinContext, which delegates to App.handleSetRawMode (node_modules/ink/build/components/App.js). That function does three things:
   - stdin.setEncoding('utf8')
   - stdin.setRawMode(true) (with a reference count)
   - stdin.addListener('readable', this.handleReadable) — this listener is what actually reads data from stdin and emits 'input' events
3. useInput calls setRawMode(true) inside a useEffect — which runs AFTER the first render, not synchronously. The handleReadable listener (which reads from stdin and dispatches to the input handler) is only added when this effect runs.
4. dirac's auth flow: cli/src/commands/auth.ts -> runInkApp() in cli/src/utils/ink.ts -> render() from Ink -> mounts the App component which provides StdinContext -> the auth view component uses useInput hook.
Attempted fixes (all failed)
Attempt 1: Early setRawMode(true) at top of bundle
Added if(process.stdin.isTTY&&typeof process.stdin.setRawMode==="function"){process.stdin.setRawMode(true);process.stdin.resume();} at the very top of dist/cli.mjs, before any imports. Result: No change. Likely because this only activates raw mode but doesn't add the readable listener — data arrives as escape sequences but nobody reads it.
Attempt 2: Early setRawMode(true) in runInkApp() (source-level)
Added the same 3 lines in cli/src/utils/ink.ts after import("ink") but before render(). Could not test from source because building requires proto generation (npm run protos) which needs dist-standalone/proto/descriptor_set.pb that doesn't exist. Installed bundle was not rebuilt.
Attempt 3: Change useEffect to useLayoutEffect in Ink's use-input.js
Modified node_modules/ink/build/hooks/use-input.js to use useLayoutEffect instead of useEffect for both the setRawMode call and the event listener attachment. Result: No change. This should have made the raw mode + readable listener setup synchronous, but the bug persists.
Key uncertainty
We do not know WHY input is completely dead until Enter. The theories we explored (deferred setRawMode, missing readable listener, useEffect vs useLayoutEffect) all proved insufficient. Something is fundamentally blocking stdin delivery until Enter flushes it, and none of our fixes addressed the actual cause.
Possible unexplored causes:
- Windows console mode interaction between Volta's process spawning and Node's stdin
- Ink's @jrichman/ink@7.0.0 fork may have different stdin handling than stock Ink
- Something in the Ink App component or render() initialization resets or ignores stdin state
- The parseKeypress module may require an initial Enter to synchronize
- A React rendering timing issue where the component tree isn't fully mounted when the first input arrives
Files of interest
- Installed bundle: C:\\Users\\MC\\AppData\\Local\\Volta\\tools\\image\\packages\\dirac-cli\\node_modules\\dirac-cli\\dist\\cli.mjs
- Ink use-input hook: C:\\Users\\MC\\AppData\\Local\\Volta\\tools\\image\\packages\\dirac-cli\\node_modules\\dirac-cli\\node_modules\\ink\\build\\hooks\\use-input.js
- Ink App component: C:\\Users\\MC\\AppData\\Local\\Volta\\tools\\image\\packages\\dirac-cli\\node_modules\\dirac-cli\\node_modules\\ink\\build\\components\\App.js
- Ink StdinContext: C:\\Users\\MC\\AppData\\Local\\Volta\\tools\\image\\packages\\dirac-cli\\node_modules\\dirac-cli\\node_modules\\ink\\build\\components\\StdinContext.js
- Ink render function: C:\\Users\\MC\\AppData\\Local\\Volta\\tools\\image\\packages\\dirac-cli\\node_modules\\dirac-cli\\node_modules\\ink\\build\\render.js
- dirac source repo: C:\\Users\\MC\\Documents\\AirSentinel\\openwrt-docs4ai-pipeline\\vendors\\dirac
- dirac CLI entry: vendors/dirac/cli/src/index.ts
- dirac auth command: vendors/dirac/cli/src/commands/auth.ts
- dirac runInkApp: vendors/dirac/cli/src/utils/ink.ts
- esbuild config (confirms ink externalized): vendors/dirac/cli/esbuild.mts line 272
- Volta shim: C:\\Users\\MC\\AppData\\Local\\Volta\\tools\\image\\packages\\dirac-cli\\dirac.cmd
Current state of modified files
The use-input.js in the installed Ink package currently has useLayoutEffect instead of useEffect (Attempt 3). The cli.mjs bundle is clean (Attempt 1 was reverted). The dirac source repo's cli/src/utils/ink.ts is clean (Attempt 2 was reverted). The dirac source repo's node_modules do not exist (never successfully installed with --ignore-scripts followed by proto generation).`;

  await runKodaX(
    {
      provider: 'deepseek',
      model: 'deepseek-v4-pro',
      reasoningMode: 'auto',
      permissionMode: 'auto-in-project',
      context: {
        gitRoot: process.cwd(),
        executionCwd: process.cwd(),
      },
      events: {
        onTextDelta: (text) => process.stdout.write(text),
        onThinkingDelta: (text) => process.stdout.write(text),
        onToolCall: (call) => console.log(`\n[Tool Call] ${call.name}(...)`),
        onToolResult: (res) => console.log(`\n[Tool Result] ${res.name} -> Done`),
        onComplete: () => console.log('\n[Complete]'),
        onError: (e) => console.error('\n[Error]', e),
      }
    },
    prompt
  );
}

main();