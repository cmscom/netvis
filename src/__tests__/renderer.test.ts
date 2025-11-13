// T012: TypeScript renderer tests

import { NetVisRenderer } from '../renderer';

// Mock IRenderMime types
interface IMimeModel {
  data: { [key: string]: any };
  metadata?: { [key: string]: any };
}

interface IRendererOptions {
  mimeType: string;
  sanitizer?: any;
  resolver?: any;
  linkHandler?: any;
  latexTypesetter?: any;
}

describe('NetVisRenderer', () => {
  const MIME_TYPE = 'application/vnd.netvis+json';

  describe('renderModel - success cases', () => {
    it('should render valid graph data', async () => {
      const renderer = new NetVisRenderer({
        mimeType: MIME_TYPE,
      } as IRendererOptions);

      const graphData = JSON.stringify({
        nodes: [{ id: 'A' }, { id: 'B' }],
        links: [{ source: 'A', target: 'B' }],
      });

      const model: IMimeModel = {
        data: {
          [MIME_TYPE]: {
            data: graphData,
            version: '0.4.0',
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
      } as IRendererOptions);

      const graphData = JSON.stringify({
        nodes: [{ id: 'A' }],
        links: [],
      });

      const model: IMimeModel = {
        data: {
          [MIME_TYPE]: {
            data: graphData,
            version: '0.4.0',
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
      } as IRendererOptions);

      const model: IMimeModel = {
        data: {
          [MIME_TYPE]: {
            version: '0.4.0',
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
      } as IRendererOptions);

      const model: IMimeModel = {
        data: {
          [MIME_TYPE]: {
            data: 'invalid json',
            version: '0.4.0',
          },
        },
      };

      await expect(renderer.renderModel(model as any)).rejects.toThrow();
    });

    it('should throw error for missing nodes', async () => {
      const renderer = new NetVisRenderer({
        mimeType: MIME_TYPE,
      } as IRendererOptions);

      const graphData = JSON.stringify({
        links: [],
      });

      const model: IMimeModel = {
        data: {
          [MIME_TYPE]: {
            data: graphData,
            version: '0.4.0',
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
      } as IRendererOptions);

      const graphData = JSON.stringify({
        nodes: [{ id: 'A' }],
      });

      const model: IMimeModel = {
        data: {
          [MIME_TYPE]: {
            data: graphData,
            version: '0.4.0',
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
      } as IRendererOptions);

      const renderer2 = new NetVisRenderer({
        mimeType: MIME_TYPE,
      } as IRendererOptions);

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
            version: '0.4.0',
          },
        },
      };

      const model2: IMimeModel = {
        data: {
          [MIME_TYPE]: {
            data: graphData2,
            version: '0.4.0',
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
});
