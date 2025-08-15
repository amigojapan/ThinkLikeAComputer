#!/usr/bin/bash
sed -e 's/TALC\.globals//g; s/globals//g; s/\.//g;s/TLAC//g; s/globals\.//g; 1,8d' problem4-program.py > problem4-program-simplified.py
sed -e 's/,//g; s/TALC\.globals//g; s/globals//g; s/\.//g;s/TLAC//g; s/globals\.//g; 1,8d' problem5-program.py > problem5-program-simplified.py
sed -e 's/,//g; s/TALC\.globals//g; s/globals//g; s/\.//g;s/TLAC//g; s/globals\.//g; 1,8d' problem6-program.py > problem6-program-simplified.py
sed -e 's/,//g; s/TALC\.globals//g; s/globals//g; s/\.//g;s/TLAC//g; s/globals\.//g; 1,8d' problem7-program.py > problem7-program-simplified.py
sed -e 's/,//g; s/TALC\.globals//g; s/globals//g; s/\.//g;s/TLAC//g; s/globals\.//g; 1,8d' problem8-program.py > problem8-program-simplified.py