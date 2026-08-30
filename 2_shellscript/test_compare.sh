#!/bin/bash
echo '====test比较整数值===='

A=12
B=5
echo ${A}
echo ${B}

echo 'test ${A} -gt ${B}的结果: '
test ${A} -gt ${B} 
echo ${?}
echo 'test ${A} -lt ${B}的结果: '
test ${A} -lt ${B} 
echo ${?}
echo 'test ${A} -eq ${B}的结果: '
test ${A} -eq ${B}
echo ${?}

echo '====[]比较整数值===='
echo '[ ${A} -gt ${B} ]的结果: '
[ ${A} -gt ${B} ]
echo ${?}
echo '[ ${A} -lt ${B} ]的结果: '
[ ${A} -lt ${B} ]
echo ${?}
echo '[ ${A} -eq ${B} ]的结果: '
[ ${A} -eq ${B} ]
echo ${?}

echo '====[]比较字符串===='
A="hello"
B="world"
echo 'A='${A}
echo 'B='${B}

echo '[ ${A} \> ${B} ]的结果: '
[ ${A} \> ${B} ]
echo ${?}
echo '[ ${A} = ${B} ]的结果: '
[ ${A} = ${B} ]
echo ${?}
echo '[ -n ${A} ]的结果: '
[ -n ${A} ]
echo ${?}
