/**
 * NON-INTERACTIVE diagnostic: Test whether stdin stream state prevents
 * setRawMode from taking effect on Windows/ConPTY.
 * 
 * This checks:
 * 1. Is stdin already reading before we touch it?
 * 2. Does pausing before setRawMode help?
 * 3. Does the stream need a fresh readStart?
 * 
 * Run: node scratch/diagnose_stdin_stream.mjs
 * (Can run piped — it checks internal stream state)
 */
import process from "node:process";
import { Readable } from "node:stream";

const stdin = process.stdin;

console.log("=== Stdin Stream State Diagnostic ===");
console.log(`Platform: ${process.platform}`);
console.log(`isTTY: ${stdin.isTTY}`);
console.log(`isPaused(): ${stdin.isPaused()}`);
console.log(`readableFlowing: ${stdin.readableFlowing}`);
console.log(`readableLength: ${stdin.readableLength}`);
console.log(`readableEnded: ${stdin.readableEnded}`);
console.log(`destroyed: ${stdin.destroyed}`);
console.log(`errored: ${stdin.errored}`);

// Check if readable state is available
const rs = stdin._readableState;
if (rs) {
  console.log(`\n--- ReadableState internals ---`);
  console.log(`flowing: ${rs.flowing}`);
  console.log(`paused: ${rs.paused}`);
  console.log(`reading: ${rs.reading}`);
  console.log(`sync: ${rs.sync}`);
  console.log(`needReadable: ${rs.needReadable}`);
  console.log(`emittedReadable: ${rs.emittedReadable}`);
  console.log(`readableListening: ${rs.readableListening}`);
  console.log(`resumeScheduled: ${rs.resumeScheduled}`);
  console.log(`length: ${rs.length}`);
  console.log(`pipesCount: ${rs.pipesCount}`);
  console.log(`flowing: ${rs.flowing}`);
  console.log(`ended: ${rs.ended}`);
  console.log(`endEmitted: ${rs.endEmitted}`);
  console.log(`readingMore: ${rs.readingMore}`);
  console.log(`highWaterMark: ${rs.highWaterMark}`);
  console.log(`constructed: ${rs.constructed}`);
  console.log(`decoder: ${rs.decoder ? rs.decoder.encoding : 'none'}`);
  console.log(`encoding: ${rs.encoding}`);
}

// Check if there's a pending read
console.log(`\n--- Pending Read Test ---`);
console.log(`Calling stdin.read(0)...`);
const r0 = stdin.read(0);
console.log(`read(0) result: ${r0 === null ? 'null' : JSON.stringify(String(r0))}`);

// Test: does a fresh read trigger anything?
try {
  stdin.setEncoding('utf8');
  console.log(`setEncoding('utf8') succeeded`);
} catch(e) {
  console.log(`setEncoding failed: ${e.message}`);
}

console.log(`\n--- Post-setEncoding State ---`);
console.log(`isPaused(): ${stdin.isPaused()}`);
console.log(`readableLength: ${stdin.readableLength}`);
if (rs) console.log(`reading: ${rs.reading}, length: ${rs.length}`);

// Try pause + resume pattern
console.log(`\n--- Pause/Resume Test ---`);
stdin.pause();
console.log(`After pause - isPaused(): ${stdin.isPaused()}`);

if (stdin.isTTY && typeof stdin.setRawMode === 'function') {
  stdin.setRawMode(true);
  console.log(`setRawMode(true) succeeded`);
  
  stdin.resume();
  stdin.ref();
  console.log(`After resume - isPaused(): ${stdin.isPaused()}`);
  if (rs) console.log(`After resume - reading: ${rs.reading}, flowing: ${rs.flowing}`);
  
  // Force a read
  const kick = stdin.read();
  console.log(`Kick read result: ${kick === null ? 'null' : JSON.stringify(String(kick))}`);
  
  // Reset
  stdin.setRawMode(false);
}

console.log(`\n=== Done ===`);
console.log(`If the stream is 'reading' before setRawMode, that's the root cause.`);
console.log(`Expected fix: stdin.pause() BEFORE setRawMode(true), then resume() after.`);
