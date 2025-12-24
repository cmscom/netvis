/**
 * Standalone bundle entry point for HTML export.
 *
 * This module exports the renderGraph function for use in standalone HTML files.
 * It bundles all necessary D3.js modules and rendering code into a single file.
 *
 * Usage in exported HTML:
 *   netvis.renderGraph(container, graphData);
 */

import { renderGraph, GraphData } from './graph';

// Export renderGraph for standalone HTML usage
export { renderGraph, GraphData };

// Also expose types for documentation purposes
export type { Node, Link, GraphOptions } from './graph';
