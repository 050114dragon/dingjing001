#!/usr/bin/bash

function test_sentieon(){
	if [ -f $logfile ];then
		rm $logfile
	fi
	$sentieon  licclnt ping --server $sentieon_license
	if [ $? -ne 0 ];then
		zmail "${message}"
		if [ $? -ne 0 ];then
			echo "sentieon license can not access!" > $logfile
		else
			echo "sentieon license can not access and error info have send to email!" > $logfile
		fi
		exit 1
	else
		echo "sentieon license ok"
	fi
}

function zmail(){
	ssh `whoami`@admin <<-hehe
	python /public/home/zhangshuilong/bin/zmail_test_sentieon.py "${1}"
	hehe
}



sentieon=""   #sentieon path
sentieon_license=""  #sentieon_license
export SENTIEON_LICENSE=${sentieon_license}

logfile=log.txt
message="sentieon license can not access!"

test_sentieon

echo "end"
