#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, sys, datetime
from collections import defaultdict
from functools import partial
from itertools import repeat

class BorderCrossing:
    """
    
    Find the monthly totals, and sort border data with a running
    average for each type of vehicle over either of the US
    boarders.
    
    Typical use:
    
    1. Make BorderCrossing object with csv input file
    with fields including 'Border', 'Date', 'Measure', 'Value'
    
    bc = BorderCrossing(input_file)
    
    2. Write the monthly totals to output csv file
    
    bc.write_file(output_file, sort_dir_rev)
    
    sort_dir_rev = True: sorted descending
    sort_dir_rev = False: sorted ascending
    
    """ 
    
    _timedate_format = '%m/%d/%Y %I:%M:%S %p' # set the date/time format here
    
    # initialize dict as _border_dict[date][border][meas][values] = int; read file  
    def __init__(self, filename): 
        self._border_dict = self._n_level_defaultdict(int, 4)   
        self.read_file(filename)
        
    # read csv file to _border_dict then calculate the running average   
    def read_file(self, filename):   
        try:
            with open(filename) as csvfile:
                row_reader = csv.DictReader(csvfile)
                self._read_all_rows(row_reader)
        except KeyError:
            print("Error reading file: {}".format(filename))
            raise 
        except FileNotFoundError:
            raise FileNotFoundError("Error no file: {}".format(filename))      
        self._calc_run_average()
    
    # write _border_dict to csv file in descending order if sort_dir_rev = True
    def write_file(self, filename, sort_dir_rev = True):
        with open(filename, "w", newline='') as csvfile:
            row_writer = csv.writer(csvfile)
            # write header here
            row_writer.writerow(['Border', 'Date', 'Measure', 'Value', 'Average'])
            self._write_all_rows(row_writer, sort_dir_rev)
             
    # Calc the running average, save as 'run_average' in _border_dict[date][border][meas]         
    def _calc_run_average(self):
        dates = sorted(self._border_dict.keys())
        # keep track of the running totals with prev_dict[border][meas]=int
        prev_dict = self._n_level_defaultdict(int,2) 
        for k, date in enumerate(dates):
            borders = sorted(set(self._border_dict[date].keys()))
            for border in borders:
                measures = sorted(set(self._border_dict[date][border].keys()))
                for meas in measures:
                    c_total = self._border_dict[date][border][meas]['total']
                    run_average = 0
                    if meas in prev_dict[border] and k>0:
                        p_total = prev_dict[border][meas]
                        # 0.1 is for round up for *.5 => *.6
                        run_average = round(0.1 + (p_total / k) ) 
                    self._border_dict[date][border][meas]['run_average'] = run_average
                    prev_dict[border][meas] += c_total                 
    
    # make a nested defaultdict of type date_type, with n_nest levels
    def _n_level_defaultdict(self, data_type, n_nest):
        n_level_dict = partial(defaultdict, data_type)
        for _ in range(n_nest-1):
            n_level_dict = partial(defaultdict, n_level_dict)
        return n_level_dict()

    # read date_string with format _timedate_format, returns None if format is incorrect
    def _read_date(self, date_string):
        try:
            output = datetime.datetime.strptime(date_string, self._timedate_format).date()
            # round all dates to first day of the month
            return datetime.date(output.year, output.month, 1)
        except ValueError:
            print('Error reading date: {}'.format(date_string))
            return None
    
    # converts datetime object into a str with format _timedate_format
    def _write_date(self, date_object):
        return date_object.strftime(self._timedate_format)
    
    # adds value into _border_dict, skips dates that don't conform to _timedate_format
    def _add_row_data(self, border_str, date_str, measure_str, value_str):
        date = self._read_date(date_str)
        if date is not None:
            self._border_dict[date][border_str][measure_str]["total"] += int(value_str)

    # reads all the rows in the row_reader object with columns Border, Date, Measure, Value
    def _read_all_rows(self, row_reader):
        for row in row_reader:
            border = row['Border']
            date = row['Date']
            measure = row['Measure']
            value = row['Value']
            self._add_row_data(border, date, measure, value)
    
    # loops through _border_dict in descending order if sort_dir_rev = True
    def _write_all_rows(self, row_writer, sort_dir_rev):    
        dates = set(self._border_dict.keys())
        dates = sorted(self._border_dict.keys(), reverse=sort_dir_rev)
        for date in dates:
            borders = sorted(self._border_dict[date].keys(), reverse=sort_dir_rev)
            for border in borders:
                measures = sorted(self._border_dict[date][border].keys(), reverse=sort_dir_rev)
                for meas in measures:
                    c_total = self._border_dict[date][border][meas]['total']
                    run_avg = self._border_dict[date][border][meas]['run_average']
                    output = [border, self._write_date(date), str(meas), 
                        str(c_total), str(run_avg)]
                    row_writer.writerow(output)
                   
# run this script as: border_analytics.py input_file output_file
if __name__ == '__main__':
    input_file = sys.argv[1] 
    output_file = sys.argv[2]  
    bc = BorderCrossing(input_file)
    bc.write_file(output_file)

    

    
    
    