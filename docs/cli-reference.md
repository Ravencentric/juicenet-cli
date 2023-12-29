# CLI Reference

## Usage

``` shell
$ juicenet [OPTIONS] <path>
```
``` shell
$ juicenet <path> [OPTIONS]
```
``` shell
$ juicenet [OPTIONS] <path> [OPTIONS]
```

## Options

| Positional Arguments    | Description                                                                                   |
|-------------------------|-----------------------------------------------------------------------------------------------|
| `path`                  | Directory containing your files (default: CWD)                                                |

| Options:                | Description                                                                                   |
| ----------------------- | ----------------------------------------------------------------------------------------------|
| `-h, --help`            | Show a help message and exit                                                                  |
| `--config CONFIG`       | Specify the path to your juicenet config file                                                 |
| `--version`             | Print juicenet version                                                                        |
| `--public`              | Use your public config                                                                        |
| `--nyuu`                | Only run Nyuu in `<path>` (default: `cwd`)                                                    |
| `--parpar`              | Only run ParPar in `<path>` (default: `cwd`)                                                  |
| `--raw`                 | Only repost raw articles                                                                      |
| `--skip-raw`            | Skip reposting raw articles                                                                   |
| `--glob    [*/ ...]`    | Specify the glob pattern(s) to be matched instead of extensions                               |
| `--bdmv`                | Find and upload BDMV discs in cwd, can be used with `--glob`                                  |
| `--debug`               | Show logs for debugging                                                                       |
| `--move`                | Move files into their own directories `(foobar.ext -> foobar/foobar.ext)` before processing   |
| `--only-move`           | Same as `--move` except it immediately exists after it's done moving                          |
| `--exts [mkv mp4 ...]`  | Look for these extensions in `<path>`                                                         |
| `--no-resume`           | ignore resume data                                                                            |
| `--clear-resume`        | delete resume data                                                                            |

!!! info
    If you don't feel like using `--config` every single time, you can use the environment variable `JUICENET_CONFIG` to hold the path of your config file. If set, this will always be used unless overridden by explicitly passing `--config`.

## Examples

!!! info
    `juicenet` will automatically preserve structure for all folder uploads and discard them for singular files.


1. Uploading the files in current working directory with config passed via the environment variable `JUICENET_CONFIG`

    ``` bash
    juicenet
    ```
    Yep, that's it. That'll do the rest for you.

2. Upload a single file

    ```bash
    juicenet "path/to/file.mkv" # config loaded from $JUICENET_CONFIG
    ```

    ```bash
    juicenet --config "path/to/juicenet.yaml" "path/to/file.mkv"
    ```

3. Upload files from an arbitrary directory with an explicit config

    ``` bash
    juicenet --config "path/to/juicenet.yaml" "path/to/files"
    ```

4. Specify arbitrary extensions at runtime, ignoring the extensions defined in config

    ``` bash
    juicenet --exts mp4 epub # CWD
    ```
    
    ``` bash
    juicenet "path/to/files" --exts mp4 epub
    ```

5. Upload all subfolders in `<path>`

    ``` bash
    juicenet --glob "*/" # CWD
    ```

    ``` bash
    juicenet "path/to/files" --glob "*/"
    ```
    
    !!! info
        Linux shells automatically expand the glob pattern before passing it to the command, quote the glob pattern to stop the expansion since we want `juicenet` to read those glob patterns.

6. Upload all subfolders with the word "BDMV" anywhere in their name and all the subfolders that start with the word "UHD"

    ``` bash
    juicenet --glob "*BDMV*/" "UHD*/" # CWD
    ```

    ``` bash
    juicenet "path/to/files" --glob "*BDMV*/" "*UHD*/"
    ```

7. Find and upload BDMV discs in current working directory automatically

    !!! note
        This may not be perfect, it simply finds BDMVs by looking for `BDMV/index.bdmv`

    ``` bash
    juicenet "path/to/files" --bdmv
    ```
    Can be paired with `--glob` to further filter what you want to upload. For example, if you only want to find BDMV discs in folders that have the word "BDMV" and "UHD" in them, you would run the following command

    ``` bash
    juicenet "path/to/files" --bdmv --glob "*BDMV*/" "*UHD*/"
    ```

8. Only Upload E10 to E15 from a folder with all the episodes

    ``` bash
    juicenet --glob "S01E1[0-5]" # CWD
    ```

    ``` bash
    juicenet "path/to/files" --glob "S01E1[0-5]"
    ```
