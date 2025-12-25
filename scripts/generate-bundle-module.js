#!/usr/bin/env node
/**
 * Generate TypeScript module containing the standalone bundle content.
 *
 * This script reads the built netvis-standalone.min.js and generates
 * a TypeScript file that exports the bundle content as a string constant.
 *
 * Usage:
 *   node scripts/generate-bundle-module.js           # Generate from built bundle
 *   node scripts/generate-bundle-module.js --stub    # Create placeholder stub
 *
 * Output: src/standaloneBundleContent.ts
 */

const fs = require('fs');
const path = require('path');

const bundlePath = path.join(
  __dirname,
  '..',
  'net_vis',
  'resources',
  'netvis-standalone.min.js'
);
const outputPath = path.join(__dirname, '..', 'src', 'standaloneBundleContent.ts');

// Check if we should create a stub (placeholder)
const isStub = process.argv.includes('--stub');

if (isStub) {
  // Create a placeholder that allows TypeScript to compile
  const stubContent = `/**
 * Auto-generated stub file - will be replaced with actual bundle content.
 * DO NOT EDIT MANUALLY - regenerate with: node scripts/generate-bundle-module.js
 */

// Placeholder - will be replaced after webpack build
export const STANDALONE_BUNDLE: string = '';
`;
  fs.writeFileSync(outputPath, stubContent, 'utf8');
  console.log(`Created stub: ${outputPath}`);
  process.exit(0);
}

// Read the bundle
if (!fs.existsSync(bundlePath)) {
  console.error(`Error: Bundle not found at ${bundlePath}`);
  console.error('Run "yarn run build:standalone" first.');
  process.exit(1);
}

const bundleContent = fs.readFileSync(bundlePath, 'utf8');

// Generate TypeScript module
const tsContent = `/**
 * Auto-generated file containing the standalone bundle content.
 * DO NOT EDIT MANUALLY - regenerate with: node scripts/generate-bundle-module.js
 *
 * This module exports the minified D3.js + NetVis rendering code
 * for embedding in standalone HTML exports.
 */

// eslint-disable-next-line max-len
export const STANDALONE_BUNDLE: string = ${JSON.stringify(bundleContent)};
`;

// Write the TypeScript file
fs.writeFileSync(outputPath, tsContent, 'utf8');

console.log(`Generated: ${outputPath}`);
console.log(`Bundle size: ${(bundleContent.length / 1024).toFixed(1)} KB`);
