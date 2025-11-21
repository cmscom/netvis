
Examples
========

This section contains examples of using NetVis for interactive graph visualization in JupyterLab.

Basic Usage
-----------

The most basic usage of NetVis::

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


.. toctree::
    :glob:

    *
