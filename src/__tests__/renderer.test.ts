import { NetVisRenderer } from '../renderer';
import { IRenderMime } from '@jupyterlab/rendermime-interfaces';
import packageJson from '../../package.json';

// Mock MIME model type
interface IMimeModel {
  data: { [key: string]: any };
  metadata?: { [key: string]: any };
}

const CURRENT_VERSION = packageJson.version;

describe('NetVisRenderer', () => {
  const MIME_TYPE = 'application/vnd.netvis+json';

  describe('renderModel - success cases', () => {
    it('should render valid graph data', async () => {
      const renderer = new NetVisRenderer({
        mimeType: MIME_TYPE,
        sanitizer: {},
        resolver: null,
        linkHandler: null,
        latexTypesetter: null,
      } as IRenderMime.IRendererOptions);

      const graphData = JSON.stringify({
        nodes: [{ id: 'A' }, { id: 'B' }],
        links: [{ source: 'A', target: 'B' }],
      });

      const model: IMimeModel = {
        data: {
          [MIME_TYPE]: {
            data: graphData,
            version: CURRENT_VERSION,
          },
        },
      };

      await renderer.renderModel(model as any);

      // Check that SVG was created
      const svg = renderer.node.querySelector('svg');
      expect(svg).toBeTruthy();
    });

    it('should render graph with single node', async () => {
      const renderer = new NetVisRenderer({
        mimeType: MIME_TYPE,
        sanitizer: {},
        resolver: null,
        linkHandler: null,
        latexTypesetter: null,
      } as IRenderMime.IRendererOptions);

      const graphData = JSON.stringify({
        nodes: [{ id: 'A' }],
        links: [],
      });

      const model: IMimeModel = {
        data: {
          [MIME_TYPE]: {
            data: graphData,
            version: CURRENT_VERSION,
          },
        },
      };

      await renderer.renderModel(model as any);

      const svg = renderer.node.querySelector('svg');
      expect(svg).toBeTruthy();
    });
  });

  describe('renderModel - error cases', () => {
    it('should throw error for missing data field', async () => {
      const renderer = new NetVisRenderer({
        mimeType: MIME_TYPE,
        sanitizer: {},
        resolver: null,
        linkHandler: null,
        latexTypesetter: null,
      } as IRenderMime.IRendererOptions);

      const model: IMimeModel = {
        data: {
          [MIME_TYPE]: {
            version: CURRENT_VERSION,
          },
        },
      };

      await expect(renderer.renderModel(model as any)).rejects.toThrow(
        'missing data field',
      );
    });

    it('should throw error for invalid JSON', async () => {
      const renderer = new NetVisRenderer({
        mimeType: MIME_TYPE,
        sanitizer: {},
        resolver: null,
        linkHandler: null,
        latexTypesetter: null,
      } as IRenderMime.IRendererOptions);

      const model: IMimeModel = {
        data: {
          [MIME_TYPE]: {
            data: 'invalid json',
            version: CURRENT_VERSION,
          },
        },
      };

      await expect(renderer.renderModel(model as any)).rejects.toThrow();
    });

    it('should throw error for missing nodes', async () => {
      const renderer = new NetVisRenderer({
        mimeType: MIME_TYPE,
        sanitizer: {},
        resolver: null,
        linkHandler: null,
        latexTypesetter: null,
      } as IRenderMime.IRendererOptions);

      const graphData = JSON.stringify({
        links: [],
      });

      const model: IMimeModel = {
        data: {
          [MIME_TYPE]: {
            data: graphData,
            version: CURRENT_VERSION,
          },
        },
      };

      await expect(renderer.renderModel(model as any)).rejects.toThrow(
        'missing nodes or links',
      );
    });

    it('should throw error for missing links', async () => {
      const renderer = new NetVisRenderer({
        mimeType: MIME_TYPE,
        sanitizer: {},
        resolver: null,
        linkHandler: null,
        latexTypesetter: null,
      } as IRenderMime.IRendererOptions);

      const graphData = JSON.stringify({
        nodes: [{ id: 'A' }],
      });

      const model: IMimeModel = {
        data: {
          [MIME_TYPE]: {
            data: graphData,
            version: CURRENT_VERSION,
          },
        },
      };

      await expect(renderer.renderModel(model as any)).rejects.toThrow(
        'missing nodes or links',
      );
    });
  });

  describe('renderModel - multiple instances', () => {
    it('should create independent renderer instances', async () => {
      const renderer1 = new NetVisRenderer({
        mimeType: MIME_TYPE,
        sanitizer: {},
        resolver: null,
        linkHandler: null,
        latexTypesetter: null,
      } as IRenderMime.IRendererOptions);

      const renderer2 = new NetVisRenderer({
        mimeType: MIME_TYPE,
        sanitizer: {},
        resolver: null,
        linkHandler: null,
        latexTypesetter: null,
      } as IRenderMime.IRendererOptions);

      const graphData1 = JSON.stringify({
        nodes: [{ id: 'A' }],
        links: [],
      });

      const graphData2 = JSON.stringify({
        nodes: [{ id: 'B' }],
        links: [],
      });

      const model1: IMimeModel = {
        data: {
          [MIME_TYPE]: {
            data: graphData1,
            version: CURRENT_VERSION,
          },
        },
      };

      const model2: IMimeModel = {
        data: {
          [MIME_TYPE]: {
            data: graphData2,
            version: CURRENT_VERSION,
          },
        },
      };

      await renderer1.renderModel(model1 as any);
      await renderer2.renderModel(model2 as any);

      // Both should have their own SVG
      expect(renderer1.node.querySelector('svg')).toBeTruthy();
      expect(renderer2.node.querySelector('svg')).toBeTruthy();

      // They should be different DOM nodes
      expect(renderer1.node).not.toBe(renderer2.node);
    });
  });

  // Note: These tests verify that the renderer can process node and link data without errors.
  // Full SVG element verification requires integration tests in JupyterLab environment.
  describe('node and link rendering', () => {
    it('should successfully render graph with multiple nodes without error', async () => {
      const renderer = new NetVisRenderer({
        mimeType: MIME_TYPE,
        sanitizer: {},
        resolver: null,
        linkHandler: null,
        latexTypesetter: null,
      } as IRenderMime.IRendererOptions);

      const graphData = JSON.stringify({
        nodes: [{ id: 'A' }, { id: 'B' }, { id: 'C' }],
        links: [],
      });

      const model: IMimeModel = {
        data: {
          [MIME_TYPE]: {
            data: graphData,
            version: CURRENT_VERSION,
          },
        },
      };

      // Should not throw error
      await expect(renderer.renderModel(model as any)).resolves.toBeUndefined();
    });

    it('should successfully render graph with nodes and links without error', async () => {
      const renderer = new NetVisRenderer({
        mimeType: MIME_TYPE,
        sanitizer: {},
        resolver: null,
        linkHandler: null,
        latexTypesetter: null,
      } as IRenderMime.IRendererOptions);

      const graphData = JSON.stringify({
        nodes: [{ id: 'A' }, { id: 'B' }],
        links: [{ source: 'A', target: 'B' }],
      });

      const model: IMimeModel = {
        data: {
          [MIME_TYPE]: {
            data: graphData,
            version: CURRENT_VERSION,
          },
        },
      };

      // Should not throw error with links present
      await expect(renderer.renderModel(model as any)).resolves.toBeUndefined();
    });

    it('should successfully render complex graph with multiple nodes and links', async () => {
      const renderer = new NetVisRenderer({
        mimeType: MIME_TYPE,
        sanitizer: {},
        resolver: null,
        linkHandler: null,
        latexTypesetter: null,
      } as IRenderMime.IRendererOptions);

      const graphData = JSON.stringify({
        nodes: [{ id: '1' }, { id: '2' }, { id: '3' }, { id: '4' }],
        links: [
          { source: '1', target: '2' },
          { source: '2', target: '3' },
          { source: '3', target: '4' },
        ],
      });

      const model: IMimeModel = {
        data: {
          [MIME_TYPE]: {
            data: graphData,
            version: CURRENT_VERSION,
          },
        },
      };

      // Should handle complex graphs without errors
      await expect(renderer.renderModel(model as any)).resolves.toBeUndefined();
    });
  });

  describe('large graph performance', () => {
    it('should handle large graph (100 nodes, 200 links) without crashing', async () => {
      const renderer = new NetVisRenderer({
        mimeType: MIME_TYPE,
        sanitizer: {},
        resolver: null,
        linkHandler: null,
        latexTypesetter: null,
      } as IRenderMime.IRendererOptions);

      // Generate 100 nodes
      const nodes = [];
      for (let i = 0; i < 100; i++) {
        nodes.push({ id: `node_${i}` });
      }

      // Generate 200 links
      const links = [];
      for (let i = 0; i < 100; i++) {
        const target1 = (i + 1) % 100;
        const target2 = (i + 2) % 100;
        links.push({ source: `node_${i}`, target: `node_${target1}` });
        if (links.length < 200) {
          links.push({ source: `node_${i}`, target: `node_${target2}` });
        }
      }

      const graphData = JSON.stringify({ nodes, links: links.slice(0, 200) });

      const model: IMimeModel = {
        data: {
          [MIME_TYPE]: {
            data: graphData,
            version: CURRENT_VERSION,
          },
        },
      };

      // Should not throw error even with large graph
      await expect(renderer.renderModel(model as any)).resolves.toBeUndefined();
    });

    it('should handle very large graph (1000 nodes, 2000 links) without crashing', async () => {
      const renderer = new NetVisRenderer({
        mimeType: MIME_TYPE,
        sanitizer: {},
        resolver: null,
        linkHandler: null,
        latexTypesetter: null,
      } as IRenderMime.IRendererOptions);

      // Generate 1000 nodes
      const nodes = [];
      for (let i = 0; i < 1000; i++) {
        nodes.push({ id: `n${i}` });
      }

      // Generate 2000 links
      const links = [];
      for (let i = 0; i < 1000; i++) {
        const target1 = (i + 1) % 1000;
        const target2 = (i + 2) % 1000;
        links.push({ source: `n${i}`, target: `n${target1}` });
        if (links.length < 2000) {
          links.push({ source: `n${i}`, target: `n${target2}` });
        }
      }

      const graphData = JSON.stringify({ nodes, links: links.slice(0, 2000) });

      const model: IMimeModel = {
        data: {
          [MIME_TYPE]: {
            data: graphData,
            version: CURRENT_VERSION,
          },
        },
      };

      // Should handle very large graph without crashing (SC-008 requirement)
      await expect(renderer.renderModel(model as any)).resolves.toBeUndefined();
    });
  });
});
