const { get_encoding } = require('tiktoken');
const fs = require('fs');
const enc = get_encoding('cl100k_base');
const input = JSON.parse(fs.readFileSync(0, 'utf8')); // {name: text}
const out = {};
for (const [k, v] of Object.entries(input)) out[k] = enc.encode(v).length;
enc.free();
process.stdout.write(JSON.stringify(out));
