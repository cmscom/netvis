/**
 * Tests for HTML Export functionality (Download Button)
 *
 * T069-T074: TypeScript tests for download button in JupyterLab
 */

import {
  generateFilename,
  generateStandaloneHtml,
  downloadHtml,
  createDownloadButton,
  ExportConfig,
} from '../htmlExport';

// T072: test_generated_filename_format() - verify netvis_export_YYYY-MM-DD.html format
describe('generateFilename', () => {
  it('should generate filename with current date in YYYY-MM-DD format', () => {
    const filename = generateFilename();

    // Should match pattern netvis_export_YYYY-MM-DD.html
    expect(filename).toMatch(/^netvis_export_\d{4}-\d{2}-\d{2}\.html$/);
  });

  it('should use current date', () => {
    const today = new Date().toISOString().split('T')[0];
    const filename = generateFilename();

    expect(filename).toBe(`netvis_export_${today}.html`);
  });
});

// T073: test_generated_html_structure() - verify HTML has required elements
describe('generateStandaloneHtml', () => {
  const mockGraphData = {
    nodes: [{ id: 'A', name: 'Node A' }],
    links: [],
  };

  const defaultConfig: ExportConfig = {
    title: 'Test Graph',
    width: '100%',
    height: 600,
    graphData: mockGraphData,
  };

  it('should generate valid HTML5 document', () => {
    const html = generateStandaloneHtml(defaultConfig);

    expect(html).toContain('<!DOCTYPE html>');
    expect(html).toContain('<html');
    expect(html).toContain('</html>');
  });

  it('should include UTF-8 charset meta tag', () => {
    const html = generateStandaloneHtml(defaultConfig);

    expect(html).toContain('charset="UTF-8"');
  });

  it('should include viewport meta tag for responsive design', () => {
    const html = generateStandaloneHtml(defaultConfig);

    expect(html).toContain('name="viewport"');
  });

  it('should embed custom title in document', () => {
    const html = generateStandaloneHtml({
      ...defaultConfig,
      title: 'My Custom Graph',
    });

    expect(html).toContain('<title>My Custom Graph</title>');
  });

  it('should use default title when not provided', () => {
    const config: ExportConfig = {
      ...defaultConfig,
      title: undefined as unknown as string,
    };
    const html = generateStandaloneHtml(config);

    expect(html).toContain('<title>Network Visualization</title>');
  });

  it('should embed graph data as JSON', () => {
    const html = generateStandaloneHtml(defaultConfig);

    // Graph data should be embedded in script
    expect(html).toContain('"nodes"');
    expect(html).toContain('"id":"A"');
  });

  it('should include inline CSS styles', () => {
    const html = generateStandaloneHtml(defaultConfig);

    expect(html).toContain('<style>');
    expect(html).toContain('</style>');
  });

  it('should include inline JavaScript', () => {
    const html = generateStandaloneHtml(defaultConfig);

    expect(html).toContain('<script>');
    expect(html).toContain('</script>');
  });

  it('should include graph container with specified dimensions', () => {
    const html = generateStandaloneHtml({
      ...defaultConfig,
      width: '800px',
      height: 700,
    });

    expect(html).toContain('width: 800px');
    expect(html).toContain('height: 700px');
  });

  it('should handle empty graph data', () => {
    const html = generateStandaloneHtml({
      ...defaultConfig,
      graphData: { nodes: [], links: [] },
    });

    // Should still generate valid HTML
    expect(html).toContain('<!DOCTYPE html>');
    expect(html).toContain('"nodes":[]');
    expect(html).toContain('"links":[]');
  });
});

