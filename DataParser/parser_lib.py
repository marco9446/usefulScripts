import json
import os.path
from enum import Enum
import glob
import re
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np



class Type(Enum):
    DATE = 1
    NUMBER = 2

def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.    

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(
        dlat / 2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km

class Parser:
    def __init__(self, miband_basepath, location_basepath):
        self.miband_basepath = miband_basepath
        self.location_basepath = '/Users/marcoravazzini/RavazDrive/Config_files/Android_OP3_Sync/Gps_Logger/'

    def __mi_generic_parser__(self, files_path, pickle_path, main_key,
                              number_of_files, columns):
        main_df = ''
        if not os.path.isfile(pickle_path) or is_debug:
            for a in range(0, number_of_files + 1):
                a = a if number_of_files > 0 else ''
                curr_path = files_path.format(a)

                with open(curr_path) as data_file:
                    data = json.load(data_file)

                df = json_normalize(data[main_key])

                for column in columns:
                    if column[1] == Type.DATE:
                        df[column[0]] = pd.to_datetime(
                            df[column[0]], unit='ms')
                    elif column[1] == Type.NUMBER:
                        df[column[0]] = pd.to_numeric(df[column[0]])

                df.set_index(columns[0][0], inplace=True)

                if main_df is '':
                    main_df = df[[col[0] for col in columns[1:]]]
                else:
                    main_df = pd.concat(
                        [main_df, df[[col[0] for col in columns[1:]]]])
        else:
            main_df = pd.read_pickle(pickle_path)

        return main_df

    def mi_heart_parser(self, number_of_files, is_debug=False):
        '''Return a DataFrame with the date as index and heart rate value as instensity column'''

        files_path = os.path.join(self.miband_basepath, 'logReportHeart{}.bak')
        pickle_path = os.path.join(self.miband_basepath, 'heart_data_pickle')
        columns = [('timestamp', Type.DATE), ('intensity', Type.NUMBER)]
        return self.__mi_generic_parser__(files_path, pickle_path,
                                          'HeartMonitorData', number_of_files,
                                          columns)

    def mi_steps_parser(self, number_of_files, is_debug=False):
        '''Return a DataFrame with the date as index and cumulative number of steps in steps column'''

        files_path = os.path.join(self.miband_basepath, 'logReportSteps{}.bak')
        pickle_path = os.path.join(self.miband_basepath, 'steps_data_pickle')
        columns = [('dateTime', Type.DATE), ('steps', Type.NUMBER)]
        return self.__mi_generic_parser__(files_path, pickle_path, 'StepsData',
                                          number_of_files, columns)

    def mi_sleep_parser(self, number_of_files, is_debug=False):
        '''
            Return a DataFrame with the date as index, the total mitntes of sleep,
            the minutes of REM and NON REM sleep and the starting and ending
            time of the sleep session
        '''

        files_path = os.path.join(self.miband_basepath,
                                  'logReportSleepDay{}.bak')
        pickle_path = os.path.join(self.miband_basepath, 'sleep_data_pickle')

        columns = [('dayDate', Type.DATE), ('startDateTime', Type.DATE),
                   ('endDateTime', Type.DATE), ('totalMinutes', Type.NUMBER),
                   ('totalNREM', Type.NUMBER), ('totalREM', Type.NUMBER)]

        return self.__mi_generic_parser__(
            files_path, pickle_path, 'SleepDayData', number_of_files, columns)

    def location_parser(self, is_debug=False):
        '''Parse GpsLogger files'''

        files = glob.glob(os.path.join(self.location_basepath, '*.csv'))

        main_df = ''
        for file in files:
            df = pd.read_csv(
                file, usecols=['time', 'lat', 'lon', 'elevation', 'battery'])
            df['time'] = pd.to_datetime(df.time)
            if main_df is '':
                main_df = df
            else:
                main_df = pd.concat([main_df, df])
        main_df.set_index('time', inplace=True)

        # print( main_df.iloc[1:, 1])
        main_df['dist'] = haversine_np(
            main_df.lon.shift(), main_df.lat.shift(), main_df.iloc[1:, 1],
            main_df.iloc[1:, 0])

        return main_df

    def app_usage_parser(self):
        path = '/Users/marcoravazzini/RavazDrive/Config_files/Android_OP3_Sync/App_Usage/'
        files = glob.glob(os.path.join(path, 'app_usage_*.log'))

        df = pd.DataFrame(columns=['time', 'app_name', 'usage'])
        counter = 0
        for file in files:
            with open(file, "r") as in_file:
                time_range=''
                for line in in_file:
                    time_range_raw = re.search(r'timeRange="(.*),', line)
                    if time_range_raw:
                        time_range = time_range_raw.group(1)
                    total_time = re.search(r'totalTime=\"(.*)\" l', line)
                    name = re.search(
                        r'package=(?!com\.google\.android\.|com\.android|org.lineageos|com\.qualcomm|com\.quicinc).*\.(.*) t',
                        line)

                    if name and total_time:
                        usage = total_time.group(1) if len(total_time.group(1)) > 5 else '00:'+total_time.group(1)
                        df.loc[counter] = [time_range, name.group(1), usage]
                        counter +=1
                    if 'ChooserCounts' in line:
                        break
        df['time'] = pd.to_datetime(df.time)
        df.set_index('time', inplace=True)
        df['usage'] = pd.to_timedelta(df.usage)
        return df

    def battery_parser(self):
        path = '/Users/marcoravazzini/RavazDrive/Config_files/Android_OP3_Sync/App_Usage/'
        files = glob.glob(os.path.join(path, 'battery*.csv'))
        main_df = ''
        for file in files:
            df = pd.read_csv(file, skipinitialspace=True)
            if main_df is '':
                main_df = df
            else:
                main_df = pd.concat([main_df, df], axis=0)

        main_df['time'] = pd.to_datetime(main_df.time, unit='ms')
        main_df.set_index('time', inplace=True)
        return main_df

