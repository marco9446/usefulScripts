import os
import re
IS_DEBUG = True


path = './data/dump_2019-03-01-15-05-31.log'


with open(path, "r") as in_file:
    for line in in_file:
        total_time = re.search(r'totalTime=\"(\d\d:\d\d)\"', line)
        name = re.search(r'package=(?!com\.google\.android\.|com\.android|org.lineageos|com\.qualcomm|com\.quicinc).*\.(.*) t', line)

        if name and total_time:
            print(name.group(1), total_time.group(1))
        if 'ChooserCounts' in line:
            break
