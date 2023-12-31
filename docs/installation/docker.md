# Docker Installation

`juicenet` is available as a docker image on both [Docker Hub](https://hub.docker.com/r/ravencentric/juicenet-cli) and [ghcr.io](https://github.com/Ravencentric/juicenet-cli/pkgs/container/juicenet-cli).


=== "Docker Hub"

    ``` shell
    docker pull ravencentric/juicenet-cli
    ```

=== "ghcr"

    ``` shell
    docker pull ghcr.io/ravencentric/juicenet-cli
    ```

### `docker-compose.yml`

``` yaml
--8<--
docker-compose.yml
--8<--
```

!!! note
    The value of `dump-failed-posts` in your [nyuu config](../nyuu-config-files.md) must match the compose file, i.e, it must be set to `/data/raw`

    ``` json title="nyuu-config.json"
    "dump-failed-posts":  "/data/raw"
    ```

!!! note
    To keep things simple, this image requires a secondary config. If you aren't planning to use a secondary config, you can simply reuse the primary config again.

### Usage

After you're done copying the `docker-compose.yml` and editing the host paths to match yours, you can run `juicenet` with the following command:

``` shell
docker compose -f "path/to/docker-compose.yml" run juicenet --help
```

### Available Tags

!!! note
    Docker images are only available for `v0.30.0`+

| Tag           | Description                                                                                                  |
|---------------|--------------------------------------------------------------------------------------------------------------|
| `latest`      | [Latest stable release](https://github.com/Ravencentric/juicenet-cli/releases/latest) (default)              |
| `main`        | [Latest commit in the `main` branch](https://github.com/Ravencentric/juicenet-cli/commits/main)              |
| `X.Y.Z`       | Specific release, for example, [`0.30.0`](https://github.com/Ravencentric/juicenet-cli/releases/tag/v0.30.0) |
| `X.Y`         | Latest release in the specified major and minor version                                                      |
| `sha-ed9e6ff` | Specific git commit identified by its unique short SHA                                                       |

### Defaults

This image ships with the following default configuration:

``` yaml
--8<--
config/juicenet.docker.yaml
--8<--
```

Having a default configuration for values which most likely will not change simplifies the setup for most people. If you do need to override it, you can do so by mounting `host/path/to/your/juicenet.docker.yaml:/config/juicenet.docker.yaml` in your `docker-compose.yml`

!!! tip
    If you want to match extensions other than the default `mkv`, use the `--exts` option in the CLI

!!! note
    You can read about the configuration file [here](../configuration.md)