# CLI Reference

## Usage

```console
$ juicenet [OPTIONS] <path>
```
```console
$ juicenet <path> [OPTIONS]
```
```console
$ juicenet [OPTIONS] <path> [OPTIONS]
```

## Options

| Positional Arguments    | Description                                                                                   |
|-------------------------|-----------------------------------------------------------------------------------------------|
| `path`                  | Directory containing your files (default: CWD)                                                |

| Options:                | Description                                                                                   |
| ----------------------- | ----------------------------------------------------------------------------------------------|
| `-h, --help`            | Show this help message and exit                                                               |
| `--config CONFIG`       | Specify the path to your juicenet config file                                                 |
| `--version`             | Print juicenet version                                                                        |
| `--public`              | Use your public config                                                                        |
| `--nyuu`                | Only run Nyuu                                                                                 |
| `--parpar`              | Only run ParPar                                                                               |
| `--raw`                 | Only repost raw articles                                                                      |
| `--skip-raw`            | Skip reposting raw articles                                                                   |
| `--glob    [*/ ...]`    | Specify the glob pattern(s) to be matched instead of extensions                               |
| `--debug`               | Show logs for debugging purposes                                                              |
| `--move`                | Move files into their own directories `(foobar.ext -> foobar/foobar.ext)` before processing   |
| `--only-move`           | Same as `--move` except it immediately exists after it's done moving                          |
| `--exts [mkv mp4 ...]`  | Look for these extensions in `<path>`                                                         |
| `--no-resume`           | ignore resume data                                                                            |
| `--clear-resume`        | delete resume data                                                                            |

## Examples

1. Uploading the files in current working directory with config passed via the environment variable `JUICENET_CONFIG`

    ``` bash
    juicenet
    ```
    Yep, that's it. That'll do the rest for you.

2. Upload files from an arbitrary directory with an explicit config

    ``` bash
    juicenet --config "path/to/juicenet.yaml" "path/to/files"
    ```

3. Specify arbitrary extensions at runtime, ignoring the extensions defined in config

    ``` bash
    juicenet --exts mp4 epub # CWD
    ```
    
    ``` bash
    juicenet "path/to/files" --exts mp4 epub
    ```

4. Upload all subfolders while preserving their structure

    ``` bash
    juicenet --glob "*/" # CWD
    ```

    ``` bash
    juicenet "path/to/files" --glob "*/"
    ```

5. Upload all subfolders with the word "BDMV" and "UHD" in it while preserving their structure

    ``` bash
    juicenet --glob "*BDMV*/" "*UHD*/" # CWD
    ```

    ``` bash
    juicenet "path/to/files" --glob "*BDMV*/" "*UHD*/"
    ```

6. Only Upload E10 to E15 from a folder with all the episodes

    ``` bash
    juicenet --glob "S01E1[0-5]" # CWD
    ```

    ``` bash
    juicenet "path/to/files" --glob "S01E1[0-5]"
    ```
