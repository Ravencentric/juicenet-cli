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

!!! note
    To keep things simple, this image requires a secondary config. If you aren't planning to use a secondary config, you can simply reuse the primary config again.

### Usage

After you're done copying the `docker-compose.yml` and editing the host paths to match yours, you can run `juicenet` with the following command:

``` shell
docker compose -f "path/to/docker-compose.yml" run juicenet --help
```

### Available Tags

| Tag      | Description                                                                           |
|----------|---------------------------------------------------------------------------------------|
| `latest` | [Latest stable release](https://github.com/Ravencentric/juicenet-cli/releases/latest) |
| `main`   | [Latest git commit](https://github.com/Ravencentric/juicenet-cli/commits/main)        |

### Defaults

This image ships with the following default configuration:

``` yaml
--8<--
config/juicenet.docker.yaml
--8<--
```

Having a default configuration for values which most likely will not change simplifies the setup for most people. If you do need to override it, you can do so by mounting `host/path/to/your/juicenet.docker.yaml:/config/juicenet.docker.yaml` in your `docker-compose.yml`

!!! note
    You can read about the configuration file [here](../configuration.md)