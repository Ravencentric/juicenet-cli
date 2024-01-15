FROM nikolaik/python-nodejs:python3.12-nodejs20

ENV LANG C.UTF-8
USER pn

WORKDIR /node

RUN sudo npm install -g yencode
RUN sudo npm install -g git+https://github.com/animetosho/Nyuu.git --production --unsafe-perm
RUN sudo npm install -g @animetosho/parpar

WORKDIR /app

COPY . .
COPY ./config/juicenet.docker.yaml /config/juicenet.docker.yaml

RUN pip install .

WORKDIR /media

ENTRYPOINT ["python", "-m", "juicenet", "--config", "/config/juicenet.docker.yaml"]
