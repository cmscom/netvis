from setuptools import setup, find_packages

setup(
    name="net_vis",
    version="0.2.0",
    description="NetVis is a package for interactive visualization Python NetworkX graphs within Jupyter Lab",
    packages=find_packages(),
    install_requires=[
        "ipywidgets>=8.0.0",
    ],
    extras_require={
        "docs": [
            "jupyter_sphinx",
            "nbsphinx",
            "nbsphinx-link",
            "pypandoc",
            "pytest_check_links",
            "recommonmark",
            "sphinx>=1.5",
            "sphinx_rtd_theme",
        ],
        "examples": [],
        "test": [
            "nbval",
            "pytest-cov",
            "pytest>=6.0",
        ],
    }
)