// T071: test_download_button_click() - verify click triggers download
describe('downloadHtml', () => {
  let mockCreateObjectURL: jest.Mock;
  let mockRevokeObjectURL: jest.Mock;
  let mockAppendChild: jest.SpyInstance;
  let mockRemoveChild: jest.SpyInstance;
  let mockClick: jest.Mock;
  let mockLink: HTMLAnchorElement;
  let originalCreateObjectURL: typeof URL.createObjectURL;
  let originalRevokeObjectURL: typeof URL.revokeObjectURL;

  beforeEach(() => {
    // Save originals
    originalCreateObjectURL = URL.createObjectURL;
    originalRevokeObjectURL = URL.revokeObjectURL;

    // Mock URL methods by direct assignment (jsdom doesn't have these)
    mockCreateObjectURL = jest.fn().mockReturnValue('blob:mock-url');
    mockRevokeObjectURL = jest.fn();
    URL.createObjectURL = mockCreateObjectURL;
    URL.revokeObjectURL = mockRevokeObjectURL;

    // Mock DOM methods
    mockClick = jest.fn();
    mockLink = {
      href: '',
      download: '',
      click: mockClick,
    } as unknown as HTMLAnchorElement;

    jest.spyOn(document, 'createElement').mockReturnValue(mockLink);
    mockAppendChild = jest
      .spyOn(document.body, 'appendChild')
      .mockImplementation(() => mockLink);
    mockRemoveChild = jest
      .spyOn(document.body, 'removeChild')
      .mockImplementation(() => mockLink);
  });

  afterEach(() => {
    // Restore originals
    URL.createObjectURL = originalCreateObjectURL;
    URL.revokeObjectURL = originalRevokeObjectURL;
    jest.restoreAllMocks();
  });

  it('should create Blob with HTML content', () => {
    const htmlContent = '<!DOCTYPE html><html></html>';
    downloadHtml(htmlContent, 'test.html');

    expect(mockCreateObjectURL).toHaveBeenCalledWith(expect.any(Blob));
  });

  it('should set correct filename on link element', () => {
    downloadHtml('<html></html>', 'my_graph.html');

    expect(mockLink.download).toBe('my_graph.html');
  });

  it('should trigger click on link element', () => {
    downloadHtml('<html></html>', 'test.html');

    expect(mockClick).toHaveBeenCalled();
  });

  it('should clean up blob URL after download', () => {
    downloadHtml('<html></html>', 'test.html');

    expect(mockRevokeObjectURL).toHaveBeenCalledWith('blob:mock-url');
  });

  it('should append and remove link from document body', () => {
    downloadHtml('<html></html>', 'test.html');

    expect(mockAppendChild).toHaveBeenCalledWith(mockLink);
    expect(mockRemoveChild).toHaveBeenCalledWith(mockLink);
  });
});

// T070: test_download_button_renders() - verify button appears in renderer output
describe('createDownloadButton', () => {
  let mockGraphData: { nodes: any[]; links: any[] };

  beforeEach(() => {
    mockGraphData = {
      nodes: [{ id: 'A' }],
      links: [],
    };
  });

  it('should create a button element', () => {
    const button = createDownloadButton(mockGraphData);

    expect(button.tagName).toBe('BUTTON');
  });

  it('should have correct CSS class', () => {
    const button = createDownloadButton(mockGraphData);

    expect(button.classList.contains('netvis-download-btn')).toBe(true);
  });

  // T074: test_button_accessibility() - verify aria-label attribute
  it('should have aria-label for accessibility', () => {
    const button = createDownloadButton(mockGraphData);

    expect(button.getAttribute('aria-label')).toBe('Download HTML');
  });

  it('should contain SVG icon', () => {
    const button = createDownloadButton(mockGraphData);

    const svg = button.querySelector('svg');
    expect(svg).not.toBeNull();
  });

  it('should trigger download on click', () => {
    // Save originals
    const originalCreateObjectURL = URL.createObjectURL;
    const originalRevokeObjectURL = URL.revokeObjectURL;
    const originalCreateElement = document.createElement.bind(document);

    // Mock URL methods
    URL.createObjectURL = jest.fn().mockReturnValue('blob:mock');
    URL.revokeObjectURL = jest.fn();

    const mockClick = jest.fn();

    // Mock createElement to only intercept anchor creation
    jest
      .spyOn(document, 'createElement')
      .mockImplementation((tagName: string) => {
        if (tagName === 'a') {
          return {
            href: '',
            download: '',
            click: mockClick,
          } as unknown as HTMLAnchorElement;
        }
        return originalCreateElement(tagName);
      });

    jest
      .spyOn(document.body, 'appendChild')
      .mockImplementation((node) => node as Node);
    jest
      .spyOn(document.body, 'removeChild')
      .mockImplementation((node) => node as Node);

    const button = createDownloadButton(mockGraphData);
    button.click();

    expect(mockClick).toHaveBeenCalled();

    // Restore originals
    URL.createObjectURL = originalCreateObjectURL;
    URL.revokeObjectURL = originalRevokeObjectURL;
    jest.restoreAllMocks();
  });
});

// T092: Empty graph button test
describe('download button with empty graph', () => {
  it('should work with empty graph data', () => {
    const emptyGraphData = { nodes: [], links: [] };
    const button = createDownloadButton(emptyGraphData);

    expect(button).toBeDefined();
    expect(button.classList.contains('netvis-download-btn')).toBe(true);
  });

  it('should generate valid HTML for empty graph', () => {
    const config: ExportConfig = {
      title: 'Empty Graph',
      width: '100%',
      height: 600,
      graphData: { nodes: [], links: [] },
    };
    const html = generateStandaloneHtml(config);

    expect(html).toContain('<!DOCTYPE html>');
    expect(html).toContain('"nodes":[]');
  });
});
