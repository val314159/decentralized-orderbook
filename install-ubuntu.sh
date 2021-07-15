set -ex
(
    export DEBIAN_FRONTEND=noninteractive
    apt-get -y update && apt-get -y upgrade
    apt-get -y install apt-utils sudo wget curl tree telnet xz-utils make
    yes | adduser val
    adduser val sudo
    adduser val root
    echo "val:valxlav"|chpasswd
    #echo  "root:toor"|chpasswd

    export SOLCV=v0.8.6
    wget https://github.com/ethereum/solidity/releases/download/${SOLCV}/solc-static-linux
    mv solc-static-linux /usr/local/bin/solc
    chmod +x /usr/local/bin/solc

    export NODEV=v14.17.2
    export NODE=${NODEV}-linux-x64
    (cd /usr/local ; curl https://nodejs.org/dist/${NODEV}/node-${NODE}.tar.xz | xzcat | tar xv ; ln -s node-${NODE} node)
    (cd /usr/local/bin ; ln    /usr/local/node/bin/node ;
     ln -s /usr/local/node/lib/node_modules/npm/bin/npm-cli.js npm
     ln -s /usr/local/node/lib/node_modules/npm/bin/npx-cli.js npx)
    npm i -g ganache-cli

    #apt-get -y install docker.io && adduser val docker

    apt-get -y install python3-pip python3-bottle python3-docopt python3-gevent-websocket
    (cd /usr/local/lib/python3.9/dist-packages/ ;
     wget https://raw.githubusercontent.com/circleclick-labs/kista/main/kista.py)
    mv kista.py /usr/local/lib/python3.9/dist-packages/
    #cp kista.py /usr/local/lib/python3.9/dist-packages/
    pip3 install web3
    #pip3 install web3 ethpm-cli solc py-solc
    apt-get -y autoremove
    rm install-ubuntu.sh
)
