# Changelog

## 0.5.0 (2025-12-22)

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

### Compatibility

- NetworkX: 3.0+
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
