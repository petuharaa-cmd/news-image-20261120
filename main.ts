// Copies entry.png to the output directory.
// Runs twice; both runs must produce identical bytes.
import { copyFileSync } from 'node:fs';
import { join } from 'node:path';
const out = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(new URL('./entry.png', import.meta.url), join(out, 'entry.png'));
