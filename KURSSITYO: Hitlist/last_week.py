#!/usr/bin/env python3

import pandas as pd
import numpy as np

def special_missing_values():
    data = pd.read_csv("src/UK-top40-1964-1-2.tsv",sep="\t")
    m = ((data.loc[:,"LW"] == "New") | (data.loc[:,"LW"] == "Re"))
    data[m] = np.nan
    data["LW"] = pd.to_numeric(data.loc[:,"LW"])
    return data

def last_week():
    data = special_missing_values()
    peak_mask = (data["Peak Pos"] != data["Pos"]) | (data["Pos"] == data["LW"])
    uusidatum = pd.DataFrame({"Pos":data["LW"],"LW":np.nan,"Title":data["Title"],"Artist":data["Artist"],"Publisher":data["Publisher"],"Peak Pos":data["Peak Pos"],"WoC":data["WoC"]-1,})
    uusidatum["Peak Pos"].where(peak_mask, other = np.nan, inplace=True)
    uusidatum.loc[uusidatum["Pos"] == 1,"Peak Pos"] = data.loc[data["Pos"] == 1,"Peak Pos"]
    uusidatum.loc[(data["Pos"]-1 == data["LW"]) & (data["Pos"] == data["Peak Pos"]),"Peak Pos"] = uusidatum.loc[(data["Pos"]-1 == data["LW"]) & (data["Pos"] == data["Peak Pos"]),"Pos"]
    
    puuttuvat_entryt = list(range(1,41))
    for i in range(1,41):
        if i in uusidatum["Pos"].values:
            puuttuvat_entryt.remove(i)

    uusidatum.loc[uusidatum["Pos"].isnull(),"Pos"] = puuttuvat_entryt

    uusidatum.sort_values(by="Pos",inplace=True)

    return uusidatum

def main():
    df = last_week()
    #print("Shape: {}, {}".format(*df.shape))
    #print("dtypes:", df.dtypes)
    print(df)
    #df1 = special_missing_values()
    #print(df1.loc[(df1["Pos"]-1 == df1["LW"]) & (df1["Pos"] == df1["Peak Pos"]),:])
    #print()
    #print(df.loc[df["Peak Pos"].isnull(),:])
    


if __name__ == "__main__":
    main()
