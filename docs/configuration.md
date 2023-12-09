# Configuration

Before you can use `juicenet`, you'll have to configure it. This is a one time thing after which you can pretty much forget about it.

## juicenet.yaml

`juicenet` requires you to put your configuration in a file called `juicenet.yaml`. Below is an example `juicenet.yaml` which you can copy and edit:

``` yaml
--8<--
config/juicenet.yaml
--8<--
```

## Loading the config file

Now that you've got your `juicenet.yaml` ready, you have to pass it to `juicenet`. This can be achieved in one of three ways:

- Using the command-line argument

    ```console
    juicenet --config "path/to/juicenet.yaml" [OPTIONS] <path>
    ```

- Setting an environment variable named `JUICENET_CONFIG` with the full path to your `juicenet.yaml`. If you do this, it'll never fall back to using `juicenet.yaml` from current working directory. This is also convenient since you no longer have to pass `--config` everytime.
- Placing the configuration file in the current working directory as `juicenet.yaml`

!!! note
    The order of precedence, if all three are present, is: `command-line argument` > `environment variable` > `local file in the current working directory`