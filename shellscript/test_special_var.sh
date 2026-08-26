#!/bin/bash
echo '=========$n========='
echo 脚本文件名称: ${0}
echo 第一个参数: ${1}
echo 第二个参数: ${2}
echo 第三个参数: ${3}
echo '=========$#========='
echo 输入的参数个数: ${#}
echo '=========$*========='
echo 所有输入参数${*}
echo '=========$@========='
echo 所有输入参数${@}
echo '======双引号$*======'
for i in "$*"
do
	echo "${i}"
done

echo '======双引号$@======'
for j in "$@"
do
	echo "${j}"
done

echo '=========$?========='
ls /root
echo 'ls /root执行结果: '${?}
ls ./
echo 'ls ./执行结果: '${?}

echo '=========$$========='
echo 当前Shell进程的PID: ${$}

echo '=========$!========='
sleep 10 & echo 上一个sleep进程的PID: ${!}
