
net_vis
=====================================

Version: |release|

NetVis is a package for interactive visualization of Python NetworkX graphs within JupyterLab. It leverages D3.js for dynamic rendering and supports HTML export, making network analysis effortless.

**Version 0.4.0** introduces a MIME renderer architecture that simplifies installation and improves compatibility with modern JupyterLab environments.


Quickstart
----------

To get started with net_vis, install with pip::

    pip install net_vis

**Note**: As of version 0.4.0, NetVis uses a MIME renderer that works automatically in JupyterLab 3.x and 4.x. Manual extension enabling is no longer required.


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
