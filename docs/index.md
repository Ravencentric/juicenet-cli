<br/>
<p align="center">
  <a href="https://github.com/Ravencentric/juicenet-cli">
    <img src="https://em-content.zobj.net/source/twitter/376/beverage-box_1f9c3.png" alt="Logo" width="100" height="100">
  </a>

  <h3 align="center">juicenet</h3>

  <p align="center">
    CLI tool designed to simplify the process of uploading files to usenet
    <br/>
    <br/>
  </p>
</p>

<p align="center">
<a href="https://pypi.org/project/juicenet-cli/"><img src="https://img.shields.io/pypi/v/juicenet-cli?link=https%3A%2F%2Fpypi.org%2Fproject%2Fjuicenet-cli%2F" alt="PyPI - Version"></a>
<img src="https://img.shields.io/pypi/pyversions/juicenet-cli" alt="PyPI - Python Version">
<img src="https://img.shields.io/github/actions/workflow/status/Ravencentric/juicenet-cli/release.yml" alt="GitHub Workflow Status (with event)">
<img src="https://img.shields.io/github/license/Ravencentric/juicenet-cli" alt="License">
<img src="https://www.mypy-lang.org/static/mypy_badge.svg" alt="Checked with mypy">
<img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
</p>


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

## License

Distributed under the [Unlicense](https://choosealicense.com/licenses/unlicense/) License. See [UNLICENSE](https://github.com/Ravencentric/juicenet-cli/blob/main/UNLICENSE) for more information.
