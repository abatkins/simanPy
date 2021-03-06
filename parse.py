# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 15:55:14 2016

@author: altur
@edited: abatkins
"""
import re, argparse
import pandas as pd
import numpy as np
import scipy.stats as stats


# Parse SIMAN outfile. Convert output to df/csv.
def parse(infile):
    data = {'TALLY VARIABLES': [[], ['run_id', 'identifier', 'average', 'half_width', 'min', 'max', 'obs']],
            'DISCRETE-CHANGE VARIABLES': [[], ['run_id', 'identifier', 'average', 'half_width', 'min', 'max', 'final_value']],
            'COUNTERS': [[], ['run_id', 'identifier', 'count', 'limit']]}
    replications = 0
    count = 0

    # Get filesize
    with open(infile, 'r') as f:
        num_lines = len(f.readlines())

    with open(infile, 'r') as f:
        # Iterate over each replication
        while count <= num_lines:
            key = re.sub("\s\s+", " ", f.readline()).strip()
            count += 1
            if key == "ARENA Simulation Results":  # start of new replication
                replications += 1
            if key in data.keys():  # start of new section
                [f.readline() for i in range(4)]
                count += 4

                # Iterate over a variable section for a single replication
                while True:
                    text = re.sub("\s\s+", " ", f.readline()).strip()
                    count += 1
                    if text != "":  # Not end of section
                        values = text.split(" ")
                        var_size = len(values) - len(data[key][1]) + 1
                        if var_size > 0: # handle varnames with spaces
                            row = [str(replications)] + ['_'.join(values[:var_size+1]).lower()] + values[var_size+1:]
                        else:
                            row = [str(replications)] + [values[0].lower()] + values[1:]
                        data[key][0].append(row)
                    else:  # end of section
                        break
    f.close()

    # Tally Variables Dataframe
    data['TALLY VARIABLES'] = pd.DataFrame(
        data=data['TALLY VARIABLES'][0],
        columns=data['TALLY VARIABLES'][1]
    ).apply(pd.to_numeric, args=('ignore',))

    # DSTATS Variables Dataframe
    data['DISCRETE-CHANGE VARIABLES'] = pd.DataFrame(
        data=data['DISCRETE-CHANGE VARIABLES'][0],
        columns=data['DISCRETE-CHANGE VARIABLES'][1]
    ).apply(pd.to_numeric, args=('ignore',))

    # Counter Dataframe
    data['COUNTERS'] = pd.DataFrame(
        data=data['COUNTERS'][0],
        columns=data['COUNTERS'][1]
    ).apply(pd.to_numeric, args=('ignore',))

    # Output to csv
    outfile = infile.split('.')[0]
    data['TALLY VARIABLES'].to_csv(outfile + '_tally.csv')
    data['DISCRETE-CHANGE VARIABLES'].to_csv(outfile + '_dstat.csv')
    data['COUNTERS'].to_csv(outfile + '_counters.csv')

    return data, outfile

# Creates df/csv with aggregate statistics over all replications. Includes mean and confidence intervals.
# Note: Use the to_latex method to output the df to a latex table.
def aggregate_stats(data, outfile_name=None, alpha=.05):
    results = []
    for df in data.values():
        names = df.identifier.unique()
        df_group = df.groupby('identifier')
        for name in names:
            if 'average' in df_group.get_group(name).columns:
                group_vals = df_group.get_group(name)['average']
            else:
                group_vals = df_group.get_group(name)['count']
            mean, ci = _compute_stats(group_vals)

            if 'obs' in df_group.get_group(name).columns:
                obs_vals = df_group.get_group(name)['obs']
                obs_mean, obs_ci = _compute_stats(obs_vals)
            else:
                obs_mean, obs_ci = None, None

            if 'min' in df_group.get_group(name).columns:
                min_vals = df_group.get_group(name)['min']
                min_mean, min_ci = _compute_stats(min_vals)
            else:
                min_mean, min_ci = None, None

            if 'max' in df_group.get_group(name).columns:
                max_vals = df_group.get_group(name)['max']
                max_mean, max_ci = _compute_stats(max_vals)
            else:
                max_mean, max_ci = None, None

            results.append([name, mean, ci, min_mean, max_mean, obs_mean, obs_ci])
    agg_df = pd.DataFrame(data=results,
                          columns=['identifier',
                                   'average', '{}% CI'.format(int((1-alpha)*100)),
                                   'min',
                                   'max',
                                   'obs', '{}% CI'.format(int((1 - alpha) * 100))
                                   ])
    agg_df.to_csv(outfile_name + '_aggregate.csv')

    return agg_df


def _compute_stats(vals, alpha=.05):
    vals = [0.0 if val == '.00000' else float(val) for val in vals if val != '--']
    mean = np.mean(vals)
    if len(np.unique(vals)) > 1:  # Compute CI
        lb, ub = stats.t.interval(1 - alpha, len(vals) - 1, loc=mean, scale=stats.sem(vals))
        ci = "({:.4f}, {:.4f})".format(float(lb), float(ub))
    else:  # Don't bother with CI if all values are the same.
        ci = "NA"
    return round(float(mean), 4), ci

if __name__ == "__main__":
    # Arg Parser
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--infile', '-i', type=str, help='Input file')
    parser.add_argument('--latex', '-l', action='store_true', help='Print Latex Table')

    args = parser.parse_args()
    data, outfile = parse(args.infile)
    agg = aggregate_stats(data, outfile)

    if args.latex:
        print(agg.to_latex())
    else:
        print(agg)