
Developer install
=================


To install a developer version of net_vis, you will first need to clone
the repository::

    git clone https://github.com/cmscom/netvis
    cd netvis

Create a development environment::

    python -m venv venv-netvis
    source venv-netvis/bin/activate

Install the Python package with development dependencies::

    pip install -e ".[test, examples, docs]"

Install JavaScript dependencies and set up the JupyterLab extension::

    yarn install
    jupyter labextension develop --overwrite .
    yarn run build


Development workflow
--------------------

TypeScript development
^^^^^^^^^^^^^^^^^^^^^^

To watch for changes and automatically rebuild the extension::

    # Terminal 1: Watch TypeScript source
    yarn run watch

    # Terminal 2: Run JupyterLab
    jupyter lab

After making changes, wait for the build to finish, then refresh your browser.

Python development
^^^^^^^^^^^^^^^^^^

If you make changes to the Python code, restart the Jupyter kernel to see the effects.


Running tests
-------------

Run Python tests::

    pytest -v

Run TypeScript tests::

    yarn run test

Run linting::

    yarn run lint:check
    python -m ruff check net_vis
    python -m pyright net_vis


**Note**: As of version 0.4.0, nbextension support has been removed. NetVis now exclusively uses the MIME renderer architecture for JupyterLab 3.x and 4.x.
