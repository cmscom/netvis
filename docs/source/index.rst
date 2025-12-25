
net_vis
=====================================

Version: |release|

NetVis is a package for interactive visualization of Python NetworkX graphs within JupyterLab. It leverages D3.js for dynamic rendering and provides a high-level Plotter API for effortless network analysis.

**Version 0.6.0** adds standalone HTML export, enabling you to share visualizations as self-contained HTML files that work anywhere—no JupyterLab or internet connection required.


Quickstart
----------

To get started with net_vis, install with pip::

    pip install net_vis

**NetworkX Plotter API**::

    from net_vis import Plotter
    import networkx as nx

    # Create and visualize NetworkX graph
    G = nx.karate_club_graph()
    plotter = Plotter(title="Karate Club Network")
    plotter.add_networkx(G)

**HTML Export (New in v0.6.0)**::

    # Export to standalone HTML file
    plotter.export_html("my_graph.html")

    # Export with customization
    plotter.export_html(
        "report.html",
        title="Network Analysis",
        description="Karate club social network"
    )

    # Get HTML as string for embedding
    html = plotter.export_html()

**One-Click Download Button**: When viewing a graph in JupyterLab, click the download button (top-right corner) to instantly save the visualization as an HTML file.

**Note**: NetVis uses a MIME renderer that works automatically in JupyterLab 3.x and 4.x. Manual extension enabling is not required.


Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Installation and usage

   installing
   introduction

.. toctree::
   :maxdepth: 1

   examples/index


.. toctree::
   :maxdepth: 2
   :caption: Development

   develop-install


.. links

.. _`Jupyter widgets`: https://jupyter.org/widgets.html

.. _`notebook`: https://jupyter-notebook.readthedocs.io/en/latest/
