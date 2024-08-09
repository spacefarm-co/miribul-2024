import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def preprocessing(ex_path, in_path, control_path):
    # data
    ex_df = pd.read_csv(ex_path)
    in_df = pd.read_csv(in_path)
    control_df = pd.read_csv(control_path)

    # copy
    ex_df_copy = ex_df.copy()
    in_df_copy = in_df.copy()
    control_df_copy = control_df.copy()

    ex_df_copy['datetime'] = pd.to_datetime(ex_df_copy['datetime'])
    in_df_copy['datetime'] = pd.to_datetime(in_df_copy['datetime'])
    control_df_copy['datetime'] = pd.to_datetime(control_df_copy['datetime'])

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


    uwl01 = []
    uwl02 = []
    uwl03 = []
    uwl04 = []
    uwR01 = []
    uwR02 = []
    uwR03 = []
    uwR04 = []
    swl01 = []
    swl02 = []
    swl03 = []
    swl04 = []
    pd.set_option('mode.chained_assignment',  None) 
    merge_copy = merge.copy()
    control = uwl01
    control = merge_copy[['datetime', 'upWinL01']]
    control.fillna(0, inplace=True)
    control['date'] = control['datetime'].dt.date
    control['hour'] = control['datetime'].dt.hour

    # Missing value correction
    for idx, row in control.iterrows():
        if row['upWinL01'] == 0:
            hour = row['hour']
            date = row['date']
            
            # Set 5-day intervals before and after
            start_date = date - pd.Timedelta(days=5)
            end_date = date + pd.Timedelta(days=5)
            
            ref_data = control[(control['date'] >= start_date) & (control['date'] <= end_date) 
                                & (control['hour'] == hour) & (control['upWinL01'] > 0)]
            
            if not ref_data.empty:
                control.at[idx, 'upWinL01'] = np.random.choice(ref_data['upWinL01'])
            uwl01 = control
            
    merge_copy = merge.copy()
    control = uwl02
    control = merge_copy[['datetime','upWinL02']]
    control.fillna(0, inplace=True)
    control['date'] = control['datetime'].dt.date
    control['hour'] = control['datetime'].dt.hour

    # Missing value correction
    for idx, row in control.iterrows():
        if row['upWinL02'] == 0:
            hour = row['hour']
            date = row['date']
            
            # Set 5-day intervals before and after
            start_date = date - pd.Timedelta(days=5)
            end_date = date + pd.Timedelta(days=5)
            
            ref_data = control[(control['date'] >= start_date) & (control['date'] <= end_date) 
                                & (control['hour'] == hour) & (control['upWinL02'] > 0)]
            
            if not ref_data.empty:
                control.at[idx, 'upWinL02'] = np.random.choice(ref_data['upWinL02'])
            uwl02 = control

    merge_copy = merge.copy()
    control = uwl03
    control = merge_copy[['datetime','upWinL03']]
    control.fillna(0, inplace=True)
    control['date'] = control['datetime'].dt.date
    control['hour'] = control['datetime'].dt.hour

    # Missing value correction
    for idx, row in control.iterrows():
        if row['upWinL03'] == 0:
            hour = row['hour']
            date = row['date']
            
            # Set 5-day intervals before and after
            start_date = date - pd.Timedelta(days=5)
            end_date = date + pd.Timedelta(days=5)
            
            ref_data = control[(control['date'] >= start_date) & (control['date'] <= end_date) 
                                & (control['hour'] == hour) & (control['upWinL03'] > 0)]
            
            if not ref_data.empty:
                control.at[idx, 'upWinL03'] = np.random.choice(ref_data['upWinL03'])
            uwl03 = control

    pd.set_option('mode.chained_assignment',  None) 
    merge_copy = merge.copy()
    control = uwl04
    control = merge_copy[['datetime','upWinL04']]
    control.fillna(0, inplace=True)
    control['date'] = control['datetime'].dt.date
    control['hour'] = control['datetime'].dt.hour

    # Missing value correction
    for idx, row in control.iterrows():
        if row['upWinL04'] == 0:
            hour = row['hour']
            date = row['date']
            
            # Set 5-day intervals before and after
            start_date = date - pd.Timedelta(days=5)
            end_date = date + pd.Timedelta(days=5)
            
            ref_data = control[(control['date'] >= start_date) & (control['date'] <= end_date) 
                                & (control['hour'] == hour) & (control['upWinL04'] > 0)]
            
            if not ref_data.empty:
                control.at[idx, 'upWinL04'] = np.random.choice(ref_data['upWinL04'])
            uwl04 = control
            
    merge_copy = merge.copy()
    control = uwR01
    control = merge_copy[['datetime','upWinR01']]
    control.fillna(0, inplace=True)
    control['date'] = control['datetime'].dt.date
    control['hour'] = control['datetime'].dt.hour

    # Missing value correction
    for idx, row in control.iterrows():
        if row['upWinR01'] == 0:
            hour = row['hour']
            date = row['date']
            
            # Set 5-day intervals before and after
            start_date = date - pd.Timedelta(days=5)
            end_date = date + pd.Timedelta(days=5)
            
            ref_data = control[(control['date'] >= start_date) & (control['date'] <= end_date) 
                                & (control['hour'] == hour) & (control['upWinR01'] > 0)]
            
            if not ref_data.empty:
                control.at[idx, 'upWinR01'] = np.random.choice(ref_data['upWinR01'])
            uwR01 = control

    merge_copy = merge.copy()
    control = uwR02
    control = merge_copy[['datetime','upWinR02']]
    control.fillna(0, inplace=True)
    control['date'] = control['datetime'].dt.date
    control['hour'] = control['datetime'].dt.hour

    # Missing value correction
    for idx, row in control.iterrows():
        if row['upWinR02'] == 0:
            hour = row['hour']
            date = row['date']
            
            # Set 5-day intervals before and after
            start_date = date - pd.Timedelta(days=5)
            end_date = date + pd.Timedelta(days=5)
            
            ref_data = control[(control['date'] >= start_date) & (control['date'] <= end_date) 
                                & (control['hour'] == hour) & (control['upWinR02'] > 0)]
            
            if not ref_data.empty:
                control.at[idx, 'upWinR02'] = np.random.choice(ref_data['upWinR02'])
            uwR02 = control

    merge_copy = merge.copy()
    control = uwR03
    control = merge_copy[['datetime','upWinR03']]
    control.fillna(0, inplace=True)
    control['date'] = control['datetime'].dt.date
    control['hour'] = control['datetime'].dt.hour

    # Missing value correction
    for idx, row in control.iterrows():
        if row['upWinR03'] == 0:
            hour = row['hour']
            date = row['date']
            
            # Set 5-day intervals before and after
            start_date = date - pd.Timedelta(days=5)
            end_date = date + pd.Timedelta(days=5)
            
            ref_data = control[(control['date'] >= start_date) & (control['date'] <= end_date) 
                                & (control['hour'] == hour) & (control['upWinR03'] > 0)]
            
            if not ref_data.empty:
                control.at[idx, 'upWinR03'] = np.random.choice(ref_data['upWinR03'])
            uwR03 = control

    merge_copy = merge.copy()
    control = uwR04
    control = merge_copy[['datetime','upWinR04']]
    control.fillna(0, inplace=True)
    control['date'] = control['datetime'].dt.date
    control['hour'] = control['datetime'].dt.hour

    # Missing value correction
    for idx, row in control.iterrows():
        if row['upWinR04'] == 0:
            hour = row['hour']
            date = row['date']
            
            # Set 5-day intervals before and after
            start_date = date - pd.Timedelta(days=5)
            end_date = date + pd.Timedelta(days=5)
            
            ref_data = control[(control['date'] >= start_date) & (control['date'] <= end_date) 
                                & (control['hour'] == hour) & (control['upWinR04'] > 0)]
            
            if not ref_data.empty:
                control.at[idx, 'upWinR04'] = np.random.choice(ref_data['upWinR04'])
            uwR04 = control

    merge_copy = merge.copy()
    control = swl01
    control = merge_copy[['datetime', 'siWinL01']]
    control.fillna(0, inplace=True)
    control['date'] = control['datetime'].dt.date
    control['hour'] = control['datetime'].dt.hour

    # Missing value correction
    for idx, row in control.iterrows():
        if row['siWinL01'] == 0:
            hour = row['hour']
            date = row['date']
            
            # Set 5-day intervals before and after
            start_date = date - pd.Timedelta(days=5)
            end_date = date + pd.Timedelta(days=5)
            
            ref_data = control[(control['date'] >= start_date) & (control['date'] <= end_date) 
                                & (control['hour'] == hour) & (control['siWinL01'] > 0)]
            
            if not ref_data.empty:
                control.at[idx, 'siWinL01'] = np.random.choice(ref_data['siWinL01'])
            swl01 = control

    merge_copy = merge.copy()
    control = swl02
    control = merge_copy[['datetime', 'siWinL02']]
    control.fillna(0, inplace=True)
    control['date'] = control['datetime'].dt.date
    control['hour'] = control['datetime'].dt.hour

    # Missing value correction
    for idx, row in control.iterrows():
        if row['siWinL02'] == 0:
            hour = row['hour']
            date = row['date']
            
            # Set 5-day intervals before and after
            start_date = date - pd.Timedelta(days=5)
            end_date = date + pd.Timedelta(days=5)
            
            ref_data = control[(control['date'] >= start_date) & (control['date'] <= end_date) 
                                & (control['hour'] == hour) & (control['siWinL02'] > 0)]
            
            if not ref_data.empty:
                control.at[idx, 'siWinL02'] = np.random.choice(ref_data['siWinL02'])
            swl02 = control

    merge_copy = merge.copy()
    control = swl03
    control = merge_copy[['datetime', 'siWinL03']]
    control.fillna(0, inplace=True)
    control['date'] = control['datetime'].dt.date
    control['hour'] = control['datetime'].dt.hour

    # Missing value correction
    for idx, row in control.iterrows():
        if row['siWinL03'] == 0:
            hour = row['hour']
            date = row['date']
            
            # Set 5-day intervals before and after
            start_date = date - pd.Timedelta(days=5)
            end_date = date + pd.Timedelta(days=5)
            
            ref_data = control[(control['date'] >= start_date) & (control['date'] <= end_date) 
                                & (control['hour'] == hour) & (control['siWinL03'] > 0)]
            
            if not ref_data.empty:
                control.at[idx, 'siWinL03'] = np.random.choice(ref_data['siWinL03'])
            swl03 = control

    merge_copy = merge.copy()
    control = swl04
    control = merge_copy[['datetime','siWinL04']]
    control.fillna(0, inplace=True)
    control['date'] = control['datetime'].dt.date
    control['hour'] = control['datetime'].dt.hour

    # Missing value correction
    for idx, row in control.iterrows():
        if row['siWinL04'] == 0:
            hour = row['hour']
            date = row['date']
            
            # Set 5-day intervals before and after
            start_date = date - pd.Timedelta(days=5)
            end_date = date + pd.Timedelta(days=5)
            
            ref_data = control[(control['date'] >= start_date) & (control['date'] <= end_date) 
                                & (control['hour'] == hour) & (control['siWinL04'] > 0)]
            
            if not ref_data.empty:
                control.at[idx, 'siWinL04'] = np.random.choice(ref_data['siWinL04'])
            swl04 = control

    # Remove what you don’t need
    drop_label = ['date', 'hour']
    uwl01 = uwl01.drop(labels = drop_label, axis=1)
    uwl02 = uwl02.drop(labels = drop_label, axis=1)
    uwl03 = uwl03.drop(labels = drop_label, axis=1)
    uwl04 = uwl04.drop(labels = drop_label, axis=1)

    uwR01 = uwR01.drop(labels = drop_label, axis=1)
    uwR02 = uwR02.drop(labels = drop_label, axis=1)
    uwR03 = uwR03.drop(labels = drop_label, axis=1)
    uwR04 = uwR04.drop(labels = drop_label, axis=1)

    swl01 = swl01.drop(labels = drop_label, axis=1)
    swl02 = swl02.drop(labels = drop_label, axis=1)
    swl03 = swl03.drop(labels = drop_label, axis=1)
    swl04 = swl04.drop(labels = drop_label, axis=1)

    # merge
    merge1 = merge.combine_first(uwl01)
    merge2 = merge1.combine_first(uwl02)
    merge3 = merge2.combine_first(uwl03)
    merge4 = merge3.combine_first(uwl04)
    merge5 = merge4.combine_first(uwR01)
    merge6 = merge5.combine_first(uwR02)
    merge7 = merge6.combine_first(uwR03)
    merge8 = merge7.combine_first(uwR04)
    merge9 = merge8.combine_first(swl01)
    merge10 = merge9.combine_first(swl02)
    merge11 = merge10.combine_first(swl03)
    merge_final_ = merge11.combine_first(swl04)
    merge_final = merge_final_.fillna(0)

    return merge_final
