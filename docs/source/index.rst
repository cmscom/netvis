
net_vis
=====================================

Version: |release|

NetVis is a package for interactive visualization of Python NetworkX graphs within JupyterLab. It leverages D3.js for dynamic rendering and provides a high-level Plotter API for effortless network analysis.

**Version 0.5.0** introduces the NetworkX Plotter API, enabling direct visualization of NetworkX graph objects without manual JSON conversion.


Quickstart
----------

To get started with net_vis, install with pip::

    pip install net_vis

**NetworkX Plotter API (New in v0.5.0)**::

    from net_vis import Plotter
    import networkx as nx

    # Create and visualize NetworkX graph
    G = nx.karate_club_graph()
    plotter = Plotter(title="Karate Club Network")
    plotter.add_networkx(G)

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
