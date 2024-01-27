# Local Installation

## Prerequisites

Since `juicenet` uses Nyuu and ParPar, you need to have these installed. Follow the instructions below to install them.

=== "With Executables (Windows)"

    1. [`ParPar >= 0.4.2`](https://github.com/animetosho/ParPar) - Grab the executable from [here](https://github.com/animetosho/ParPar/releases/latest)

    2. [`Nyuu >= 0.4.2`](https://github.com/animetosho/Nyuu) - Grab the executable from [here](https://github.com/animetosho/Nyuu/releases/latest)


=== "With NPM (Windows)"

    1. Install [`Visual C++ Build Environment`](https://github.com/nodejs/node-gyp#on-windows)

    2. Install [`nvm`](https://github.com/coreybutler/nvm-windows/releases/latest)

    3. Install [`node`](https://nodejs.org/en)

        ``` bash
        nvm install node
        ```

    4. Install [`yencode`](https://github.com/animetosho/node-yencode)

        ``` bash
        npm install yencode
        ```

    5. Install [`Nyuu`](https://github.com/animetosho/Nyuu)

        ``` bash
        npm install -g nyuu --production --unsafe-perm
        ```

    6. Install [`ParPar`](https://github.com/animetosho/ParPar)

        ``` bash
        npm install -g @animetosho/parpar
        ```

=== "With NPM (Linux)"

    1. Install [`nvm`](https://github.com/nvm-sh/nvm)

        ``` bash
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
        ```

    2. Install [`node`](https://nodejs.org/en)

        ``` bash
        nvm install node
        ```

    3. Install [`yencode`](https://github.com/animetosho/node-yencode)

        ``` bash
        npm install yencode
        ```

    4. Install [`Nyuu`](https://github.com/animetosho/Nyuu)

        ``` bash
        npm install -g nyuu --production --unsafe-perm
        ```

    5. Install [`ParPar`](https://github.com/animetosho/ParPar)

        ``` bash
        npm install -g @animetosho/parpar
        ```

## Installing juicenet

`juicenet` currently supports [`Python >= 3.9`](https://www.python.org/downloads/)

1. With [pipx](https://pypa.github.io/pipx/installation/) (recommended):

    ``` shell
    pipx install juicenet-cli
    ```

2. With pip:

    ``` shell
    pip install juicenet-cli
    ```

3. From git with [poetry](https://python-poetry.org/docs/#installation):

    !!! note
        The `main` branch is not stable and maybe broken. Use this method if you know what you're doing.

        Stable (mostly) builds can be found in [releases](https://github.com/Ravencentric/juicenet-cli/releases) or [PyPI](https://pypi.org/project/juicenet-cli/).

    ``` shell
    git clone https://github.com/Ravencentric/juicenet-cli.git
    ```

    ``` shell
    cd juicenet-cli
    ```

    Run:

    ``` shell
    poetry install
    ```

    ``` shell
    poetry run juicenet --help
    ```

    Build:

    ``` shell
    poetry build
    ```
