#!/bin/bash
echo '====for语句1===='
for ((i=1; i<=10; i++))
do
	echo ${i}
done

echo '====for语句2===='
for S in "$@"
do
	echo ${S}
done
