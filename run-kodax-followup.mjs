import { runKodaX } from './vendors/InfCodeX/dist/index.js';
async function main() {
  await runKodaX(
    {
      provider: 'deepseek',
      model: 'deepseek-v4-pro',
      reasoningMode: 'auto',
      permissionMode: 'auto-in-project',
      context: { gitRoot: process.cwd(), executionCwd: process.cwd() },
      events: {
        onTextDelta: (text) => process.stdout.write(text),
        onThinkingDelta: (text) => process.stdout.write(text),
        onToolCall: (call) => console.log('\n[Tool Call] ' + call.name + '...'),
        onToolResult: (res) => console.log('\n[Tool Result] ' + res.name + ' -> Done'),
        onComplete: () => console.log('\n[Complete]'),
        onError: (e) => console.error('\n[Error]', e)
      }
    },
    process.env.KODAX_PROMPT
  );
}
main();
