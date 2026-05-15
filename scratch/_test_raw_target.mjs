
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
  process.stdout.write("KICK_DONE:" + (r === null ? "null" : "data") + "\n");
});

stdin.on("readable", () => {
  let chunk;
  while ((chunk = stdin.read()) !== null) {
    totalEvents++;
    const hex = Buffer.from(chunk, "utf8").toString("hex");
    
    if (chunk === "\x03") {
      process.stdout.write("EXIT:CtrlC\n");
      stdin.setRawMode(false);
      process.exit(0);
    }
    
    if (!rawActive && chunk !== "\r" && chunk !== "\n") {
      receivedBeforeEnter = true;
    }
    
    if (chunk === "\r" || chunk === "\n") {
      rawActive = true;
      process.stdout.write("FIRST_ENTER\n");
    }
    
    process.stdout.write("KEY:" + hex + "\n");
  }
});

setTimeout(() => {
  process.stdout.write(
    "RESULT:" + JSON.stringify({
      total: totalEvents,
      receivedBeforeEnter,
      rawActive
    }) + "\n"
  );
  stdin.setRawMode(false);
  process.exit(totalEvents > 0 ? 0 : 1);
}, 5000);
