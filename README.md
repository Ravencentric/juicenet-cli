<br/>
<p align="center">
  <a href="https://github.com/Ravencentric/juicenet-cli">
    <img src="https://em-content.zobj.net/source/twitter/376/beverage-box_1f9c3.png" alt="Logo" width="100" height="100">
  </a>

  <h3 align="center">juicenet-cli</h3>

  <p align="center">
    Crude CLI tool to upload files to Usenet using Nyuu and ParPar
    <br/>
    <br/>
  </p>
</p>

<div align="center">
  
[![PyPI - Version](https://img.shields.io/pypi/v/juicenet-cli?link=https%3A%2F%2Fpypi.org%2Fproject%2Fjuicenet-cli%2F)
](https://pypi.org/project/juicenet-cli/) ![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/Ravencentric/juicenet-cli/pypi.yml) ![Issues](https://img.shields.io/github/issues/Ravencentric/juicenet-cli) ![License](https://img.shields.io/github/license/Ravencentric/juicenet-cli)

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

* Searches subdirectories for defined file extensions in `juicenet.yaml` or as passed in `--exts`
* Alternatively, searches for glob patterns passed in `--pattern`
* Provides basic BDMV support
* Creates par2 files
* Directly passes files and corresponding .par2 files to Nyuu
* Offers the option to organize files into separate folders for manual upload
* Automatically checks for and reposts raw articles on each run
* Can **NOT** continue from where it stopped if it gets interrupted for any reason
* Probably has alot of cases where it breaks. I've tried to keep it OS independent but I've mostly tested this on Windows

## Getting Started

This script uses ParPar for generating the PAR2 recovery files and Nyuu for uploading to usenet.

### Prerequisites

* [Python 3.11](https://www.python.org/downloads/)
* [animetosho/Nyuu](https://github.com/animetosho/Nyuu) - You need version [`a4b1712`](https://github.com/animetosho/Nyuu/commit/a4b1712d77faeacaae114c966c238773acc534fb) or newer. [v0.4.1 is outdated and you shouldn't use it](https://github.com/animetosho/Nyuu/releases/tag/v0.4.1).
  * Until animetosho uploads a new release, you can grab the [Windows binary here](https://github.com/Ravencentric/Nyuu/releases/latest).
* [animetosho/ParPar](https://github.com/animetosho/ParPar)

### Installation

1. With pipx (recommended):

    ```sh
    pipx install juicenet-cli
    ```

2. With pip:

    ```sh
    pip install juicenet-cli
    ```

3. With poetry:

    ```sh
    git clone https://github.com/Ravencentric/juicenet-cli.git
    ```

    ```sh
    cd juicenet-cli
    ```

    ```sh
    poetry install
    ```

    ```sh
    poetry shell
    ```

## Usage

Before you can use this, you'll have to fill out [`juicenet.yaml`](https://github.com/Ravencentric/juicenet-cli/blob/main/juicenet.yaml). After you've specified all the values in the config you just have to pass it to juicenet-cli. You can do that in one of three ways:

1. Using the command-line argument: `--config <path>`
2. Setting an environment variable named `JUICENET_CONFIG`
3. Placing the configuration file in the current working directory as `juicenet.yaml`

The order of precedence, if all three are present, is:
`command-line argument > environment variable > local file in the current working directory`

The above was the first time setup, after which you can simply run:

```sh
juicenet "path\to\directory\with\files"
```

For more information, go [here](https://github.com/Ravencentric/juicenet-cli/wiki).

## License

Distributed under the [Unlicense](https://choosealicense.com/licenses/unlicense/) License. See [UNLICENSE](https://github.com/Ravencentric/juicenet-cli/blob/main/UNLICENSE) for more information.
