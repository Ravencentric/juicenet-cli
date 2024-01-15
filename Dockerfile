FROM nikolaik/python-nodejs:python3.12-nodejs20

# 1000:1000
USER pn

ENV LANG=C.UTF-8

# https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md#global-npm-dependencies
ENV NPM_CONFIG_PREFIX=/home/pn/.npm-global
ENV PATH=$PATH:/home/pn/.npm-global/bin

# This is where pip install goes
ENV PATH=$PATH:/home/pn/.local/bin

WORKDIR /node

RUN npm install -g yencode
RUN npm install -g git+https://github.com/animetosho/Nyuu.git --omit=dev --unsafe-perm
RUN npm install -g @animetosho/parpar

WORKDIR /app

COPY . .
COPY ./config/juicenet.docker.yaml /config/juicenet.docker.yaml

RUN pip install .

WORKDIR /media

ENTRYPOINT ["python", "-m", "juicenet", "--config", "/config/juicenet.docker.yaml"]
