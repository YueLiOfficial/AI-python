!/bin/bash
echo '====2选1===='
echo '[ 条件判断 && 结果1 || 结果2 ]'
A=12
B=5
echo 'A='${A}
echo 'B='${B}

[ ${A} -gt ${B} ] && echo 最大值是${A} || echo 最大值是${B}

echo '====多个条件===='
echo '-a且, -o或, &&且, ||或'

[ ${A} -gt 0 ] && [ ${A} -lt 100 ] && echo ${A}满足大于0且小于100 || echo ${A}不满足大于0且小于100
