# -*- encoding: utf-8 -*-
'''
@File    :   family_size.py
@Time    :   2022/06/10 22:01:27
@Author  :   Shuilong Zhang 
@Version :   0.1.0
@Contact :   050114dragon@163.com
'''

import pysam
from collections import Counter,defaultdict
import re
import numpy as np
import pandas as pd
# import plotnine
import argparse
import os
import sys
import glob
import random
import pandas as pd
import openpyxl

def umi(bam,resample=0):
    umi_read = defaultdict(set)
    n = 0
    # bam = "/public/test_data/Multiplex_MRD/results/Topgen-20220602-L-01-2022-06-051530/umi/align/R22013066-DJHK20220602-IDT-0.1-10ng-6cy-1_combined.sorted.bam"
    samfile = pysam.AlignmentFile(filename=bam)
    fetchs = samfile.fetch()
    fetchs = list(fetchs)
    if resample > 0:
        print(resample)
        fetchs.sort(key=lambda x:x.query_name)
        print(len(fetchs))
        fetchs = fetchs[0:resample]
        for j in fetchs:
                n += 1
                dicts = j.to_dict()
                name = dicts["name"]
                tags = dict(j.tags)
                umi_read[tags["RX"]].add(name)
                if n > resample:
                    break
    else:
        for j in fetchs:
            dicts = j.to_dict()
            name = dicts["name"]
            tags = dict(j.tags)
            umi_read[tags["RX"]].add(name)
    samfile.close()
    return umi_read



def family_size(umis_read):
    umi_dedup_count = len(umis_read.keys())
    umi_count = 0
    for i in umis_read.values():
        umi_count = umi_count + len(i)
    family_size_mean = round(np.mean(umi_count/umi_dedup_count),3)
    return [umi_count,umi_dedup_count,family_size_mean]



def combine_file(input_dir,out_dir,out_file):
    with pd.ExcelWriter(os.path.join(out_dir,out_file),mode="w",engine="openpyxl") as writer:
        files = glob.glob(os.path.join(input_dir,"*.csv"))
        for i in files:
            df = pd.read_csv(i,header=0)
            df.to_excel(writer, sheet_name="Sheet1", index=False)


if __name__ == "__main__":
    parses = argparse.ArgumentParser(description="重采样，并计算family size mean")
    parses.add_argument("-i",type=str,help="输入文件或者目录",metavar="input",nargs="+",required=True)
    parses.add_argument("-d",action="store_true",help="指定input是目录")
    parses.add_argument("-o",type=str,help="输出文件",metavar="outfile",required=True)
    parses.add_argument("--out_dir",type=str,help="输出目录",metavar="out_dir",required=True)
    parses.add_argument("--resample",type=int,help="重采样深度,默认值为0,表示不进行重采样",metavar="resample_depth",default=0)
    args = parses.parse_args()
    print(args)
    out_dir=args.out_dir
    out_file=args.o
    if args.d == False:
        # /public/test_data/Multiplex_MRD/results/202205280209/umi/align/0524-A-WTa-1_S1.sorted.bam
        with open("temp_family_size.csv","w") as f:
            f.write("sampleID,tumi_count,umi_dedup_count,family_size_mean\n")
            for i in args.i:
                sampleID = re.sub(r"(\.sorted)?\.bam","",os.path.basename(os.path.realpath(i)))
                print(sampleID)
                umis_read = umi(bam=i,resample=args.resample)
                result = family_size(umis_read)
                f.write(sampleID + "," +  (",".join([str(j) for j in result])) + "\n")
        with pd.ExcelWriter(os.path.join(out_dir,out_file),mode="w",engine="openpyxl") as writer:
            df = pd.read_csv("temp_family_size.csv",header=0)
            df.to_excel(writer, sheet_name="Sheet1", index=False)
        os.remove("temp_family_size.csv")
    else:
        for i in args.i:
            # /public/test_data/Multiplex_MRD/results/202205280209
            batch = os.path.basename(os.path.realpath(i))
            print(batch)
            with open(os.path.join(out_dir,"{}.csv".format(batch)),"w") as f:
                f.write("batch,sampleID,umi_count,umi_dedup_count,family_size_mean\n")
                bams = glob.glob(os.path.join(os.path.realpath(i),"umi","align","*sorted.bam")) 
                for j in bams:
                    sampleID=os.path.basename(re.sub(r"(\.sorted)?\.bam","",j))
                    print(sampleID)
                    # if re.match("N",sampleID) or sampleID == "Topgen-20220601-L-01-2022-06-041338,R22012941-DJHK20220601-N5_combined":
                    #     continue
                    umis_read = umi(bam=j,resample=args.resample)
                    result = family_size(umis_read)
                    f.write(batch + "," + sampleID + "," +  (",".join([str(j) for j in result])) + "\n")
        combine_file(input_dir=out_dir,out_dir=out_dir,out_file=out_file)
        os.system("rm {}/*.csv".format(out_dir))             
    print("analysis complete")


    
    
    
