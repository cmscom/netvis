
.. _installation:

Installation
============

Basic Installation
------------------

The simplest way to install net_vis is via pip::

    pip install net_vis

This provides core functionality with the following layout algorithms:

- **spring** (force-directed)
- **circular**
- **random**

Full Installation (Recommended)
--------------------------------

For all layout algorithms including advanced options::

    pip install net_vis[full]

This installs optional dependencies (scipy) and enables additional layouts:

- **kamada_kawai** (stress-minimization)
- **spectral** (eigenvalue-based)

**That's it!** As of version 0.4.0, NetVis uses a MIME renderer that works automatically in JupyterLab 3.x and 4.x environments. No additional installation or configuration steps are required.


Requirements
------------

**Core Dependencies:**

- Python 3.10 or later
- JupyterLab 3.x or 4.x
- NetworkX 3.0+ (automatically installed)
- NumPy 2.0+ (automatically installed, required for layout algorithms)

**Optional Dependencies (installed with [full]):**

- SciPy 1.8+ (required for kamada_kawai and spectral layouts)

**Note**: Jupyter Notebook Classic is no longer supported as of version 0.4.0. Please use JupyterLab instead.


Upgrading from 0.3.x
---------------------

If you're upgrading from version 0.3.x, please see the `MIGRATION.md <https://github.com/cmscom/netvis/blob/main/MIGRATION.md>`_ guide for detailed migration instructions.

Key changes in 0.4.0:

- **Simplified installation**: No manual extension enabling required
- **MIME renderer architecture**: Replaces ipywidgets-based rendering
- **JupyterLab only**: Jupyter Notebook Classic is no longer supported
- **Python API unchanged**: Your existing code will continue to work
