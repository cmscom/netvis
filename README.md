# netvis

NetVis is a package for interactive visualization of Python NetworkX graphs within JupyterLab. It leverages D3.js for dynamic rendering and provides a high-level Plotter API for effortless network analysis.

**Version 0.6.0** adds standalone HTML export, enabling you to share visualizations as self-contained HTML files that work anywhere—no JupyterLab or internet connection required.

## Installation

### Basic Installation

You can install using `pip`:

```bash
pip install net_vis
```

This provides core functionality with layouts: **spring**, **circular**, and **random**.

### Full Installation (Recommended)

For all layout algorithms including **kamada_kawai** and **spectral**:

```bash
pip install net_vis[full]
```

This installs optional dependencies (scipy) required for advanced layout algorithms.

**Note**: NetVis uses a MIME renderer that works automatically in JupyterLab 3.x and 4.x environments. No manual extension enabling is required.

## Quick Start

### NetworkX Plotter API (New in v0.5.0)

The easiest way to visualize NetworkX graphs in JupyterLab:

```python
from net_vis import Plotter
import networkx as nx

# Create a NetworkX graph
G = nx.karate_club_graph()

# Visualize with one line
plotter = Plotter(title="Karate Club Network")
plotter.add_networkx(G)
```

#### Custom Styling

Control node colors, labels, and layouts:

```python
# Color nodes by attribute, customize labels
plotter = Plotter(title="Styled Network")
plotter.add_networkx(
    G,
    node_color="club",              # Use 'club' attribute for colors
    node_label=lambda d: f"Node {d.get('name', '')}",  # Custom labels
    edge_label="weight",            # Show edge weights
    layout='kamada_kawai'           # Choose layout algorithm
)
```

#### Supported Features

- **Graph Types**: Graph, DiGraph, MultiGraph, MultiDiGraph
- **Layouts**: spring (default), kamada_kawai, spectral, circular, random, or custom functions
- **Styling**: Attribute-based or function-based color/label mapping
- **Automatic**: Node/edge attribute preservation in metadata

#### HTML Export (New in v0.6.0)

Export your visualizations as standalone HTML files:

```python
# Export to file
path = plotter.export_html("my_graph.html")
print(f"Exported to {path}")

# Export with customization
plotter.export_html(
    "report.html",
    title="Network Analysis Report",
    description="Generated from NetworkX graph",
    width="800px",
    height=700
)

# Get HTML as string for embedding
html = plotter.export_html()
```

The exported HTML files:
- Work offline (no internet required)
- Include all interactive features (zoom, pan, node selection)
- Are self-contained (no external dependencies)
- Open in any modern browser

#### One-Click Download Button (New in v0.6.0)

When viewing a graph in JupyterLab, you'll see a download button in the top-right corner of the visualization. Click it to instantly download the graph as a standalone HTML file:

- **No code needed**: Just click the button
- **Works offline**: Button works even if the kernel is stopped
- **Auto-named**: Files are saved as `netvis_export_YYYY-MM-DD.html`

| Use Case | Method |
|----------|--------|
| Quick download | Click the download button |
| Custom filename | `plotter.export_html("my_name.html")` |
| Programmatic export | `html = plotter.export_html()` |

### Low-Level API (Advanced)

For manual control over the visualization data structure:

```python
import net_vis

data = """
{
  "nodes": [
    {
      "id": "Network"
    },
    {
      "id": "Graph"
    }
  ],
  "links": [
    {
      "source": "Network",
      "target": "Graph"
    }
  ]
}
"""

w = net_vis.NetVis(value=data)
w
```

When executed, an interactive D3.js force-directed graph is displayed.

- Display Sample

![Desplay Sample](https://raw.githubusercontent.com/cmscom/netvis/refs/heads/main/docs/source/_static/img/demo.png)

![JpyterLab Sample](https://raw.githubusercontent.com/cmscom/netvis/refs/heads/main/docs/source/_static/img/net-vis-0.4.0.jpg)

## Development Installation

Create a dev environment:

```bash
python -m venv venv-netvis
source venv-netvis/bin/activate
```

Install the Python package. This will also build the TypeScript package:

```bash
pip install -e ".[test, examples, docs]"
```

Install JavaScript dependencies and build the extension:

```bash
yarn install
jupyter labextension develop --overwrite .
yarn run build
```

**Note**: As of version 0.4.0, nbextension support has been removed. NetVis now exclusively uses the MIME renderer architecture for JupyterLab 3.x and 4.x.

### How to see your changes

#### TypeScript:

If you use JupyterLab to develop, you can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
yarn run watch
# Run JupyterLab in another terminal
jupyter lab
```

After a change, wait for the build to finish and then refresh your browser and the changes should take effect.

#### Python:

If you make a change to the Python code, you will need to restart the notebook kernel to have it take effect.

## Contributing

Contributions are welcome!  
For details on how to contribute, please refer to [CONTRIBUTING.md](https://github.com/cmscom/netvis/blob/main/CONTRIBUTING.md).

## Special Thanks

This project was initiated on the proposal of Shingo Tsuji. His invaluable contributions —from conceptual planning to requirements definition— have been instrumental in bringing this project to fruition. We extend our deepest gratitude for his vision and support.
