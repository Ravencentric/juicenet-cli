FROM nikolaik/python-nodejs:python3.12-nodejs20
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV LANG=C.UTF-8 \
    # See: https://github.com/Ravencentric/juicenet-cli/issues/75
    GYP_DEFINES="enable_native_tuning=0"

WORKDIR /node

RUN npm install -g yencode
RUN npm install -g nyuu --production
RUN npm install -g @animetosho/parpar

WORKDIR /app

COPY . .
COPY ./config/juicenet.docker.yaml /config/juicenet.docker.yaml

RUN uv sync --locked --compile-bytecode

WORKDIR /media

ENTRYPOINT ["uv", "run", "juicenet", "--config", "/config/juicenet.docker.yaml"]
