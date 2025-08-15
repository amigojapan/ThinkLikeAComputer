#!/usr/bin/bash
sed -e 's/TALC\.globals//g; s/globals//g; s/\.//g;s/TLAC//g; s/globals\.//g; 1,8d' problem4-program.py > problem4-program-simplified.py