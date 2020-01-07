# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 09:07:12 2020

@author: jdeed
"""

# path is a folder containing csvs, outputpath = output folder, outputname = output filename
def concatinate_script(path,outputpath,outputname):

    import glob
    import pandas as pd
    filelist = glob.glob(path + "/*.csv")
    print(filelist)
    li = []
    for filename in filelist:
        df = pd.read_csv(filename, index_col=None, header = 0)
        li.append(df)
        frame = pd.concat(li, axis=0, ignore_index=True)
    print(frame)
    frame.to_csv('{}/{}.csv'.format(outputpath,outputname), index=None, header=True)
