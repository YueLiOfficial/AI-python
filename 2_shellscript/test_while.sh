#!/bin/bash
echo '====while从1加到100===='

i=1
total=0
while [ ${i} -le 100 ]
do
	((total+=i))
	((i++))
done

echo ${total}
