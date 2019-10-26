# Border Crossing Analysis

### Ian Finneran (ifinn505@gmail.com)

## Table of Contents
1. [Problem from Insight](README.md#Problem-from-Insight)
1. [Solution Overview](README.md#Solution-Overview)
1. [Algorithm](README.md#Algorithm)
1. [Tests](README.md#Tests)
1. [Input Output Format](README.md#Input-Output-Format)
1. [Repo Directory Structure](README.md#Repo-Directory-Structure)

## Problem from Insight
The Bureau of Transportation Statistics regularly makes available data on the number of vehicles, equipment, passengers and pedestrians crossing into the United States by land.

**For this challenge, we want to you to calculate the total number of times vehicles, equipment, passengers and pedestrians cross the U.S.-Canadian and U.S.-Mexican borders each month. We also want to know the running monthly average of total number of crossings for that type of crossing and border.**

## Solution Overview

I used Python 3.7 and packages from the Python Standard Library. My solution is a class called BorderCrossing in the border_analytics.py file. It can be run as a script (with a default descending sort order):

```   
python3.7 border_analytics.py input_file output_file
``` 

Alternatively, the class the can be imported and used as follows:

1. Make BorderCrossing object bc with csv input file with fields including 'Border', 'Date', 'Measure', 'Value'. 

```    
bc = BorderCrossing(input_file)
```   
   
The default format for the date entry in input_file is ```'%m/%d/%Y %I:%M:%S %p'``` using Python's datetime package. This can be modified with the class variable ```_timedate_format```.
   
1. Write the monthly totals to output csv file:
   
```   
bc.write_file(output_file, sort_dir_rev=True)
```
The sorting order is determined by sort_dir_rev:     
sort_dir_rev = True: sorted descending
sort_dir_rev = False: sorted ascending
   

## Algorithm

Here are the steps of the algorithm with some notes on implementation/performance:

1. The border data is read from the csv file. Each line is stored in a nested dictionary with layers given by ```[date][border][measure][value]=integer``` where integer is the value associated with a row.

Notes: 

- I chose the dictionary data type because it is fast for looking up values, and it logically fits the format of the data. One downside is that it is unordered, but the keys can be converted to sets and ordered. Alternatively, I could have used the OrderedDict type. I chose defaultdict instead, because of its ability to quickly add new values. 

- One limitation of this implementation is that it will run out of memory if the input file and resulting dictionary are too big. In that case, the class would have to be rewritten to use disk space rather than memory. The advantage of the memory-based approach is that it will be faster for medium-sized data sets that can fit into memory.

- Dates are stored as datetime objects, so they can be sorted. Rows with invalid dates (e.g. ```91/31/2019 12:00:00```) are skipped and displayed to the user. Dates are rounded to the 1st day of each month.

- I read and load the file into the dictionary line by line so that I use minimal memory.

1. The running monthly average of the data is computed. 

Notes:

- The average is started from the first date in the data. For example, if there are entries for the US-Mexico border, but not entries for the US-Canada border for the first 3 months, the running average for US-Canada will start from the US-Mexico first date.

- The running average is rounded to the nearest int by dividing the running total by the months from the start. 
 
- In order to minimize compute time and memory usage, the program only loops through the dictionary once and keeps track of the months since the first month and the running totals of each measure. The dict keys are sorted ascending at each layer, and the running average entry is added to the dict one at a time at ```[date][border][measure]['run_avgerage']```.

1. The dictionary results are sorted and output to a csv file.

Notes:

- The program loops through the dictionary, and sorts by descending at each layer. The csv file is written line by line to save memory.

- If the user wanted an ascending order, then the data could have been written to file in the previous step. This would save time (one loop through the dict).

## Tests

Here is a short description of the tests in the insight_testsuite/tests directory:

1. The original insight test
1. One line has been edited to have an invalid date: 
    ```Hidalgo,Texas,2305,US-Mexico Border,02/91/2019 12:00:00 AM,Pedestrians,156891,POINT (-98.26278 26.1)```
    The program skips this line resulting in a sum for February that is less by 156891.
1. One date has been changed to be not the first of the month:
    ```Eagle Pass,Texas,2303,US-Mexico Border,01/31/2019 12:00:00 AM,Pedestrians,56810,POINT (-100.49917 28.70889)```
    The program still gives the same output as the first test, since dates are rounded to the first of the month.
1. Two copies of the original insight test. The program should have 2 times the values on the output.
1. Three different borders all with the same pedestrian traffic. The program should give the same numbers for all of them by month.
1. Two different borders and two different measures.
1. Same as original but zeros for all values.

## Requirements

- Python 3.7 with Standard Library Packages:
    - csv
    - sys
    - datetime
    - collections
    - functools
    - itertools

## Input Output Format

### Example Input File

```
Port Name,State,Port Code,Border,Date,Measure,Value,Location
Derby Line,Vermont,209,US-Canada Border,03/01/2019 12:00:00 AM,Truck Containers Full,6483,POINT (-72.09944 45.005)
Norton,Vermont,211,US-Canada Border,03/01/2019 12:00:00 AM,Trains,19,POINT (-71.79528000000002 45.01)
Calexico,California,2503,US-Mexico Border,03/01/2019 12:00:00 AM,Pedestrians,346158,POINT (-115.49806000000001 32.67889)
Hidalgo,Texas,2305,US-Mexico Border,02/01/2019 12:00:00 AM,Pedestrians,156891,POINT (-98.26278 26.1)
Frontier,Washington,3020,US-Canada Border,02/01/2019 12:00:00 AM,Truck Containers Empty,1319,POINT (-117.78134000000001 48.910160000000005)
Presidio,Texas,2403,US-Mexico Border,02/01/2019 12:00:00 AM,Pedestrians,15272,POINT (-104.37167 29.56056)
Eagle Pass,Texas,2303,US-Mexico Border,01/01/2019 12:00:00 AM,Pedestrians,56810,POINT (-100.49917 28.70889)
```

### Example Output File

```
Border,Date,Measure,Value,Average
US-Mexico Border,03/01/2019 12:00:00 AM,Pedestrians,346158,114487
US-Canada Border,03/01/2019 12:00:00 AM,Truck Containers Full,6483,0
US-Canada Border,03/01/2019 12:00:00 AM,Trains,19,0
US-Mexico Border,02/01/2019 12:00:00 AM,Pedestrians,172163,56810
US-Canada Border,02/01/2019 12:00:00 AM,Truck Containers Empty,1319,0
US-Mexico Border,01/01/2019 12:00:00 AM,Pedestrians,56810,0

```

## Repo Directory Structure

    ├── README.md
    ├── run.sh
    ├── src
    │   └── border_analytics.py
    ├── input
    │   └── Border_Crossing_Entry_Data.csv
    ├── output
    |   └── report.csv
    ├── insight_testsuite
        └── run_tests.sh
        └── tests
            └── test_1
            |   ├── input
            |   │   └── Border_Crossing_Entry_Data.csv
            |   |__ output
            |   │   └── report.csv
            └── test_2
            |   ├── input
            |   │   └── Border_Crossing_Entry_Data.csv
            |   |__ output
            |   │   └── report.csv
            └── test_3
            |   ├── input
            |   │   └── Border_Crossing_Entry_Data.csv
            |   |__ output
            |   │   └── report.csv
            └── test_4
            |   ├── input
            |   │   └── Border_Crossing_Entry_Data.csv
            |   |__ output
            |   │   └── report.csv
            └── test_5
            |   ├── input
            |   │   └── Border_Crossing_Entry_Data.csv
            |   |__ output
            |   │   └── report.csv
            └── test_6
            |   ├── input
            |   │   └── Border_Crossing_Entry_Data.csv
            |   |__ output
            |   │   └── report.csv
            └── test_7
            |   ├── input
            |   │   └── Border_Crossing_Entry_Data.csv
            |   |__ output
            |   │   └── report.csv
