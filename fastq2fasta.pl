#!/usr/bin/env perl -w
my $file = "";
my $rm = 0;
if($ARGV[0] =~ m/(.*)\.gz$/){
	$file = "temp.fastq";
	$rm = 1;
	system("gunzip -c $ARGV[0] > $file");
}elsif( $ARGV[0] =~ m/(.*)\.zip$/){
	$file = "temp.fastq";
	$rm = 1;
	system("unzip -p $ARGV[0] > $file");
}elsif(! -f $ARGV[0]){
	die("$ARGV[0] is not a file!\n");
}else{
	$file = $ARGV[0];
}
open FH1, $file;
open FH2, "> $ARGV[1]";
while(<FH1>){
	s/^\@/>/;
	print FH2;
	print FH2  scalar  <FH1>;
	<FH1>;
	<FH1>;
}

close FH1;
close FH2;

if( $rm == 1  && -f $file){
	system("rm $file");
}
