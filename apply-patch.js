const fs = require('fs');
const file = 'C:/Users/MC/AppData/Local/Volta/tools/image/packages/dirac-cli/node_modules/dirac-cli/dist/cli.mjs';
let code = fs.readFileSync(file, 'utf8');

const original = 'let{waitUntilExit:a,unmount:o}=r(t,{exitOnCtrlC:!0,patchConsole:!1,synchronizedUpdateMode:!0,incrementalRendering:!0});try{await a()}finally{try{o()}catch{}i(),await e()}';

const patched = 'const wasRaw=process.stdin.isRaw;if(process.stdin.isTTY&&typeof process.stdin.setRawMode==="function"){process.stdin.setRawMode(true);process.stdin.resume();}let{waitUntilExit:a,unmount:o}=r(t,{exitOnCtrlC:!0,patchConsole:!1,synchronizedUpdateMode:!0,incrementalRendering:!0});try{await a()}finally{try{o()}catch{}if(process.stdin.isTTY&&typeof process.stdin.setRawMode==="function"){process.stdin.setRawMode(Boolean(wasRaw));process.stdin.pause();}i(),await e()}';

if (code.includes(original)) {
  code = code.replace(original, patched);
  fs.writeFileSync(file, code);
  console.log('Successfully patched cli.mjs!');
} else if (code.includes('process.stdin.resume()')) {
  console.log('Already patched!');
} else {
  console.log('Original string not found! Could not patch.');
}
