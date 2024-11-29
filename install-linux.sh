#!/bin/sh

CURRENT_VERSION=0.1.2

./build.sh # build

tar -xf dist/treepy-$CURRENT_VERSION.tar.gz -C /tmp
echo "Unpacked into /tmp/treepy-$CURRENT_VERSION"
echo "Copying executable to /usr/local/bin/treepy. Requesting permissions..."
sudo cp /tmp/treepy-$CURRENT_VERSION/src/tree.py /usr/local/bin/treepy
