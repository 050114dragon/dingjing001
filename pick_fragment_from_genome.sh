#!/usr/bin/bash
#usage: bash $0 <input> <out> <genome version>

if [ $# -ne 3 ];then
	echo "Error: argument number is wrong!"
	echo "usage: bash $0 <input> <out> <genome version>"
	exit 1
fi

if [ -f $2 ];then
	rm $2
else
	touch $2
fi

genome_version=$3


if [ $genome_version == "hg19" ];then
	index=/public/home/zhangshuilong/database/ucsc_hg19/ucsc_hg19.fasta
elif [ $genome_version == "hg38" ];then
	index=/public/home/zhangshuilong/database/ucsc_hg19/ucsc_hg38.fasta
fi

if [ ! -f $index ];then
	echo "Error: index file is not exists!"
	exit 1	
fi

if [ ! -f `realpath $index`.fai ];then
	echo "creating index, please be patient!"
	samtools faidx $index --fai-idx `realpath $index`.fai
fi


while read line
	do
	region=`echo -e "$line" | perl -n -e 'chomp; if(m/^(chr[0-9a-zA-Z]+)\t(\d+)\t(\d+)/i){print lc($1) . ":" . $2 . "-" . $3;}elsif(m/^chr[0-9a-zA-Z]+:\d+-\d+/i){print lc($_)}else{die "error: "}'`	
	if [ $? -ne 0 ];then
		echo "$line:" "input file format is wrong!" 
		rm $2
		exit 1
	else
		samtools faidx $index "$region" >> $2
		
	fi
	done < $1
	mv $2 temp.txt
	perl /public/home/zhangshuilong/bin/fasta_format.pl temp.txt  $2 && rm temp.txt
