
Examples
========

This section contains examples of using NetVis for interactive graph visualization in JupyterLab.


NetworkX Plotter API (Recommended)
-----------------------------------

The easiest way to visualize NetworkX graphs::

    from net_vis import Plotter
    import networkx as nx

    # Create and visualize NetworkX graph
    G = nx.karate_club_graph()
    plotter = Plotter(title="Karate Club Network")
    plotter.add_networkx(G)

For comprehensive examples including custom styling, layouts, and multi-graph support, see the :ref:`NetworkX Plotter API notebook <networkx_plotter>` below.


HTML Export (New in v0.6.0)
---------------------------

Export visualizations as self-contained HTML files::

    # Export to file
    plotter.export_html("my_graph.html")

    # Export with customization
    plotter.export_html(
        "report.html",
        title="Network Analysis",
        description="Generated from NetworkX graph",
        width="800px",
        height=700
    )

    # Get HTML as string
    html = plotter.export_html()

    # Browser download for remote environments
    plotter.export_html("graph.html", download=True)

The exported HTML files work offline and include all interactive features. See the :ref:`HTML Export notebook <html_export>` for more examples.


Low-Level API
-------------

For advanced control with manual JSON, you can use the low-level NetVis API:

**Basic Usage**

The most basic usage of the low-level API::

    import net_vis

    data = """
    {
      "nodes": [
        {"id": "Node1"},
        {"id": "Node2"},
        {"id": "Node3"}
      ],
      "links": [
        {"source": "Node1", "target": "Node2"},
        {"source": "Node2", "target": "Node3"}
      ]
    }
    """

    vis = net_vis.NetVis(value=data)
    vis

Custom Node Properties
-----------------------

You can customize node appearance with additional properties::

    import net_vis

    data = """
    {
      "nodes": [
        {"id": "A", "size": 10, "category": "type1"},
        {"id": "B", "size": 20, "category": "type2"},
        {"id": "C", "size": 15, "category": "type1"}
      ],
      "links": [
        {"source": "A", "target": "B"},
        {"source": "B", "target": "C"}
      ]
    }
    """

    vis = net_vis.NetVis(value=data)
    vis

Large Graphs
------------

NetVis can handle large graphs efficiently. The force-directed layout automatically adjusts to the size of the graph.


.. note::

    For more examples, see the `examples directory <https://github.com/cmscom/netvis/tree/main/examples>`_ in the GitHub repository.


Detailed Examples
-----------------

.. toctree::
    :maxdepth: 2

    networkx_plotter
    html_export
    introduction
