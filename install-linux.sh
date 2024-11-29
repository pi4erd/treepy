#!/bin/sh

CURRENT_VERSION=0.1.2
INSTALL_DIR=/usr/local/bin

./build.sh # build

tar -xf dist/treepy-$CURRENT_VERSION.tar.gz -C /tmp
echo "Unpacked into /tmp/treepy-$CURRENT_VERSION"
echo "Installing executable to $INSTALL_DIR/treepy. Requesting permissions..."
sudo install /tmp/treepy-$CURRENT_VERSION/src/tree.py $INSTALL_DIR/treepy
