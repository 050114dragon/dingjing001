#!/usr/bin/perl -w
#usage: perl $0 <seqid> <input> <out>
#pick sequence by sequence id from input fasta file, and out file format is fasta
open FH1,"< $ARGV[0]";
open FH2,"< $ARGV[1]";
open FH3,"> $ARGV[2]";
my @seqid;
while(<FH1>){
	chomp;
	push(@seqid,$_);
	}
close FH1;

my %hash;
while(<FH2>){
	chomp;
	my $a = $_;
	my $b = <FH2>;
	chomp $b;
	if($a =~ m/^>(\S+)\s*/){
		$hash{${1}} = $b;
		}
	}
close FH2;

foreach (@seqid){
	if( exists  $hash{$_}){
		print FH3 ">$_\n$hash{$_}\n";
		}
	}

close FH3;
