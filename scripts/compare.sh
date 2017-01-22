#!/bin/bash
for i in $*; do
    echo "Comparing $i out/$i"
    diff -u out/$i $i
done
