import pandas as pd
import numpy as np
import multiprocessing
from functools import partial

def _df_split(tup_arg, **kwargs):
	split_ind, df_split, df_f_name = tup_arg
	return (split_ind, getattr(df_split, df_f_name)(**kwargs))

def df_multicores(df, df_f_name, subset=None, njobs=-1, **kwargs):
    '''
    process operation in a multiprocessing fashion
    args:
        df: dataframe on which performing operations
        df_f_name: processing function
        subset : column of the dataframe on which to compute the function
        njobs: number of processes
    '''
    if njobs == -1:
        njobs = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=njobs-1)

    try:
        splits = np.array_split(df[subset], njobs)

    except ValueError:
        splits = np.array_split(df, njobs)

    pool_data = [(split_ind, df_split, df_f_name) for split_ind, df_split in enumerate(splits)]
    results = pool.map(partial(_df_split, **kwargs), pool_data)
    pool.close()
    pool.join()

    # order results back
    results = sorted(results, key=lambda x:x[0])
    # concatenate the results in a dataframe
    results = pd.concat([split[1] for split in results])

    return results.values