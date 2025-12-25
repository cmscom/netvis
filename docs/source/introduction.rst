=============
Introduction
=============

NetVis is a package for interactive visualization of Python NetworkX graphs within JupyterLab. It leverages D3.js for dynamic rendering, providing an intuitive and powerful way to explore and analyze network data.


Key Features
------------

- **Standalone HTML Export (v0.6.0)**: Export visualizations as self-contained HTML files that work offline
- **One-Click Download Button (v0.6.0)**: Download HTML directly from JupyterLab visualization with a single click
- **NetworkX Plotter API (v0.5.0)**: Direct visualization of NetworkX graphs without JSON conversion
- **Interactive D3.js Visualization**: Force-directed graph layout with interactive node dragging, zooming, and panning
- **Multiple Graph Types**: Support for Graph, DiGraph, MultiGraph, and MultiDiGraph
- **Layout Control**: 5 built-in algorithms (spring, kamada_kawai, spectral, circular, random) plus custom functions
- **Custom Styling**: Attribute-based or function-based color and label mapping
- **MIME Renderer Architecture**: Automatic rendering in JupyterLab 3.x and 4.x without manual extension configuration
- **Modern Stack**: Built with TypeScript and modern JupyterLab extension architecture


Quick Example (NetworkX Plotter API)
-------------------------------------

The easiest way to visualize NetworkX graphs (new in v0.5.0)::

    from net_vis import Plotter
    import networkx as nx

    # Create NetworkX graph
    G = nx.karate_club_graph()

    # Visualize with one line
    plotter = Plotter(title="Karate Club Network")
    plotter.add_networkx(G)

    # Custom styling
    plotter = Plotter()
    plotter.add_networkx(
        G,
        node_color="club",              # Use 'club' attribute for colors
        node_label=lambda d: f"Node {d.get('name', '')}",
        edge_label="weight",
        layout='kamada_kawai'           # Choose layout algorithm
    )

When executed in JupyterLab, this displays an interactive force-directed graph.


Low-Level API Example
----------------------

For advanced control, you can use the low-level API with manual JSON::

    import net_vis

    data = """
    {
      "nodes": [
        {"id": "A"},
        {"id": "B"},
        {"id": "C"}
      ],
      "links": [
        {"source": "A", "target": "B"},
        {"source": "B", "target": "C"}
      ]
    }
    """

    w = net_vis.NetVis(value=data)
    w

When executed in JupyterLab, this displays an interactive force-directed graph where you can:

- **Drag nodes** to rearrange the layout
- **Zoom and pan** to explore different areas
- **Hover over nodes** to see labels
- **Click nodes** to pin/unpin them


What's New in 0.5.0
-------------------

Version 0.5.0 introduces the **NetworkX Plotter API**, a high-level interface for visualizing NetworkX graphs:

**NetworkX Plotter API**
    - Direct visualization of NetworkX graph objects without manual JSON conversion
    - Support for all 4 NetworkX graph types: Graph, DiGraph, MultiGraph, MultiDiGraph
    - Automatic node and edge extraction with full attribute preservation

**Layout Control**
    - 5 built-in layout algorithms: spring, kamada_kawai, spectral, circular, random
    - Custom layout function support
    - Automatic fallback for invalid positions (NaN/inf)

**Custom Styling**
    - Node color mapping via attribute names or callable functions
    - Node label mapping with flexible attribute selection
    - Edge label mapping for relationship visualization
    - Automatic color scale detection (continuous vs. categorical)

**Multi-Graph Type Support**
    - Edge direction preservation for DiGraph (stored in metadata)
    - Edge key preservation for MultiGraph/MultiDiGraph
    - Multiple edges expanded to independent Edge objects
    - Automatic graph type detection and dispatch

See the :doc:`examples/index` for complete usage examples.


What's New in 0.6.0
-------------------

Version 0.6.0 introduces **Standalone HTML Export**, enabling you to share visualizations without JupyterLab:

**HTML Export API**
    Export visualizations as self-contained HTML files::

        # Export to file
        plotter.export_html("my_graph.html")

        # Export with customization
        plotter.export_html(
            "report.html",
            title="Network Analysis Report",
            description="Generated analysis results",
            width="800px",
            height=700
        )

        # Get HTML as string for embedding
        html = plotter.export_html()

**One-Click Download Button**
    When viewing a graph in JupyterLab, a download button appears in the top-right corner:

    - Click the button to instantly download the visualization as HTML
    - Files are automatically named ``netvis_export_YYYY-MM-DD.html``
    - Works even when the kernel is stopped (client-side generation)
    - No code required for quick exports

**Exported HTML Features**
    - Works offline (no internet connection required)
    - All JavaScript and CSS embedded inline
    - Interactive features preserved (zoom, pan, node dragging)
    - Opens in any modern browser (Chrome, Firefox, Safari, Edge)

**Remote Environment Support**
    For JupyterHub, Google Colab, or Binder environments::

        # Trigger browser download to local PC
        plotter.export_html("graph.html", download=True)


Architecture (v0.4.0)
---------------------

Version 0.4.0 introduced a major architectural change:

**MIME Renderer**
    NetVis uses JupyterLab's MIME renderer system instead of ipywidgets. This means:

    - Simpler installation (no manual extension enabling)
    - Better performance and integration with JupyterLab
    - Cleaner codebase with modern TypeScript

**JupyterLab Only**
    NetVis 0.4.0+ exclusively supports JupyterLab 3.x and 4.x. Jupyter Notebook Classic is no longer supported.

**Python API**
    The low-level NetVis API remains compatible with previous versions, and the new Plotter API provides a higher-level interface.


Migrating from 0.3.x
---------------------

If you're upgrading from version 0.3.x, your existing code will continue to work without changes. However, you should be aware that:

1. Jupyter Notebook Classic is no longer supported
2. Manual extension enabling is no longer required
3. Some internal APIs have changed (if you were using them directly)

For detailed migration instructions, see `MIGRATION.md <https://github.com/cmscom/netvis/blob/main/MIGRATION.md>`_.
