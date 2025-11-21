# netvis

NetVis is a package for interactive visualization of Python NetworkX graphs within JupyterLab. It leverages D3.js for dynamic rendering and supports HTML export, making network analysis effortless.

**Version 0.4.0** introduces a MIME renderer architecture that simplifies installation and improves compatibility with modern JupyterLab environments.

## Installation

You can install using `pip`:

```bash
pip install net_vis
```

**Note for version 0.4.0+**: The nbextension is no longer required. NetVis now uses a MIME renderer that works automatically in JupyterLab 3.x and 4.x environments.

## Quick Start

This section provides a simple guide to get started with the project using JupyterLab.

### Example

```python
import net_vis

data = """
{
  "nodes": [
    {
      "id": "Network"
    },
    {
      "id": "Graph"
    }
  ],
  "links": [
    {
      "source": "Network",
      "target": "Graph"
    }
  ]
}
"""

w = net_vis.NetVis(value=data)
w
```

When executed, an interactive D3.js force-directed graph is displayed.

- Display Sample

![Desplay Sample](https://raw.githubusercontent.com/cmscom/netvis/refs/heads/main/docs/source/_static/img/demo.png)

![JpyterLab Sample](https://raw.githubusercontent.com/cmscom/netvis/refs/heads/main/docs/source/_static/img/net-vis-0.4.0.jpg)

## Development Installation

Create a dev environment:

```bash
python -m venv venv-netvis
source venv-netvis/bin/activate
```

Install the Python package. This will also build the TypeScript package:

```bash
pip install -e ".[test, examples, docs]"
```

Install JavaScript dependencies and build the extension:

```bash
yarn install
jupyter labextension develop --overwrite .
yarn run build
```

**Note**: As of version 0.4.0, nbextension support has been removed. NetVis now exclusively uses the MIME renderer architecture for JupyterLab 3.x and 4.x.

### How to see your changes

#### TypeScript:

If you use JupyterLab to develop, you can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
yarn run watch
# Run JupyterLab in another terminal
jupyter lab
```

After a change, wait for the build to finish and then refresh your browser and the changes should take effect.

#### Python:

If you make a change to the Python code, you will need to restart the notebook kernel to have it take effect.

## Contributing

Contributions are welcome!  
For details on how to contribute, please refer to [CONTRIBUTING.md](https://github.com/cmscom/netvis/blob/main/CONTRIBUTING.md).

## Special Thanks

This project was initiated on the proposal of Shingo Tsuji. His invaluable contributions —from conceptual planning to requirements definition— have been instrumental in bringing this project to fruition. We extend our deepest gratitude for his vision and support.
