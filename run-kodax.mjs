import { runKodaX } from './vendors/InfCodeX/dist/index.js';

async function main() {
  console.log("Starting KodaX...");
  try {
    const result = await runKodaX(
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
          onToolCall: (call) => console.log(`\n[Tool Call] ${call.name}(${JSON.stringify(call.input)})`),
          onToolResult: (res) => console.log(`\n[Tool Result] ${res.name} -> ${String(res.content).substring(0, 50)}...`),
          onComplete: () => console.log('\n[Complete]'),
          onError: (e) => console.error('\n[Error]', e),
        }
      },
      "There is a bug in .github/scripts/openwrt-docs4ai-05a-assemble-references.py resulting in 'TypeError: string indices must be integers, not str' around line 352: `filename = legacy_part_filename(module, int(part['part_number']))`. Please analyze and fix this issue."
    );
    console.log("Final message:", result.lastText);
  } catch (err) {
    console.error("Error:", err);
  }
}

main();
