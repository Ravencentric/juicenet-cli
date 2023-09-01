# juicenet

Crude script for conveniently uploading .mkv files to usenet.

## Features

- Looks into subdirectories for `.mkv` files
- Generates `par2` files for each `.mkv`
- Passes the `.mkv` file along with it's corresponding `.par2` files directly to Nyuu
- Can move the files into their own folders if you wish to manually upload
- Checks for raw articles every run and tries to repost if found
- Probably has alot of cases where it breaks. Worked on my machine in my limited testing
- Someone please make a better script I can't code

## Prerequisites

- [Python 3.11](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) (optional)
- [animetosho/Nyuu@a4b1712](https://github.com/animetosho/Nyuu/commit/a4b1712d77faeacaae114c966c238773acc534fb) - You need this version or newer. [v0.4.1 is outdated and you shouldn't use it](https://github.com/animetosho/Nyuu/releases/tag/v0.4.1).
  - Until animetosho uploads a new release, you can grab the [Windows binary here](https://github.com/Ravencentric/Nyuu/actions/runs/6051631932).
- [animetosho/ParPar](https://github.com/animetosho/ParPar)

## Installation

1. Run `git clone https://github.com/Ravencentric/juicenet.git` or download this [ZIP](https://github.com/Ravencentric/juicenet/archive/refs/heads/main.zip)

#### With Poetry

1. Run `cd juicenet`
2. Run `poetry install` to install the 3rd party dependencies.
3. Run `poetry shell` to pop a shell into the virtual environment.

#### Without Poetry

1. Run `cd juicenet`
2. Run `pip install -r requirements.txt` to install 3rd party dependencies.

## Usage

Rename `juicenet.yaml.example` to `juicenet.yaml` and replace the dummy values with your own. This must exist next to your `juicenet.py` and named the same as the py file.

### Windows

```txt
py juicenet.py "path\to\directory\with\mkv\files"
```

### Linux

```txt
python3 juicenet.py "path/to/directory/with/mkv/files"
```

### help

```txt
> juicenet.py --help
usage: juicenet.py [-h] [-P] [-p] [-n] [-r] [-v] [-m] path

A script for conveniently uploading .mkv files to usenet

positional arguments:
  path           Path to directory containing .mkv files

options:
  -h, --help     show this help message and exit
  -P, --public   Use your public config. By default it'll use your private config.
  -p, --parpar   Only run Parpar
  -n, --nyuu     Only run Nyuu
  -r, --raw      Only repost raw articles
  -v, --verbose  Show everything in terminal
  -m, --move     Move files into their own directories (not required)
```
