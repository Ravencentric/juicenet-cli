# Configuration

Before you can use `juicenet`, you'll have to configure it. This is a one time thing after which you can pretty much forget about it.

## Reference

`juicenet` requires you to put your configuration in a file called `juicenet.yaml`.

### Required keys

| Key                 | Description                                                 |
| ------------------- | ----------------------------------------------------------- |
| NYUU_CONFIG_PRIVATE | Path to a valid Nyuu configuration file                     |
| NZB_OUTPUT_PATH     | Path to a directory where `juicenet` will store it's output |

### Optional keys

| Key                | Description                                                                                                                                                                                                            | Default                                                                             |
|--------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| PARPAR             | The path to the ParPar binary                                                                                                                                                                                          | `PATH`                                                                              |
| NYUU               | The path to the Nyuu binary                                                                                                                                                                                            | `PATH`                                                                              |
| NYUU_CONFIG_PUBLIC | The path to the public Nyuu configuration file                                                                                                                                                                         | `NYUU_CONFIG_PRIVATE`                                                               |
| EXTENSIONS         | The list of file extensions to be processed                                                                                                                                                                            | `["mkv"]`                                                                           |
| RELATED_EXTENSIONS | The list of file extensions associated with an input file. For example, if you have a file named `Big Buck Bunny The Movie (2023).mkv`, another file named `Big Buck Bunny The Movie (2023).srt` is considered related | ["*"]                                                                               |
| PARPAR_ARGS        | The arguments to be passed to the ParPar binary                                                                                                                                                                        | `--overwrite -s700k --slice-size-multiple=700K --max-input-slices=4000 -r1n*1.2 -R` |
| USE_TEMP_DIR       | Whether or not to use a temporary directory for processing                                                                                                                                                             | `True`                                                                              |
| TEMP_DIR_PATH      | Path to a specific temporary directory if USE_TEMP_DIR is True                                                                                                                                                         | `%Temp%` or `/tmp/`                                                                 |
| APPDATA_DIR_PATH   | The path to the folder where juicenet will store its data                                                                                                                                                              | `~/.juicenet`                                                                       |


### Example configuration file

``` yaml
--8<--
config/juicenet.yaml
--8<--
```

## Loading the config file

Now that you've got your `juicenet.yaml` ready, you have to pass it to `juicenet`. This can be achieved in one of three ways:

- Using the command-line argument

    ``` shell
    juicenet --config "path/to/juicenet.yaml" [OPTIONS] <path>
    ```

- Setting an environment variable named `JUICENET_CONFIG` with the full path to your `juicenet.yaml`. If you do this, it'll never fall back to using `juicenet.yaml` from current working directory. This is also convenient since you no longer have to pass `--config` everytime.
- Placing the configuration file in the current working directory as `juicenet.yaml`

!!! note
    The order of precedence, if all three are present, is: `command-line argument` > `environment variable` > `local file in the current working directory`