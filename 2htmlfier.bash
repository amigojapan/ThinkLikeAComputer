#!/usr/bin/bash
sed -e 's/    /<img src\=\"TLAC_boardgame\/img\/HTMLstuff\/block.png\"\>/g; s/$/<BR>/g' problem4-program-simplified.py > p4html.html