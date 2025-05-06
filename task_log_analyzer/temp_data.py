import pandas as pd
import math

def temp_data():
    df = pd.read_csv("./temp-data.csv", parse_dates=["Date"])
    df["Start Time"]

    # Remove empty rows
    df = df.dropna(how="all")

    # Replace empty cells with None
    df = df.replace(math.nan, "None")

    ids = [1,2,3,4,5,6,7,8,9,10]
    df.insert(0, "ID", ids, False)

    durations = ["01:53:00", "01:11:00", "01:32:00", "01:13:00",
                 "01:25:00", "01:09:00", "01:13:00", "00:38:00", "02:00:00", "02:33:00"]
    df.insert(7, "Duration", durations, True)


    df_string = df.to_string(index=False)
    # print(df_string)

    return df