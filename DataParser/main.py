from parser_lib import Parser
import matplotlib.pyplot as plt


IS_DEBUG = True

parser = Parser('', '/Users/marcoravazzini/usefulScripts/RavazDrive/Config_files/Android_OP3_Sync/Gps_Logger/')

data = parser.battery_parser()
data['temperature'] = data['temperature'] / 10
data['voltage'] = data['voltage'] /1000
data[['level', 'voltage', 'temperature']].plot(grid=True)

plt.show()

# print(data)