#!/bin/bash

case $1 in
	1) echo 'Monday';;
	2) echo 'Tuesday';;
	3) echo 'wendnesday';;
	4) echo 'Thursday';;
	5) echo 'Friday';;
	6) echo 'Saturday';;
	7) echo 'Sunday';;
	*) echo '请输入数字[1, 7]';;
esac
