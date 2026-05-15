const fs = require('fs');
const file = 'C:/Users/MC/AppData/Local/Volta/tools/image/packages/dirac-cli/node_modules/dirac-cli/dist/cli.mjs';
const code = fs.readFileSync(file, 'utf8');
const idx = code.indexOf('incrementalRendering');
if (idx > -1) {
  console.log(code.substring(idx - 100, idx + 100));
} else {
  console.log('Not found');
}
