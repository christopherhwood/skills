import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, writeFileSync, readFileSync, existsSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const script = fileURLToPath(new URL('../skills/technical-learning-profile/scripts/render-diagram.mjs', import.meta.url));
function run(input, output, ...args) {
  const browser = process.env.DIAGRAM_BROWSER ? ['--browser', process.env.DIAGRAM_BROWSER] : [];
  return spawnSync(process.execPath, [script, input, '--output', output, ...browser, ...args], { encoding: 'utf8' });
}

test('real rendering, invalid syntax, replacement protection, and spaces in paths', () => {
  const dir = mkdtempSync(join(tmpdir(), 'diagram test '));
  try {
    const input = join(dir, 'input diagram.mmd');
    const png = join(dir, 'output diagram.png');
    const svg = join(dir, 'output diagram.svg');
    const pdf = join(dir, 'output diagram.pdf');
    writeFileSync(input, 'flowchart LR\n  A[Request] --> B[Owner]\n  B --> C[(Saved state)]\n');
    let result = run(input, png);
    assert.equal(result.status, 0, result.stderr);
    assert.equal(JSON.parse(result.stdout).output, png);
    assert.equal(readFileSync(png).subarray(1, 4).toString(), 'PNG');
    result = run(input, svg);
    assert.equal(result.status, 0, result.stderr);
    assert.match(readFileSync(svg, 'utf8'), /<svg/);
    result = run(input, pdf);
    assert.equal(result.status, 0, result.stderr);
    assert.equal(readFileSync(pdf).subarray(0, 4).toString(), '%PDF');
    const original = readFileSync(png);
    assert.notEqual(run(input, png).status, 0);
    assert.deepEqual(readFileSync(png), original);
    writeFileSync(input, 'this is not mermaid !!!');
    assert.notEqual(run(input, png, '--force').status, 0);
    assert.deepEqual(readFileSync(png), original);
    assert.notEqual(run(input, join(dir, 'bad.png')).status, 0);
    assert.equal(existsSync(join(dir, 'bad.png')), false);
    writeFileSync(input, 'sequenceDiagram\n  Client->>Owner: Read\n  Owner-->>Client: Result\n');
    result = run(input, png, '--force');
    assert.equal(result.status, 0, result.stderr);
    assert.notDeepEqual(readFileSync(png), original);
    assert.notEqual(run(input, input, '--force').status, 0);
    assert.notEqual(run(input, join(dir, 'invalid.png'), '--size', 'abc').status, 0);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
