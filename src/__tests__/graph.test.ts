// Note: Full D3.js DOM manipulation testing requires integration tests in JupyterLab.
// These tests verify the API and error handling.

import { renderGraph, GraphData } from '../graph';

describe('D3.js Graph Interactions', () => {
  let container: HTMLElement;

  beforeEach(() => {
    // Create a fresh container for each test
    container = document.createElement('div');
    document.body.appendChild(container);
  });

  afterEach(() => {
    // Clean up
    document.body.removeChild(container);
  });

  describe('force simulation initialization', () => {
    it('should initialize D3 force simulation without errors', () => {
      const graphData: GraphData = {
        nodes: [{ id: 'A' }, { id: 'B' }, { id: 'C' }],
        links: [
          { source: 'A', target: 'B' },
          { source: 'B', target: 'C' },
        ],
      };

      // Should not throw error
      expect(() => renderGraph(container, graphData)).not.toThrow();
    });

    it('should handle empty graph (no links)', () => {
      const graphData: GraphData = {
        nodes: [{ id: 'A' }],
        links: [],
      };

      expect(() => renderGraph(container, graphData)).not.toThrow();
    });

    it('should handle graph with multiple components', () => {
      const graphData: GraphData = {
        nodes: [{ id: '1' }, { id: '2' }, { id: '3' }, { id: '4' }],
        links: [
          { source: '1', target: '2' }, // Component 1
          { source: '3', target: '4' }, // Component 2 (disconnected)
        ],
      };

      expect(() => renderGraph(container, graphData)).not.toThrow();
    });
  });

  describe('drag and interaction handlers', () => {
    it('should successfully render graph with nodes for drag interaction', () => {
      const graphData: GraphData = {
        nodes: [{ id: 'A' }, { id: 'B' }],
        links: [{ source: 'A', target: 'B' }],
      };

      // Should render without errors (drag handlers are set up internally)
      expect(() => renderGraph(container, graphData)).not.toThrow();
    });

    it('should handle node with custom size property', () => {
      const graphData: GraphData = {
        nodes: [
          { id: 'A', size: 10 },
          { id: 'B', size: 20 },
        ],
        links: [],
      };

      expect(() => renderGraph(container, graphData)).not.toThrow();
    });

    it('should handle nodes with category property for coloring', () => {
      const graphData: GraphData = {
        nodes: [
          { id: 'A', category: 'TYPE_A' },
          { id: 'B', category: 'TYPE_B' },
        ],
        links: [],
      };

      expect(() => renderGraph(container, graphData)).not.toThrow();
    });
  });

  describe('zoom and pan functionality', () => {
    it('should initialize without errors (zoom/pan configured internally)', () => {
      const graphData: GraphData = {
        nodes: [{ id: 'A' }],
        links: [],
      };

      // Zoom and pan are set up by D3, verified in integration tests
      expect(() => renderGraph(container, graphData)).not.toThrow();
    });
  });

  describe('error handling', () => {
    it('should throw error for null data', () => {
      expect(() => renderGraph(container, null as any)).toThrow(
        'GraphData is required',
      );
    });

    it('should throw error for missing nodes', () => {
      const invalidData = { links: [] } as any;
      expect(() => renderGraph(container, invalidData)).toThrow(
        'GraphData must have nodes array',
      );
    });

    it('should throw error for missing links', () => {
      const invalidData = { nodes: [{ id: 'A' }] } as any;
      expect(() => renderGraph(container, invalidData)).toThrow(
        'GraphData must have links array',
      );
    });

    it('should throw error for nodes without id', () => {
      const invalidData: GraphData = {
        nodes: [{ id: 'A' }, {} as any], // Second node missing id
        links: [],
      };
      expect(() => renderGraph(container, invalidData)).toThrow(
        "nodes are missing 'id' field",
      );
    });
  });
});
