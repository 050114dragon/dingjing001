#!/usr/bin/perl -w
#perl fasta_format.pl <input> <out>
#每条read对应的序列位于多行，使用此脚本，使每条read对应的序列合并为一行
open FH1,"< $ARGV[0]";
open FH2,"> $ARGV[1]";
print FH2 scalar <FH1>;
while(<FH1>){	
	chomp;
	if(m/^>/){
		print FH2 "\n",$_,"\n";
		}else{
		print FH2 "$_";
		}
	}
print FH2 "\n";
	
	
