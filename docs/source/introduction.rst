=============
Introduction
=============

NetVis is a package for interactive visualization of Python NetworkX graphs within JupyterLab. It leverages D3.js for dynamic rendering, providing an intuitive and powerful way to explore and analyze network data.


Key Features
------------

- **Interactive D3.js Visualization**: Force-directed graph layout with interactive node dragging, zooming, and panning
- **Simple Python API**: Works seamlessly with NetworkX graph data structures
- **MIME Renderer Architecture**: Automatic rendering in JupyterLab 3.x and 4.x without manual extension configuration
- **Customizable Appearance**: Support for custom node colors, sizes, and categories
- **Modern Stack**: Built with TypeScript and modern JupyterLab extension architecture


Quick Example
-------------

Here's a simple example to get you started::

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


Architecture (v0.4.0)
---------------------

Version 0.4.0 introduces a major architectural change:

**MIME Renderer**
    NetVis now uses JupyterLab's MIME renderer system instead of ipywidgets. This means:

    - Simpler installation (no manual extension enabling)
    - Better performance and integration with JupyterLab
    - Cleaner codebase with modern TypeScript

**JupyterLab Only**
    NetVis 0.4.0+ exclusively supports JupyterLab 3.x and 4.x. Jupyter Notebook Classic is no longer supported.

**Python API Unchanged**
    Despite the internal changes, the Python API remains 100% compatible with previous versions.


What's New in 0.4.0
-------------------

- **MIME renderer architecture** replacing ipywidgets
- **Simplified installation** - just ``pip install net_vis``
- **Removed nbextension support** - JupyterLab only
- **Python 3.10+ support** including 3.13 and 3.14
- **Comprehensive test suite** with 41 TypeScript tests and 16 Python tests
- **Code quality tools** - ruff and pyright for Python linting and type checking


Migrating from 0.3.x
---------------------

If you're upgrading from version 0.3.x, your existing code will continue to work without changes. However, you should be aware that:

1. Jupyter Notebook Classic is no longer supported
2. Manual extension enabling is no longer required
3. Some internal APIs have changed (if you were using them directly)

For detailed migration instructions, see `MIGRATION.md <https://github.com/cmscom/netvis/blob/main/MIGRATION.md>`_.
