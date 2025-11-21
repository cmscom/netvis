
.. _installation:

Installation
============


The simplest way to install net_vis is via pip::

    pip install net_vis

**That's it!** As of version 0.4.0, NetVis uses a MIME renderer that works automatically in JupyterLab 3.x and 4.x environments. No additional installation or configuration steps are required.


Requirements
------------

- Python 3.10 or later
- JupyterLab 3.x or 4.x

**Note**: Jupyter Notebook Classic is no longer supported as of version 0.4.0. Please use JupyterLab instead.


Upgrading from 0.3.x
---------------------

If you're upgrading from version 0.3.x, please see the `MIGRATION.md <https://github.com/cmscom/netvis/blob/main/MIGRATION.md>`_ guide for detailed migration instructions.

Key changes in 0.4.0:

- **Simplified installation**: No manual extension enabling required
- **MIME renderer architecture**: Replaces ipywidgets-based rendering
- **JupyterLab only**: Jupyter Notebook Classic is no longer supported
- **Python API unchanged**: Your existing code will continue to work
