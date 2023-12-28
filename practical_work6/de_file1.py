from common_func import write_to_json, read_data
import os
import pandas as pd
import json


def get_memory_stat_by_col(df):
    memory_usage = df.memory_usage(deep=True)
    total = memory_usage.sum()
    print(f"file in memory size = {total//1024:10} КБ")
    col_stat = []
    for key in df.dtypes.keys():
        col_stat.append({
            "col_name" : key,
            "mem_abs" : int(memory_usage[key] // 1024),
            "mem_per" : float(round(memory_usage[key] / total * 100, 4)),
            "dtype" : str(df.dtypes[key])
        })
    col_stat.sort(key=lambda x : x["mem_abs"], reverse=True)
    write_to_json(".\\out1\\mem_stat_by_col_(no_optimization).json", col_stat)


def mem_usage(pd_obj):
    if isinstance(pd_obj, pd.DataFrame):
        usage_b = pd_obj.memory_usage(deep=True).sum()
    else:
        usage_b = pd_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2
    return "{:03.2f} МБ".format(usage_mb)


def opt_obj(df):
    conv_obj = pd.DataFrame()
    data_obj = df.select_dtypes(include=["object"]).copy()

    for col in data_obj.columns:
        num_unique_val = len(data_obj[col].unique())
        num_total_val = len(data_obj[col])
        if num_unique_val / num_total_val < 0.5:
            conv_obj.loc[:, col] = data_obj[col].astype("category")
        else:
            conv_obj.loc[:, col] = data_obj[col]
        
    #print(mem_usage(data_obj))
    #print(mem_usage(conv_obj))
    return conv_obj


def opt_int(df):
    dataset_int = df.select_dtypes(include=["int"])

    conv_int = dataset_int.apply(pd.to_numeric, downcast="unsigned")
    #print(mem_usage(dataset_int))
    #print(mem_usage(conv_int))

    compare_ints = pd.concat([dataset_int.dtypes, conv_int.dtypes], axis=1)
    compare_ints.columns = ["before", "after"]
    compare_ints.apply(pd.Series.value_counts)
    #print(compare_ints)
    return conv_int


def opt_float(df):
    dataset_float = df.select_dtypes(include=["float"])

    conv_float = dataset_float.apply(pd.to_numeric, downcast="float")
    #print(mem_usage(dataset_float))
    #print(mem_usage(conv_float))

    compare_floats = pd.concat([dataset_float.dtypes, conv_float.dtypes], axis=1)
    compare_floats.columns = ["before", "after"]
    compare_floats.apply(pd.Series.value_counts)
    #print(compare_floats)
    return conv_float


def main():
    file_name = ".\\dataset_6\\[1]game_logs.csv"
    file_size = os.path.getsize(file_name)
    dataset = read_data(file_name)

    print(f"file size =           {file_size//1024:10} КБ")
    #get_memory_stat_by_col(dataset)
  
    optimized_dataset = dataset.copy()
    conv_int = opt_int(dataset)
    conv_float = opt_float(dataset)
    conv_obj = opt_obj(dataset)
    
    optimized_dataset[conv_int.columns] = conv_int
    optimized_dataset[conv_float.columns] = conv_float
    optimized_dataset[conv_obj.columns] = conv_obj
    
    # print(mem_usage(dataset))
    # print(mem_usage(optimized_dataset))
    #get_memory_stat_by_col(optimized_dataset)

    
    colm_names = ["date", "number_of_game", "day_of_week",
                  "park_id", "v_manager_name", "length_minutes",
                  "v_hits", "h_hits", "h_walks", "h_errors"]

    opt_dtypes = optimized_dataset.dtypes
    reading_colms = {}

    for key in colm_names:
        reading_colms[key] = opt_dtypes[key]

    with open(".\\out1\\dtypes1.json", "w") as f:
        dtypes = reading_colms.copy()
        for key in dtypes.keys():
            dtypes[key] = str(dtypes[key])
        json.dump(dtypes, f)

    
    
    has_header = True
    for chunk in pd.read_csv(file_name,
                             usecols=colm_names,
                             dtype=reading_colms,
                             #infer_datetime_format=True,
                             chunksize=100000):
        print(mem_usage(chunk))
        chunk.to_csv(".\\out1\\df1.csv", mode="a", header=has_header, index=False)
        has_header = False

    #dataset.info(memory_usage="deep")


if __name__ == "__main__":
    main()