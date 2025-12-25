# Changelog

## 0.6.0 (2025-12-25)

**Feature Release: Standalone HTML Export** (terapyon)

### New Features

- **HTML Export API**: Export visualizations as self-contained HTML files
  - `Plotter.export_html()` method for saving graphs as standalone HTML
  - Works offline without internet connection or JupyterLab
  - Preserves all interactive features (zoom, pan, node selection, drag)

- **One-Click Download Button**: Download HTML directly from JupyterLab
  - Download button appears in top-right corner of visualization
  - Click to instantly save as `netvis_export_YYYY-MM-DD.html`
  - Works independently of kernel state (client-side generation)
  - No code required for quick exports

- **Export Customization**:
  - Custom title and description for HTML documents
  - Configurable container width (CSS values) and height (pixels)
  - Default responsive layout (100% width x 600px height)

- **Flexible Output Options**:
  - File export with automatic .html extension
  - Automatic parent directory creation
  - HTML string return for programmatic use
  - Browser download trigger for remote environments (JupyterHub, Google Colab)

### API Examples

```python
from net_vis import Plotter
import networkx as nx

G = nx.karate_club_graph()
plotter = Plotter(title="Karate Club")
plotter.add_networkx(G)

# Export to file
path = plotter.export_html("my_graph.html")

# Export with customization
plotter.export_html(
    "report.html",
    title="Network Analysis",
    description="Karate club social network",
    width="800px",
    height=700
)

# Get HTML string
html = plotter.export_html()

# Remote environment download
plotter.export_html("graph.html", download=True)
```

### Implementation Details

- **HTMLExporter**: Template-based HTML generation using string.Template
- **Standalone Bundle**: D3.js + rendering code bundled via webpack (~280KB)
- **Test Coverage**: 50 new tests (26 Python + 24 TypeScript) covering all export functionality
- **Error Handling**: Proper exception propagation for file system errors

### Compatibility

- All modern browsers (Chrome, Firefox, Safari, Edge)
- Offline capable (no CDN or internet dependency)
- JupyterLab: 3.x and 4.x
- Python: 3.10+

## 0.5.0 (2025-12-24)

**Major Feature Release: NetworkX Plotter API** (terapyon)

### New Features

- **High-level Plotter API**: Direct NetworkX graph visualization without manual JSON conversion
  - `Plotter.add_networkx()` method for seamless graph rendering in JupyterLab
  - Support for all 4 NetworkX graph types: Graph, DiGraph, MultiGraph, MultiDiGraph
  - Automatic node/edge extraction with attribute preservation

- **Custom Styling Support**:
  - Node color mapping via attribute names or callable functions
  - Node label mapping with flexible attribute selection
  - Edge label mapping for relationship visualization
  - Automatic color scale detection (continuous vs. categorical)

- **Layout Control**:
  - 5 built-in layout algorithms: spring, kamada_kawai, spectral, circular, random
  - Custom layout function support
  - Existing position attribute detection
  - Automatic fallback with NaN/inf validation

- **Multi-Graph Type Support**:
  - Edge direction preservation for DiGraph (via metadata)
  - Edge key preservation for MultiGraph/MultiDiGraph
  - Multiple edge expansion into independent Edge objects
  - Automatic graph type detection and dispatch

### API Examples

```python
from net_vis import Plotter
import networkx as nx

# Basic visualization
G = nx.karate_club_graph()
plotter = Plotter(title="Karate Club Network")
plotter.add_networkx(G)

# Custom styling
plotter.add_networkx(G,
    node_color="club",
    node_label=lambda d: f"Node {d.get('name', '')}",
    layout='kamada_kawai'
)
```

### Implementation Details

- **NetworkXAdapter**: 650+ lines of conversion logic with comprehensive type hints
- **Test Coverage**: 60+ test methods covering all public APIs
- **Python 3.10+ type hints**: Full type annotation support
- **Comprehensive docstrings**: All public methods documented

### Installation Options

- **Basic**: `pip install net_vis` - Includes spring, circular, and random layouts
- **Full**: `pip install net_vis[full]` - Includes all layouts (adds SciPy for kamada_kawai and spectral)

### Dependencies

**Core:**

- NetworkX 3.0+
- NumPy 2.0+ (required for layout algorithms)

**Optional (installed with [full]):**

- SciPy 1.8+ (required for kamada_kawai and spectral layouts)

### Compatibility

- JupyterLab: 3.x and 4.x
- Python: 3.10+

## 0.4.0 (2025-11-21)

**Major Release: Migration to MIME Renderer Architecture** (terapyon)

### Breaking Changes

- **Removed ipywidgets dependency**: NetVis no longer requires or uses ipywidgets for rendering
- **Removed nbextension support**: The Jupyter Notebook classic extension has been removed
- **Simplified installation**: No manual extension enabling required - works automatically in JupyterLab 3.x/4.x
- **Python API unchanged**: Existing code using `NetVis(value=data)` continues to work without modification

### New Features

- MIME Renderer Architecture using custom MIME type `application/vnd.netvis+json`
- Automatic rendering in JupyterLab output cells
- Version validation between frontend and backend
- Enhanced error handling for invalid graph data

### Improvements

- Cleaner codebase with duplicate code removed
- Better performance with simplified rendering pipeline
- Comprehensive test coverage (Python 75%, TypeScript 41%)
- Modern JupyterLab 3.x/4.x architecture

### Migration

See [MIGRATION.md](./MIGRATION.md) for migration guide from 0.3.x to 0.4.0.

### Compatibility

- Supported: JupyterLab 3.x and 4.x
- Not Supported: Jupyter Notebook Classic
- Python: 3.10+
- D3.js: 7.9+ (all visualization features preserved)

## 0.3.1 (2025-07-12)

- bugfix for build version (terapyon)

## 0.3.0 (2025-07-12)

- Add node text (karad)

## 0.2.0 (2025-04-04)

- Additional styling capabilities for network visualization (karad)
- Enhanced customization options for nodes and links (karad)
- Improved color scheme and style configuration support (karad)
- Fixed package installation and CI/CD workflows (terapyon)

## 0.1.1 (2025-04-02)

- Modify document links (terapyon)
- PyPI releases using GitHub Actions (terapyon)

## 0.1.0 (2025-03-08)

- internal release (terapyon)
