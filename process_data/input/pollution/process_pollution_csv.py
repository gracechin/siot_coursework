import csv
from datetime import datetime, timedelta

class ProcessPollutionCSV:
    def __init__(self, csv_name):
        self.csv_name = csv_name
        self.datetime_dicts = {}


        for pollutant in ["pm25", "pm10", "no2", "o3", "co"]:
            self.pollutant = pollutant
            self.header = ['Datetime']

            self.curr_dict = None
            self.curr_dt = None
            self.curr_loc = None
            self.curr_val = None

            self.new_csv_name = self.pollutant + "_data"

            # with open(self.new_csv_name + '.csv', mode='wb') as csv_file:
            #     self.writer = csv.DictWriter(csv_file, fieldnames=self.header)
            self.read()
            self.write()

    def read(self):
        with open(self.csv_name + ".csv", 'r') as file:
            reader = csv.DictReader(file)
            line_count = 0
            for row in reader:
                if line_count > 0 and len(row['Timestamp'])>0:
                    self.update_curr(row)
                    self.timestamp_exist()
                    self.location_exist()
                    self.update_header()
                    self.update_dt_dicts()
                    #print(row)
                    #print(self.curr_dict)
                    # print(self.header)
                line_count+=1

    def update_curr(self, row):
        self.curr_dt = self.datetime(row['Timestamp'])
        self.curr_loc = row['Location']
        self.curr_val = row[self.pollutant]

    def round_to_hour(self, dt):
        dt_start_of_hour = dt.replace(minute=0, second=0, microsecond=0)
        dt_half_hour = dt.replace(minute=30, second=0, microsecond=0)
        if dt >= dt_half_hour:
            # round up
            dt = dt_start_of_hour + timedelta(hours=1)
        else:
            # round down
            dt = dt_start_of_hour
        return dt

    def datetime(self, ts):
        ts = ts[:-5]
        dt = datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S')
        return self.round_to_hour(dt)

    def update_header(self):
        if self.curr_loc not in self.header:
            self.header.append(self.curr_loc)

    def timestamp_exist(self):
        if len(self.datetime_dicts.keys()) == 0:
            self.datetime_dicts[self.curr_dt] = {"Datetime": self.curr_dt}
            self.curr_dict = {"Datetime": self.curr_dt}
        elif self.curr_dt not in self.datetime_dicts.keys():
            self.datetime_dicts[self.curr_dt] = {"Datetime": self.curr_dt}
            self.curr_dict = {"Datetime": self.curr_dt}
        else:
            self.curr_dict = self.datetime_dicts[self.curr_dt]

    def add_time_placeholder(self):
        last_dt = min(self.datetime_dicts.keys())
        next_dt = last_dt - timedelta(hours=1)
        next_dict = self.datetime_dicts[last_dt]
        #next_dict["Datetime"] = next_dt
        self.datetime_dicts[next_dt] = next_dict
        #print(self.datetime_dicts[next_dt])
        self.timestamp_exist()

    def location_exist(self):
        self.curr_dict[self.curr_loc] = self.curr_val

    def update_dt_dicts(self):
        self.datetime_dicts[self.curr_dt] = self.curr_dict
        #(self.curr_dt, self.curr_dict["Datetime"])

    def write(self):
        print("WRITING " + self.new_csv_name)
        with open(self.new_csv_name + '.csv', mode='wb') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.header)

            writer.writeheader()
            keys_list = sorted(self.datetime_dicts.keys())
            for i in range(len(self.datetime_dicts.keys())):
                # first key
                if i == 0:
                    writer.writerow(self.datetime_dicts[keys_list[i]])
                else:
                    last_dt = self.datetime_dicts[keys_list[i - 1]]["Datetime"]
                    curr_dt = self.datetime_dicts[keys_list[i]]["Datetime"]
                    last_dict = self.datetime_dicts[keys_list[i - 1]]
                    # Fill in difference
                    while (curr_dt - last_dt).seconds/3600.0 != 1.0:
                        # write new fill row
                        next_dt = last_dt + timedelta(hours=1)
                        next_dict = last_dict
                        next_dict["Datetime"] = next_dt
                        writer.writerow(next_dict)
                        # update last_dt
                        last_dt = next_dt
                        last_dict = next_dict
                    writer.writerow(self.datetime_dicts[keys_list[i]])



ProcessPollutionCSV("pollution_data_1")
# read csv file

# go through csv row-by-row
# filter csv by time date

# > seek country and add if not exist
# > record pollutant value

# convert date to date-time
# write new row on csv file