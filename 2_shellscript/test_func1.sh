#!/bin/bash

sum() {
	SUM=$((${1} +${2}))
	echo ${SUM}
}

read -p "请输入第一个参数: " a
read -p "请输入第二个参数: " b

sum ${a} ${b}
