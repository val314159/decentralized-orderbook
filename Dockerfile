#-*-mode:Dockerfile-*-
FROM ubuntu:21.04
ENV DEBIAN_FRONTEND=noninteractive
ENV SOLCV=v0.8.6
ENV NODE=v14.17.2
ENV URL1=https://github.com/ethereum/solidity/releases/download/${SOLCV}/solc-static-linux
ENV URL2=https://nodejs.org/dist/${NODE}/node-${NODE}-linux-x64.tar.xz
ENV URL3=https://raw.githubusercontent.com/circleclick-labs/kista/main/kista.py
ENV URL4=https://github.com/circleclick-labs/kista/

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install apt-utils sudo wget curl tree xz-utils
RUN yes | adduser val && adduser val sudo && adduser val root && echo "val:x"|chpasswd

RUN (cd /usr/local/bin && wget ${URL1} && mv solc-static-linux solc && chmod +x solc)

RUN (cd   /usr/local ; curl ${URL2} | xzcat | tar xv ; ln -s node-${NODE}-linux-x64 node) \
 && (cd   /usr/local/bin \
 && ln    /usr/local/node/bin/node \
 && ln -s /usr/local/node/lib/node_modules/npm/bin/npm-cli.js npm \
 && ln -s /usr/local/node/lib/node_modules/npm/bin/npx-cli.js npx \
 && npm i -g ganache-cli)

#RUN apt-get -y install docker.io && adduser val docker

RUN apt-get -y install python3-pip python3-bottle python3-docopt python3-gevent-websocket \
 && pip3 install web3

#RUN (cd /usr/local/lib/python3.9/dist-packages/ && wget ${URL2})

RUN apt-get -y install git make telnet

RUN mkdir qq && (cd qq ; git clone ${URL4} && cd kista && pip install .) && rm -fr qq

RUN apt-get -y install emacs-nox

RUN apt-get -y install screen

RUN pip3 install web3 ethpm-cli solc py-solc

RUN apt-get -y autoremove

#ENV URL0=https://github.com/ethereum/solidity/releases/download/v0.4.25/solc-static-linux
#RUN (cd /usr/local/bin && wget ${URL0} && mv solc-static-linux solc-0.4.25 && chmod +x solc-0.4.25)

ENV URL9=https://github.com/ethereum/solidity/releases/download/v0.6.0/solc-static-linux
RUN (cd /usr/local/bin && wget ${URL9} && mv solc-static-linux solc-0.6.0 && chmod +x solc-0.6.0)

EXPOSE 8545
WORKDIR /home/val
USER val
