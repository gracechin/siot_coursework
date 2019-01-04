import csv
from datetime import datetime

class ProcessTwitterCSV:
    def __init__(self, csv_name):
        self.csv_name = csv_name
        self.datetime_dicts = {}

        self.pollutant = "pm25"
        self.header = ['Datetime']

        self.curr_dict = None
        self.curr_dt = None
        self.curr_loc = None
        self.curr_gen_loc = None

        self.new_csv_name = "processed_twitter_data"

        self.read()
        self.write()

    def read(self):
        with open(self.csv_name + ".csv", 'r') as file:
            reader = csv.DictReader(file)
            line_count = 0
            for row in reader:
                if line_count>0:
                    print(row)
                    try:
                        self.update_curr(row)
                    except:
                        continue
                    filter_loc = self.curr_gen_loc
                    self.timestamp_exist()
                    self.location_exist(filter_loc)
                    self.update_header(filter_loc)
                    self.update_dt_dicts()
                line_count+=1

    def update_curr(self, row):
        self.curr_dt = self.datetime(row['Timestamp'])
        self.curr_loc = row['Location ']
        self.curr_gen_loc = row['General location']

    def datetime(self, ts):
        dt = datetime.strptime(ts, '%a %b %d %H:%M:%S ').replace(microsecond=0,second=0,minute=0)
        return dt

    def update_header(self, loc):
        if loc not in self.header:
            self.header.append(loc)

    def timestamp_exist(self):
        if self.curr_dt not in self.datetime_dicts.keys():
            self.datetime_dicts[self.curr_dt]={"Datetime":self.curr_dt}
            self.curr_dict = {"Datetime":self.curr_dt}
        else:
            self.curr_dict = self.datetime_dicts[self.curr_dt]

    def location_exist(self, loc):
        if loc not in self.curr_dict.keys():
            self.curr_dict[loc] = 1
        else:
            self.curr_dict[loc] +=1

    def update_dt_dicts(self):
        self.datetime_dicts[self.curr_dt] = self.curr_dict

    def write(self):
        with open(self.new_csv_name + '.csv', mode='wb') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.header)

            writer.writeheader()
            for dt_key in self.datetime_dicts.keys():
                print('writing', self.datetime_dicts[dt_key])
                writer.writerow(self.datetime_dicts[dt_key])

ProcessTwitterCSV("twitter_data")
# read csv file

# go through csv row-by-row
# filter csv by time date

# > seek country and add if not exist
# > record pollutant value

# convert date to date-time
# write new row on csv file