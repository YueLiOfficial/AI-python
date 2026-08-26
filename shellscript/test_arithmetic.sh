#!/bin/bash

echo '====算术运算===='
echo '==$((整数表达式))=='
echo '1+1'=$((1+1))

A=9
B=6
echo 'A='${A}
echo 'B='${B}
echo 'A+B='$((A+B))
echo 'A-B='$((A-B))
echo 'A*B='$((A*B))
echo 'A/B='$((A/B))
echo 'A%B='$((A%B))
echo 'A++结果: '$((A++))
echo '++A结果: '$((++A))
echo 'A='${A}
echo 'A+=1结果: '$((A+=1))
echo 'A='$((A))

