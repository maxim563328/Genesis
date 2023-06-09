# -*- coding: utf-8 -*-
"""Binomix_10.11.22.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WX521pgMmQW_H_pcuocKeQkkZIx_bmrO

## AnnotateVCF
"""

import os
import sys
import gzip
import argparse


def CheckFileExist(fn):
    if not os.path.isfile(fn):
        return None
    return os.path.abspath(fn)


def AnnotateVCF(args):
    vcf_fn = args.vcf_fn
    b_fn = args.b_fn
    annovcf_fn = args.annovcf_fn

    if vcf_fn == None or CheckFileExist(vcf_fn) == None:
        print("Missing VCF input", file=sys.stderr)
        sys.exit(1)
    if b_fn == None or CheckFileExist(vcf_fn) == None:
        print("Missing input", file=sys.stderr)
        sys.exit(1)
    if annovcf_fn == None:
        print("Missing VCF output filename", file=sys.stderr)
        sys.exit(1)

    results = {}

    with gzip.open(b_fn, "rb") if b_fn.endswith(".gz") else open(b_fn, "r") as f:
        for row in f:
            col = row.split()
            results[col[2] + "-" + col[3]] = row[0]

    with gzip.open(vcf_fn, "rb") if vcf_fn.endswith(".gz") else open(vcf_fn, "r") as f, open(annovcf_fn, "w") as o:
        for row in f:
            row = row.rstrip("\n")
            col = row.split()
            if col[0] == "#CHROM":
                print('##FILTER=<ID=b,Description="filtered">', file=o)
                print(row, file=o)
            elif col[0][0] == col[0][1] and col[0][0] == "#":
                print(row, file=o)
            else:
                stat = results[col[0] + "-" + col[1]]
                if stat == "X" or stat == "S":
                    col[6] = "b"
                else:
                    col[6] = "PASS"
                print("\t".join(col), file=o)


def main():
    parser = argparse.ArgumentParser(
        description="Annotate an VCF according output")

    parser.add_argument('--vcf_fn', type=str, default=None,
                        help="Unannotated VCF file input, mandatory")

    parser.add_argument('--b_fn', type=str, default=None,
                        help="Decision input, mandatory")

    parser.add_argument('--annovcf_fn', type=str, default=None,
                        help="Annotated VCF file output, mandatory")

    args = parser.parse_args()

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        sys.exit(1)

    AnnotateVCF(args)


if __name__ == '__main__':
    main()
