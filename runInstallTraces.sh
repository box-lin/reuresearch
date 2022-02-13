#!/bin/bash
for file in $1/*;
do
    python install_classify.py $file
    echo "==================================================="
    echo ""
done