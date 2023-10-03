# juicenet

Crude CLI tool to upload files to Usenet using Nyuu and ParPar.

## Features

- Looks into subdirectories for specific extensions as defined in `juicenet.yaml`
- Alternatively, look for glob pattern(s) instead of extensions
- Rudimentary BDMV support (read how to use it [here](https://github.com/Ravencentric/juicenet/wiki))
- Generates `par2` files
- Passes the file along with it's corresponding `.par2` files directly to Nyuu
- Can move the files into their own folders if you wish to manually upload
- Checks for raw articles every run and tries to repost if found
- Can't continue from where it stopped if it gets interrupted for any reason
- Probably has alot of cases where it breaks. Worked on my machine in my limited testing

## Prerequisites

- [Python 3.11](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) (optional)
- [animetosho/Nyuu@a4b1712](https://github.com/animetosho/Nyuu/commit/a4b1712d77faeacaae114c966c238773acc534fb) - You need this version or newer. [v0.4.1 is outdated and you shouldn't use it](https://github.com/animetosho/Nyuu/releases/tag/v0.4.1).
  - Until animetosho uploads a new release, you can grab the [Windows binary here](https://github.com/Ravencentric/Nyuu/releases/latest).
- [animetosho/ParPar](https://github.com/animetosho/ParPar)

## Installation

### With Poetry

1. `git clone https://github.com/Ravencentric/juicenet.git` or download this [zip](https://github.com/Ravencentric/juicenet/archive/refs/heads/main.zip)
2. `cd juicenet`
3. `poetry install` to install the 3rd party dependencies.
4. `poetry shell` to pop a shell into the virtual environment.

### Without Poetry

1. `git clone https://github.com/Ravencentric/juicenet.git` or download this [zip](https://github.com/Ravencentric/juicenet/archive/refs/heads/main.zip)
2. `cd juicenet`
3. `pip install -r requirements.txt` to install 3rd party dependencies.

## Usage

Rename `juicenet.yaml.example` to `juicenet.yaml` and replace the dummy values with your own. This must exist next to your `juicenet.py` and named the same as the py file.

### Windows

```powershell
python juicenet.py "path\to\directory\with\files"
```

### Linux

```shell
python3 juicenet.py "path/to/directory/with/files"
```

### help

```console
> python .\juicenet.py --help
Usage: juicenet.py [-h] [--public] [--nyuu] [--parpar] [--raw] [--skip-raw] [--match] [--pattern [*/ ...]] [--debug] [--move] [--exts [mkv mp4 ...]] path

Crude CLI tool to upload files to Usenet using Nyuu and ParPar

Positional Arguments:
  path                  Directory containing your files

Options:
  -h, --help            show this help message and exit
  --public              Use your public config
  --nyuu                Only run Nyuu
  --parpar              Only run ParPar
  --raw                 Only repost raw articles
  --skip-raw            Skip reposting raw articles
  --match               Enable pattern matching mode
  --pattern [*/ ...]    Specify the glob pattern(s) to be matched in pattern matching mode
  --debug               Show logs
  --move                Move files into their own directories. This will move foobar.ext to foobar/foobar.ext
  --exts [mkv mp4 ...]  Look for these extensions in <path> (ignores config)
```
