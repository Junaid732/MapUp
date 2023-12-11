import pandas as pd
import datetime


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    pivot = df.pivot(index="id_start", columns="id_end", values="distance")
    pivot = pivot.fillna(0)
    pivot = pivot + pivot.T

    for i in range(len(pivot)):
        pivot.iloc[i,i] = 0

        return pivot

df = calculate_distance_matrix(pd.read_csv("C:\New folder (3)\MapUp-Data-Assessment-F\datasets\dataset-3.csv", sep=","))
return df


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    stacked = df.stack()
    unstacked = stacked.reset_index()
    unstacked.columns = ["id_start", "id_end", "distance"]
    unstacked = unstacked[unstacked["id_start"] != unstacked["id_end"]]

    return unstacked

return df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    df_ref = df[df["id_start"] == ref]
    avg_ref = df_ref["distance"].mean()
    threshold = avg_ref * 0.1
    mask = abs(df["distance"] - avg_ref) <= threshold

    ids = df[mask]["id_start"].unique()
    ids_list = list(ids)
    ids_list.sort()
    return ids_list

return df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    moto_rate = 0.8
    car_rate = 1.2
    rv_rate = 1.5
    bus_rate = 2.2
    truck_rate = 3.6

    df["moto"] = df["distance"] * moto_rate
    df["car"] = df["distance"] * car_rate
    df["rv"] = df["distance"] * rv_rate
    df["bus"] = df["distance"] * bus_rate
    df["truck"] = df["distance"] * truck_rate
    
return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    weekday_morning = 0.8
    weekday_day = 1.2
    weekday_evening = 0.8
    weekend = 0.7

    morning_start = datetime.time(0, 0, 0)
    morning_end = datetime.time(10, 0, 0)
    day_start = datetime.time(10, 0, 0)
    day_end = datetime.time(18, 0, 0)
    evening_start = datetime.time(18, 0, 0)
    evening_end = datetime.time(23, 59, 59)

    start_days = []
    start_times = []
    end_days = []
    end_times = []
    toll_rates = []

    for i, row in df.iterrows():
        # get the id_start and id_end values
        id_start = row["id_start"]
        id_end = row["id_end"]

        start_day = random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        start_days.append(start_day)

        start_time = datetime.time(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
        start_times.append(start_time)

        if start_day == "Sunday":
            end_day = "Monday"
        else:
            day_index = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(start_day)
            end_day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][day_index + 1]
        end_days.append(end_day)

        end_time = (datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(hours=1)).time()
        end_times.append(end_time)

        if start_day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
            if morning_start <= start_time < morning_end:
                toll_rate = row["distance"] * weekday_morning
            elif day_start <= start_time < day_end:
                toll_rate = row["distance"] * weekday_day
            elif evening_start <= start_time <= evening_end:
                toll_rate = row["distance"] * weekday_evening
        else:
            toll_rate = row["distance"] * weekend
        toll_rates.append(toll_rate)

    df["start_day"] = start_days
    df["start_time"] = start_times
    df["end_day"] = end_days
    df["end_time"] = end_times
    df["toll_rate"] = toll_rates
    
return df
