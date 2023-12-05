<br/>
<p align="center">
  <a href="https://github.com/Ravencentric/juicenet-cli">
    <img src="https://em-content.zobj.net/source/twitter/376/beverage-box_1f9c3.png" alt="Logo" width="100" height="100">
  </a>

  <h3 align="center">juicenet-cli</h3>

  <p align="center">
    CLI tool designed to simplify the process of uploading files to usenet
    <br/>
    <br/>
  </p>
</p>

<div align="center">

[![PyPI - Version](https://img.shields.io/pypi/v/juicenet-cli?link=https%3A%2F%2Fpypi.org%2Fproject%2Fjuicenet-cli%2F)](https://pypi.org/project/juicenet-cli/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/juicenet-cli)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/Ravencentric/juicenet-cli/release.yml)
![License](https://img.shields.io/github/license/Ravencentric/juicenet-cli)
![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)

</div>

## Table Of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [License](#license)

## About The Project

Uploading stuff to usenet is tedious so I tried to make it easier.

* Uses [ParPar](https://github.com/animetosho/ParPar) and [Nyuu](https://github.com/animetosho/Nyuu) under the hood
* Recursively searches for files with pre-defined extensions in `juicenet.yaml` or as passed in `--exts`
* Alternatively, searches for glob patterns passed in `--glob`
* Preserves folder structure without RAR. [RAR sucks and here's why](https://github.com/animetosho/Nyuu/wiki/Stop-RAR-Uploads)
* Does everything automatically and gives you the resulting `nzbs` in a neatly sorted manner
* Offers the option to pick and choose what it does if you don't want it doing everything automatically
* Automatically checks for and reposts failed articles from last run. Also has the option to not do this.
* Can **NOT** continue from where it stopped if it gets interrupted for any reason

## Getting Started

`juicenet-cli` is built with Python and uses Nyuu and ParPar under the hood.

### Prerequisites

* [Python >=3.9](https://www.python.org/downloads/)
* [Nyuu](https://github.com/animetosho/Nyuu) - You need version [`a4b1712`](https://github.com/animetosho/Nyuu/commit/a4b1712d77faeacaae114c966c238773acc534fb) or newer. [v0.4.1 is outdated and you shouldn't use it](https://github.com/animetosho/Nyuu/releases/tag/v0.4.1)
  * Until animetosho uploads a new release, you can grab the [Windows binary here](https://github.com/Ravencentric/Nyuu/releases/latest)
* [ParPar](https://github.com/animetosho/ParPar)

### Installation

1. With [pipx](https://pypa.github.io/pipx/installation/) (recommended):

    ```sh
    pipx install juicenet-cli
    ```

2. With pip:

    ```sh
    pip install juicenet-cli
    ```

3. From source with [poetry](https://python-poetry.org/docs/#installation):
    > **Note**: The `main` branch is not stable and maybe broken. Use this method if you know what you're doing. Stable (mostly) builds can be found in [releases](https://github.com/Ravencentric/juicenet-cli/releases) or [PyPI](https://pypi.org/project/juicenet-cli/)

    ```sh
    git clone https://github.com/Ravencentric/juicenet-cli.git
    ```

    ```sh
    cd juicenet-cli
    ```

    Run:

    ```sh
    poetry install
    ```

    ```sh
    poetry shell
    ```

    ```sh
    python -m juicenet --help
    ```

    Build:

    ```sh
    poetry build
    ```

## Docs

Checkout the documentation [here](https://ravencentric.github.io/juicenet-cli/)

## License

Distributed under the [Unlicense](https://choosealicense.com/licenses/unlicense/) License. See [UNLICENSE](https://github.com/Ravencentric/juicenet-cli/blob/main/UNLICENSE) for more information.
