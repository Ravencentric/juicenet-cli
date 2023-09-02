# juicenet

Crude script for conveniently uploading files to usenet.

## Features

- Looks into subdirectories for specific files as defined in `juicenet.yaml`
- Generates `par2` files
- Passes the file along with it's corresponding `.par2` files directly to Nyuu
- Can move the files into their own folders if you wish to manually upload
- Checks for raw articles every run and tries to repost if found
- Can't continue from where it stopped if it gets interrupted for any reason
- Probably has alot of cases where it breaks. Worked on my machine in my limited testing
- Someone please make a better script I can't code

## Prerequisites

- [Python 3.11](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) (optional)
- [animetosho/Nyuu@a4b1712](https://github.com/animetosho/Nyuu/commit/a4b1712d77faeacaae114c966c238773acc534fb) - You need this version or newer. [v0.4.1 is outdated and you shouldn't use it](https://github.com/animetosho/Nyuu/releases/tag/v0.4.1).
  - Until animetosho uploads a new release, you can grab the [Windows binary here](https://github.com/Ravencentric/Nyuu/actions/runs/6051631932).
- [animetosho/ParPar](https://github.com/animetosho/ParPar)

## Installation

### With Poetry

1. `git clone https://github.com/Ravencentric/juicenet.git` or download this [ZIP](https://github.com/Ravencentric/juicenet/archive/refs/heads/main.zip)
2. `cd juicenet`
3. `poetry install` to install the 3rd party dependencies.
4. `poetry shell` to pop a shell into the virtual environment.

### Without Poetry

1. `git clone https://github.com/Ravencentric/juicenet.git` or download this [ZIP](https://github.com/Ravencentric/juicenet/archive/refs/heads/main.zip)
2. `cd juicenet`
3. `pip install -r requirements.txt` to install 3rd party dependencies.

## Usage

Rename `juicenet.yaml.example` to `juicenet.yaml` and replace the dummy values with your own. This must exist next to your `juicenet.py` and named the same as the py file.

### Windows

```txt
py juicenet.py "path\to\directory\with\files"
```

### Linux

```txt
python3 juicenet.py "path/to/directory/with/files"
```

### help

```txt
> py juicenet.py --help
usage: juicenet.py [-h] [-P] [-p] [-n] [-r] [-v] [-e [.mkv .mp4 ...]] [-m] path

A script for conveniently uploading files to usenet

positional arguments:
  path                  Path to directory containing your files

options:
  -h, --help            show this help message and exit
  -P, --public          Use your public config. Default: private
  -p, --parpar          Only run Parpar
  -n, --nyuu            Only run Nyuu
  -r, --raw             Only repost raw articles
  -v, --verbose         Show everything in terminal
  -e [.mkv .mp4 ...], --extensions [.mkv .mp4 ...]
                        Ignore config and look for these extensions only
  -m, --move            Move files into their own directories (not required)
```
