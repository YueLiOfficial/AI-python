#!/bin/bash

sum() {
	SUM=$((${1} + ${2}))
	echo ${SUM}
}

read -p "请输入第一个参数: " a
read -p "请输入第二个参数: " b

res=$(sum ${a} ${b})
if [ ${res} -gt 0 ]
then
	echo "和是正数"
fi
