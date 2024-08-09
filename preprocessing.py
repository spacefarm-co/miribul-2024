import pandas as pd
from datetime import datetime, timedelta

def preprocessing(ex_path, in_path, control_path):
    # data
    ex_df = pd.read_csv(ex_path)
    in_df = pd.read_csv(in_path)
    control_df = pd.read_csv(control_path)

    # copy
    ex_df_copy = ex_df.copy()
    in_df_copy = in_df.copy()
    control_df_copy = control_df.copy()

    # rename
    control_df_copy.rename(columns = {'upWin0L4' : 'upWinL04'}, inplace = True)

    # If there is no rain or snow, data is not recorded.
    # Separately handle missing data
    env = ex_df_copy[['datetime', 'temperature', 'windSpeed',
        'windDirection', 'humidity', 'solar', 'groundTemp']]
    env_clean = env.dropna(axis=0)
    weather = ex_df_copy[['datetime', 'precipitation', 'snowfall']]

    # Merge internal and external environmental data
    all_df = pd.merge(env_clean, in_df_copy, on='datetime', how='left')
    all_2df = pd.merge(all_df, weather, on='datetime', how='left')

    # Change control data by time
    control_df_copy['min'] = control_df_copy['datetime'].map(lambda x : (str(x)[14:16]))
    control_df_copy_hour = control_df_copy[control_df_copy['min'] == '00']

    # Remove unnecessary columns from control data
    control_df_copy_hour_clean = control_df_copy_hour.drop(columns=[
        'siWinR01', 'siWinR02', 'siWinR03', 'siWinR04', 'upCurt01',
        'upCurt02', 'upCurt03', 'upCurt04', 'dnCurt01', 'dnCurt02', 
        'dnCurt03','dnCurt04', 'siCurt01', 'siCurt02', 'siCurt03', 
        'siCurt04','Unnamed: 29', 'min'])

    # Merge all data
    merge = pd.merge(control_df_copy_hour_clean, all_2df, how = 'outer', on = 'datetime')

    # Declare start and end dates
    start_time = merge['datetime'].min()
    format = '%Y-%m-%d %H:%M'
    dt = datetime.strptime(merge['datetime'].max(),format)+timedelta(days=1)
    end_time = datetime.strftime(dt,format)

    # Daily index create
    time_range = pd.date_range(start=start_time, end=end_time, freq='D')
    series_ts = pd.Series(range(len(time_range)) , index=time_range)
    plus_index1 = series_ts.to_frame()
    plus_index2 = plus_index1 + 1
    plus_index2['datetime'] = plus_index2.index
    plus_index2.reset_index(drop=True)
    plus_index2['new_date'] = plus_index2['datetime'].map(lambda x : (str(x)[:10]))
    merge['new_date'] = merge['datetime'].map(lambda x : (str(x)[:10]))

    merge2 = pd.merge(plus_index2, merge, how = 'outer', on = 'new_date')
    merge3 = merge2.drop(columns=['datetime_x', 'new_date'])
    merge3.rename(columns = {'datetime_y' : 'datetime'}, inplace = True)

    return merge3