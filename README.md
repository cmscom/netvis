# netvis

NetVis is a package for interactive visualization Python NetworkX graphs within Jupyter Lab. It leverages D3.js for dynamic rendering and supports HTML export, making network analysis effortless.

## Installation

You can install using `pip`:

```bash
pip install net_vis
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:

```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] net_vis
```

## Quick Start

This section provides a simple guide to get started with the project using JupyterLab.

### Example

```
import net_vis
data = """
{
  "nodes": [
    {
      "page_id": 1,
      "id": "Network"
    },
    {
      "page_id": 2,
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

When executed, an SVG network graph is displayed.

- Display Sample

![Desplay Sample](https://github.com/cmscom/netvis/blob/docs/source/_static/img/demo.png)

## Development Installation

Create a dev environment:

```bash
conda create -n net_vis-dev -c conda-forge nodejs python jupyterlab=4.0.11
conda activate net_vis-dev
```

Install the python. This will also build the TS package.

```bash
pip install -e ".[test, examples]"
```

When developing your extensions, you need to manually enable your extensions with the
notebook / lab frontend. For lab, this is done by the command:

```
jupyter labextension develop --overwrite .
jlpm run build
```

For classic notebook, you need to run:

```
jupyter nbextension install --sys-prefix --symlink --overwrite --py net_vis
jupyter nbextension enable --sys-prefix --py net_vis
```

Note that the `--symlink` flag doesn't work on Windows, so you will here have to run
the `install` command every time that you rebuild your extension. For certain installations
you might also need another flag instead of `--sys-prefix`, but we won't cover the meaning
of those flags here.

### How to see your changes

#### Typescript:

If you use JupyterLab to develop then you can watch the source directory and run JupyterLab at the same time in different
terminals to watch for changes in the extension's source and automatically rebuild the widget.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm run watch
# Run JupyterLab in another terminal
jupyter lab
```

After a change wait for the build to finish and then refresh your browser and the changes should take effect.

#### Python:

If you make a change to the python code then you will need to restart the notebook kernel to have it take effect.

## Contributing

Contributions are welcome!  
For details on how to contribute, please refer to [CONTRIBUTING.md](https://github.com/cmscom/netvis/blob/main/CONTRIBUTING.md).

## Special Thanks

This project was initiated on the proposal of Shingo Tsuji. His invaluable contributions —from conceptual planning to requirements definition— have been instrumental in bringing this project to fruition. We extend our deepest gratitude for his vision and support.
