# How to Use InfCodeX (KodaX) for Bug Fixing

This guide explains how to leverage the **InfCodeX** (KodaX) execution-oriented AI agent to automatically analyze and fix bugs in this repository.

## 1. Installation & Build
InfCodeX is located in the `vendors/InfCodeX` directory. You must install its dependencies and build the TypeScript codebase before you can use the CLI.

```powershell
# Navigate to the vendor directory
cd vendors/InfCodeX

# Install dependencies and build the CLI
npm install
npm run build:packages
npm run build
```

## 2. Configuration & Permissions
To allow InfCodeX to automatically apply file edits (so you don't have to manually approve every change), configure its permission mode. 

Create or edit `~/.kodax/config.json` (e.g., `C:\Users\MC\.kodax\config.json`) with the following:
```json
{
  "permissionMode": "auto-in-project"
}
```

## 3. Environment Variables
You must set your LLM provider's API key before running the agent. For example, if you are using DeepSeek:
```powershell
$env:DEEPSEEK_API_KEY="sk-your-api-key-here"
```

## 4. Running KodaX to Fix a Bug

### Option A: Interactive REPL (Recommended)
You can start the interactive CLI to guide KodaX through the bug fix.

```powershell
# From the project root
node vendors/InfCodeX/dist/kodax_cli.js --provider deepseek --model deepseek-v4-pro
```
Inside the prompt, you can paste your stack trace:
```text
> There is a TypeError in .github/scripts/openwrt-docs4ai-05a-assemble-references.py at line 352. 
> Here is the stack trace: <paste error here>
> Please analyze the file, find the root cause, and fix it.
```

### Option B: One-Shot CLI Execution
If you want to feed it a prompt directly from the command line, do not use `-p` (print mode) if you want it to retain its standard execution loop. Just pass the prompt as the positional argument.

```powershell
# From the project root
node vendors/InfCodeX/dist/kodax_cli.js --provider deepseek --model deepseek-v4-pro "Please fix the TypeError 'string indices must be integers, not str' around line 352 in .github/scripts/openwrt-docs4ai-05a-assemble-references.py. Analyze the variables and apply the fix."
```

### Option C: Advanced Programmatic Execution (JS API)
If the CLI output buffering is tricky or you want to hook into the events programmatically, you can create a simple runner script in the workspace root:

```javascript
// run-kodax.mjs
import { runKodaX } from './vendors/InfCodeX/dist/index.js';

async function main() {
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
    "Paste your prompt and stack trace here."
  );
}

main();
```
Then run it:
```powershell
node run-kodax.mjs
```

## Useful Flags
- `--provider NAME`: Sets the LLM provider (e.g., `deepseek`, `anthropic`, `openai`).
- `--model NAME`: Overrides the model name for the provider.
- `--reasoning MODE`: Enforces a reasoning level (`off`, `auto`, `quick`, `balanced`, `deep`).
- `--session NAME`: Starts or continues a named session so the agent remembers previous steps.

## 5. Best Practices & Pro-Tips (From Real Debugging Sessions)

When using KodaX to solve complex architectural bugs, keep these lessons in mind:

### 1. Handling Large Bug Reports (Use Option C)
If your bug report contains stack traces, quotes, code snippets, or system logs, **do not try to format it as a CLI argument (Option B)**. Shell escaping (like PowerShell's backticks or bash quotes) will break the prompt or cause syntax errors. 
**Best Practice:** Always use **Option C (Advanced Programmatic Execution)**. Paste your raw, unedited bug report into a template literal (\ \) in un-kodax.mjs and execute the file.

### 2. Deep Architectural Bugs Require Time
KodaX is an execution-oriented agent. If given a complex issue (e.g., OS-level stream behavior, race conditions, framework render lifecycles), it will actively crawl your codebase, read node modules, write scratch files to test theories, and iterate. 
**Best Practice:** Let it run. A deep debugging session can easily take **10 to 20 minutes**. If you are orchestrating this via another script or CI pipeline, ensure you **disable or extend your timeouts** (e.g., set timeouts to 1 hour).

### 3. Tuning the easoningMode
The easoningMode parameter dictates how much time the agent spends thinking before it executes a tool.
*   **quick / alanced**: Use this for syntax errors, simple linting fixes, or localized logic bugs. It will jump straight into file editing.
*   **uto / deep**: Use this for cross-file architecture bugs, framework lifecycle issues, or platform-specific bugs (like Windows TUI freezes). It will force the agent to thoroughly trace the execution path before writing code.

### 4. Selecting Providers
Native API providers like nthropic, openai, and deepseek work best out of the box because they natively support the internal tool-calling loops KodaX requires. CLI bridge providers (like gemini-cli or codex-cli) may require additional local daemon environments to function properly.
