import pandas as pd
from pandas.io.json import json_normalize
import json
import os.path
from enum import Enum
import glob

# import numpy as np
# import matplotlib.pyplot as plt


class Type(Enum):
    DATE = 1
    NUMBER = 2


class Parser:
    def __init__(self, miband_basepath, location_basepath):
        self.miband_basepath = miband_basepath
        self.location_basepath = location_basepath

    def __mi_generic_parser__(self, files_path, pickle_path, main_key,
                              number_of_files, columns):
        main_df = ''
        if not os.path.isfile(pickle_path) or isDebug:
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

    def mi_heart_parser(self, number_of_files, isDebug=False):
        '''Return a DataFrame with the date as index and heart rate value as instensity column'''

        files_path = os.path.join(self.miband_basepath, 'logReportHeart{}.bak')
        pickle_path = os.path.join(self.miband_basepath, 'heart_data_pickle')
        columns = [('timestamp', Type.DATE), ('intensity', Type.NUMBER)]
        return self.__mi_generic_parser__(files_path, pickle_path,
                                          'HeartMonitorData', number_of_files,
                                          columns)

    def mi_steps_parser(self, number_of_files, isDebug=False):
        '''Return a DataFrame with the date as index and cumulative number of steps in steps column'''

        files_path = os.path.join(self.miband_basepath, 'logReportSteps{}.bak')
        pickle_path = os.path.join(self.miband_basepath, 'steps_data_pickle')
        columns = [('dateTime', Type.DATE), ('steps', Type.NUMBER)]
        return self.__mi_generic_parser__(files_path, pickle_path, 'StepsData',
                                          number_of_files, columns)

    def mi_sleep_parser(self, number_of_files, isDebug=False):
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

    def location_parser(self, isDebug=False):
        files = glob.glob(
            "/Users/marcoravazzini/RavazDrive/Config_files/Android_OP3_Sync/Gps_Logger/*.csv"
        )
     
        main_df = ''
        for file in files:
            df = pd.read_csv(
                file,
                usecols=['time', 'lat', 'lon', 'elevation', 'battery'])
            df['time'] = pd.to_datetime(df.time)
            if main_df is '':
                main_df = df
            else:
                main_df = pd.concat([main_df, df])
        main_df.set_index('time', inplace=True)
        return main_df
        


