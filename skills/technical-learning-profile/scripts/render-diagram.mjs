#!/usr/bin/env node
/** Render reviewed Mermaid source without shell interpolation or runtime installs. */
import { spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, realpathSync, rmSync, statSync, writeFileSync, copyFileSync, constants, renameSync } from 'node:fs';
import { dirname, extname, resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const skill = resolve(dirname(fileURLToPath(import.meta.url)), '..');
let staging;
try {
  const argv = process.argv.slice(2);
  if (argv.includes('--help')) {
    console.log('render-diagram.mjs INPUT --output OUTPUT.{png,svg,pdf} [--size 1200] [--scale 2] [--browser PATH] [--force]');
    process.exit(0);
  }
  const inputArg = argv.shift();
  if (!inputArg || inputArg.startsWith('--')) throw new Error('Provide an input Mermaid file. Use --help for usage.');
  const opts = { size: '1200', scale: '2', force: false };
  for (let i = 0; i < argv.length; i++) {
    const key = argv[i];
    if (key === '--force') { opts.force = true; continue; }
    if (!['--output', '--size', '--scale', '--browser'].includes(key)) throw new Error(`Unknown option: ${key}`);
    const value = argv[++i];
    if (!value || value.startsWith('--')) throw new Error(`Missing value for ${key}`);
    opts[key.slice(2)] = value;
  }
  if (!opts.output) throw new Error('--output is required');
  const input = realpathSync(resolve(inputArg));
  const output = resolve(opts.output);
  const format = extname(output).slice(1).toLowerCase();
  if (!['png', 'svg', 'pdf'].includes(format)) throw new Error('Output must be PNG, SVG, or PDF');
  if (input === output || (existsSync(output) && realpathSync(output) === input)) throw new Error('Input and output must differ');
  if (existsSync(output) && !opts.force) throw new Error('Output exists; use --force to replace it');
  if (!readFileSync(input, 'utf8').trim()) throw new Error('Input is empty');
  for (const [key, min, max] of [['size', 400, 4000], ['scale', 1, 4]]) {
    const value = Number(opts[key]);
    if (!Number.isInteger(value) || value < min || value > max) throw new Error(`${key} must be an integer from ${min} to ${max}`);
  }
  const cli = join(skill, 'node_modules/@mermaid-js/mermaid-cli/src/cli.js');
  if (!existsSync(cli)) throw new Error(`Install dependencies first: npm ci --prefix "${skill}"`);
  mkdirSync(dirname(output), { recursive: true });
  staging = mkdtempSync(join(dirname(output), '.diagram-'));
  const rendered = join(staging, `rendered.${format}`);
  const config = join(staging, 'mermaid.json');
  writeFileSync(config, JSON.stringify({
    theme: 'base', securityLevel: 'strict', fontFamily: 'Arial, sans-serif',
    themeVariables: { primaryColor: '#e8f0fe', primaryTextColor: '#172b4d', primaryBorderColor: '#476582', lineColor: '#476582', fontSize: '18px' },
    flowchart: { useMaxWidth: false, htmlLabels: false, curve: 'linear' }
  }));
  const args = [cli, '-i', input, '-o', rendered, '-c', config, '-b', 'white', '--size', opts.size, '-s', opts.scale];
  if (opts.browser) {
    const browser = realpathSync(resolve(opts.browser));
    const puppeteer = join(staging, 'puppeteer.json');
    writeFileSync(puppeteer, JSON.stringify({ executablePath: browser }));
    args.push('-p', puppeteer);
  }
  const result = spawnSync(process.execPath, args, { encoding: 'utf8', timeout: 60000, maxBuffer: 2 * 1024 * 1024 });
  if (result.error) throw result.error;
  if (result.status !== 0) throw new Error(`Mermaid failed (${result.status}):\n${result.stderr || result.stdout}`);
  if (!existsSync(rendered) || statSync(rendered).size === 0) throw new Error('Renderer produced no output');
  if (opts.force) renameSync(rendered, output);
  else copyFileSync(rendered, output, constants.COPYFILE_EXCL);
  console.log(JSON.stringify({ output, format, bytes: statSync(output).size }));
} catch (error) {
  console.error(`error: ${error.message}`);
  process.exitCode = 1;
} finally {
  if (staging) rmSync(staging, { recursive: true, force: true });
}
