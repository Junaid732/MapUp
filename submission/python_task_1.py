import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    pivot = df.pivot(index="id_1", columns="id_2", values="car")
    pivot = pivot.fillna(0)
    pivot = pivot.T
    for i in range(len(pivot)):
        pivot.iloc[i,i] = 0
    return pivot

df = generate_car_matrix(pd.read_csv("C:\New folder (3)\MapUp-Data-Assessment-F\datasets\dataset-1.csv", sep=","))
return df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    def assign_car_type(car):
        if car <= 15:
            return "low"
        elif car > 15 and car <= 25:
            return "medium"
        else:
            return "high"

    df["car_type"] = df["car"].apply(assign_car_type)
    count = df["car_type"].value_counts()
    count_dict = count.to_dict()
    count_dict = dict(sorted(count_dict.items()))
    return count_dict

dict = get_type_count(pd.read_csv("C:\New folder (3)\MapUp-Data-Assessment-F\datasets\dataset-1.csv", sep=","))
print(dict)

return dict()


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    mean = df["bus"].mean()
    mask = df["bus"] > 2 * mean
    index = df.index[mask]
    index_list = list(index)
    index_list.sort()

    return index_list

list = get_bus_indexes(pd.read_csv("C:\New folder (3)\MapUp-Data-Assessment-F\datasets\dataset-1.csv", sep=","))

return list()


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    grouped = df.groupby("route")["truck"].mean()
    filtered = grouped[grouped > 7]
    index = filtered.index
    index_list = list(index)
    index_list.sort()
    return index_list

list = filter_routes(pd.read_csv("C:\New folder (3)\MapUp-Data-Assessment-F\datasets\dataset-1.csv", sep=","))
return list()


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    def apply_logic(value):
        if value > 20:
            return value * 0.75
        else:
            return value * 1.25

    df = df.applymap(apply_logic).round(1)
    return df

df = pd.read_csv("C:\New folder (3)\MapUp-Data-Assessment-F\datasets\dataset-1.csv", sep=",")
result = generate_car_matrix(df)
matrix = multiply_matrix(result)

return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    df["startTime"] = pd.to_datetime(df["startTime"])
    df["endTime"] = pd.to_datetime(df["endTime"])

    df["duration"] = (df["endTime"] - df["startTime"]).dt.total_seconds() / 3600
    grouped = df.groupby(["id", "id_2"]).agg({"duration": "sum", "startDay": "nunique", "endDay": "nunique"})

    pd.Series = (grouped["duration"] != 24) | (grouped["startDay"] != 7) | (grouped["endDay"] != 7)
    
    return pd.Series()
