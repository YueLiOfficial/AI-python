#!/bin/bash

check_age() {
	if [ ${1} -ge 0 ] && [ ${1} -le 150 ]
	then
		echo "年龄校验成功"
		return 0
	else
		echo "年龄校验失败"
		return 1
	fi
}

read -p "请输入年龄: " age

check_age ${age}

echo ${?}
