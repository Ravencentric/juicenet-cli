# Installation

juicenet-cli is a tool designed to simplify the process of uploading files to usenet. It's built with Python and uses Nyuu and ParPar under the hood.

## Prerequisites

* [Python >=3.9](https://www.python.org/downloads/)
* [Nyuu](https://github.com/animetosho/Nyuu)
* [ParPar](https://github.com/animetosho/ParPar)

!!! note
    You need Nyuu version [`a4b1712`](https://github.com/animetosho/Nyuu/commit/a4b1712d77faeacaae114c966c238773acc534fb) or newer. [v0.4.1 is outdated and you shouldn't use it](https://github.com/animetosho/Nyuu/releases/tag/v0.4.1).

    Until animetosho uploads a new release, you can grab the [Windows binary here](https://github.com/Ravencentric/Nyuu/releases/latest).

## Installing juicenet-cli

1. With [pipx](https://pypa.github.io/pipx/installation/) (recommended):

    ```console
    pipx install juicenet-cli
    ```

2. With pip:

    ```console
    pip install juicenet-cli
    ```

3. From git with [poetry](https://python-poetry.org/docs/#installation):

    !!! note
        The `main` branch is not stable and maybe broken. Use this method if you know what you're doing.

        Stable (mostly) builds can be found in [releases](https://github.com/Ravencentric/juicenet-cli/releases) or [PyPI](https://pypi.org/project/juicenet-cli/).

    ```console
    git clone https://github.com/Ravencentric/juicenet-cli.git
    ```

    ```console
    cd juicenet-cli
    ```

    Run:

    ```console
    poetry install
    ```

    ```console
    poetry run juicenet --help
    ```

    Build:

    ```console
    poetry build
    ```
