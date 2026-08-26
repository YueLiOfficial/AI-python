#!/bin/bash

if read -t 10 -p '请输入姓名 年龄 城市: ' name age city
then
	echo "${name}的年龄是${age}, 居住在${city}"
else
	echo "超时未输入"
fi

echo '====读文件===='
while read line
do
	echo "行内容: ${line}"
done < ${1}
