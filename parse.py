# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 15:55:14 2016

@author: altur
@edited: abatkins
"""
import re, argparse, numpy as np, scipy.stats as stats

def parse(infile, outfile, keyword):
    f = open(infile, 'r')
    fw = open(outfile, 'w')
    j = 0
    k = 1
    results = []
    for i in range(0, 10000):
        text = f.readline()
        if keyword in text:
            mean = re.sub("\s\s+", " ", text).split(" ")[1]
            results.append(float(mean))
            fw.write(' ' + str(k) + ' ')
            fw.write(text)
            j += 1
            if j == 20:
                k += 1
                j = 0
    mean = np.mean(results)
    lb, ub = stats.t.interval(0.95, len(results) - 1, loc=np.mean(results), scale=stats.sem(results))

    fw.write("\nAggregate Results\n")
    fw.write("Mean: {:.4f}\n".format(float(mean)))
    fw.write("95% Confidence Interval: ({:.4f}, {:.4f})".format(float(lb), float(ub)))
    fw.close()


if __name__ == "__main__":
    # Arg Parser
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--infile', '-i', type=str,
                        help='Input file')
    parser.add_argument('--outfile', '-o', type=str, default='analysis.out',
                        help='Output file')
    parser.add_argument('--keyword', '-k', type=str,
                        help='Siman Attribute to analyze')

    args = parser.parse_args()
    parse(args.infile, args.outfile, args.keyword)