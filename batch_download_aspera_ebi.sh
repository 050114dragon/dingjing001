#!/usr/bin/bash
#usage: bash $0 <url file>
#url file contain a ftp path each line
#requirement: aspera-connect,sratoolkit

dos2unix $1

if [ -f success_sample.txt ];then
	#下载成功文件的列表
	rm success_sample.txt
	touch success_sample.txt 
fi

if [ -f fail_sample.txt ];then
	#下载失败文件的列表
	rm fail_sample.txt 
	touch fail_sample.txt
fi



cat $1 | while read line
do
	url=`echo $line | perl -n -e 'chomp;s#ftp\.sra\.ebi\.ac\.uk#era-fasp\@fasp.sra.ebi.ac.uk:#;print $_'`
	echo $url
	sample=`echo $url | perl -n -e 'chomp;my $sample=(split "_",(split "/",$_)[-1])[0];print("$sample")'`
	echo $sample
	ascp -QT -l 300m -P33001 -i /public/home/zhangshuilong/.aspera/connect/etc/asperaweb_id_dsa.openssh \
$url ./
	#-i <key file>, a key file created after aspera-connect was installed
	if [ $? -eq 0 ];then
		if [ -f ${sample}_1.fastq.gz ];then
			mv ${sample}_1.fastq.gz ${sample}_R1.fastq.gz
		fi
		if [ -f ${sample}_2.fastq.gz ];then
			mv ${sample}_2.fastq.gz ${sample}_R2.fastq.gz
		fi
		echo $line >> success_sample.txt
	else
		rm $sample
		echo $line >> fail_sample.txt
	fi
	echo "$sample complete"
done
	echo "all complete"

