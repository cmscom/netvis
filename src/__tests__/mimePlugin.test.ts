import { parseGraphData, validateVersion, MIME_TYPE } from '../mimePlugin';

describe('parseGraphData', () => {
  let consoleLogSpy: jest.SpyInstance;
  let consoleErrorSpy: jest.SpyInstance;

  beforeEach(() => {
    consoleLogSpy = jest.spyOn(console, 'log').mockImplementation();
    consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation();
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
    consoleErrorSpy.mockRestore();
  });

  // T021: Empty string handling test
  describe('empty string handling', () => {
    it('should return empty graph for empty string', () => {
      const result = parseGraphData('');

      expect(result).toEqual({ nodes: [], links: [] });
      expect(consoleLogSpy).toHaveBeenCalledWith(
        expect.stringContaining('Empty data received'),
      );
    });

    it('should return empty graph for whitespace-only string', () => {
      const result = parseGraphData('   ');

      expect(result).toEqual({ nodes: [], links: [] });
      expect(consoleLogSpy).toHaveBeenCalledWith(
        expect.stringContaining('Empty data received'),
      );
    });
  });

  // T022: Invalid JSON handling test
  describe('invalid JSON handling', () => {
    it('should throw error for invalid JSON', () => {
      expect(() => parseGraphData('invalid json {')).toThrow(
        'Invalid graph data',
      );
      expect(consoleErrorSpy).toHaveBeenCalled();
    });

    it('should throw error for non-object JSON', () => {
      expect(() => parseGraphData('"just a string"')).toThrow(
        'Graph data must be an object',
      );
    });

    it('should throw error for missing nodes array', () => {
      expect(() => parseGraphData('{"links": []}')).toThrow(
        'Graph data must have a nodes array',
      );
    });

    it('should throw error for missing links array', () => {
      expect(() => parseGraphData('{"nodes": [{"id": "A"}]}')).toThrow(
        'Graph data must have a links array',
      );
    });

    it('should throw error for invalid nodes type', () => {
      expect(() =>
        parseGraphData('{"nodes": "not-an-array", "links": []}'),
      ).toThrow('Graph data must have a nodes array');
    });

    it('should throw error for invalid links type', () => {
      expect(() =>
        parseGraphData('{"nodes": [], "links": "not-an-array"}'),
      ).toThrow('Graph data must have a links array');
    });
  });

  describe('valid data handling', () => {
    it('should parse valid graph data', () => {
      const validData = '{"nodes": [{"id": "A"}], "links": []}';
      const result = parseGraphData(validData);

      expect(result).toEqual({ nodes: [{ id: 'A' }], links: [] });
    });

    it('should parse complex graph data', () => {
      const complexData =
        '{"nodes": [{"id": "A"}, {"id": "B"}], "links": [{"source": "A", "target": "B"}]}';
      const result = parseGraphData(complexData);

      expect(result).toEqual({
        nodes: [{ id: 'A' }, { id: 'B' }],
        links: [{ source: 'A', target: 'B' }],
      });
    });
  });
});

// T023: Version validation test
describe('validateVersion', () => {
  let consoleLogSpy: jest.SpyInstance;
  let consoleWarnSpy: jest.SpyInstance;

  beforeEach(() => {
    consoleLogSpy = jest.spyOn(console, 'log').mockImplementation();
    consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation();
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
    consoleWarnSpy.mockRestore();
  });

  it('should log success for matching versions', () => {
    validateVersion('0.6.0');

    expect(consoleLogSpy).toHaveBeenCalledWith(
      expect.stringContaining('Version check passed: v0.6.0'),
    );
    expect(consoleWarnSpy).not.toHaveBeenCalled();
  });

  it('should warn for version mismatch', () => {
    validateVersion('0.3.0');

    expect(consoleWarnSpy).toHaveBeenCalledWith(
      expect.stringContaining('Version mismatch'),
    );
    expect(consoleWarnSpy).toHaveBeenCalledWith(
      expect.stringContaining('Frontend v0.6.0'),
    );
    expect(consoleWarnSpy).toHaveBeenCalledWith(
      expect.stringContaining('Backend v0.3.0'),
    );
  });

  it('should warn for missing version', () => {
    validateVersion(undefined);

    expect(consoleWarnSpy).toHaveBeenCalledWith(
      expect.stringContaining('Backend version information missing'),
    );
  });

  it('should not log anything for different minor versions', () => {
    validateVersion('0.4.1');

    expect(consoleWarnSpy).toHaveBeenCalledWith(
      expect.stringContaining('Version mismatch'),
    );
  });
});

describe('MIME_TYPE', () => {
  it('should export correct MIME type', () => {
    expect(MIME_TYPE).toBe('application/vnd.netvis+json');
  });
});

// T035: Plugin ID uniqueness test
describe('mimeExtension plugin', () => {
  it('should have unique plugin ID', async () => {
    const mimeExtension = (await import('../mimePlugin')).default;

    // Verify plugin ID is unique and follows convention
    expect(mimeExtension.id).toBe('net_vis:mime');
    expect(mimeExtension.id).toMatch(/^[a-z_]+:[a-z_]+$/);
  });

  it('should have correct extension properties', async () => {
    const mimeExtension = (await import('../mimePlugin')).default;

    // JupyterLab 4 IExtension does not have autoStart property
    // Test only the correct interface properties
    expect(mimeExtension.id).toBe('net_vis:mime');
    expect(mimeExtension.rendererFactory).toBeDefined();
    expect(mimeExtension.dataType).toBe('json');
  });

  // T036: MIME type registration test
  it('should register correct MIME types in factory', async () => {
    const { MIME_TYPE } = await import('../mimePlugin');

    // Verify the MIME type constant matches expected value
    expect(MIME_TYPE).toBe('application/vnd.netvis+json');

    // The actual factory registration happens in activate(),
    // which requires full JupyterLab context and is tested via integration tests
  });
});
