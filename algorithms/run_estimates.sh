#!/bin/bash
while getopts d:k:n:i: flag
do
    case "${flag}" in
        d) d=${OPTARG};;
        k) k=${OPTARG};;
        n) n=${OPTARG};;
        i) i=${OPTARG};;
    esac
done

echo "t1,t2,d,k,approximation,fpt,approximation_time,fpt_time"

for x in $(seq 1 1 $i)
do
   /usr/bin/python3 estimate.py -n $n -d $d -k $k
done