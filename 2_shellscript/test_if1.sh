#!/bin/bash
echo '======if单分支======'
A=12
echo 'A='${A}

if [ ${A} -gt 0 ]; then
	echo '大于0'
fi

echo '======if双分支======'
if [ $((A % 2)) -eq 0 ]; then
	echo '是偶数'
else
	echo '是奇数'
fi

echo '======if多分支======'
AGE=25
echo 'AGE='${AGE}

if [ ${AGE} -lt 18 ]
then
	echo '未成年'
elif [ ${AGE} -lt 60 ]
then
	echo '成年人'
else
	echo '老年人'
fi

echo '=====if判断文件是否存在====='

if [ $# -eq 0 ]
then
	echo '请输入文件目录'
elif [ -f $1 ]
then
	echo '文件的大小是'
	du -hs $1
elif [ -d $1 ]
then
	echo '目录的大小是'
	du -hs $1
else
	echo '文件或目录不存在'
fi
