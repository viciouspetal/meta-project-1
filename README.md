### How to run

```
python TSP_toStudents.py <filename>
```

#### Example
```
python TSP_toStudents.py ./dataset/inst-0.tsp
```

```
python TSP_toStudents.py ./dataset/inst-13.tsp
```

```
python3 TSP_toStudents.py ./dataset/inst-16.tsp
```

### Gathering data for additional experiments
In order to gather all the data for additional experiments run
```
python experminet_gathering.py <filename> >> <file_to_gather_results_into>
```
for example
```
python experminet_gathering.py ./dataset/inst-0.tsp inst-0-complete-results.txt
```
Omitting the `filename` parameter will result in an error, as the program will be missing input data to run experiments on. 
Omitting the `file_to_gather_results_into` will result in the entire experiment run, the whole 
6 configurations x 4 iterations x4 mutation rates x3 population sizes, aka 288 different results, times at least 6 files for each run ~1700 lines of text into the console.

Any results produced by above would be quite tedious to sift through manually, so it is recommended to redirect to a file instead.
Additionally, windows console can potentially overflow and truncate the data from the first experiments. 


The program will proceed to run all 6 configurations for 4 iterations, with gradually increasing first the mutation rate in step 0.2.
Additionally same mutation variation experiment will be run for varying population of 150 and 50.


### Processing the results
Results parser script can be used to produce a csv file for each of the result files from the additional experiments.
To run, first change the 'change-to-filename' parameter at the top of `resuls_parser.py` then execute

```
python results_parser.py >> <results-file.csv>
```

It works by redirecting the console statements to a file so omitting specifying a `results-file` file result in priting to the console instead.  