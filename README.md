# Parsing Flow Log Data 

## Overview 
The main functionality can be found in `src/mapping.py`. 
I used the Python defaulty library `csv` and implemented four functions. 
### parse_protocol_map(filename)
This function maps the decimal protocol number to the protocol name. I used the [Internet Assigned Numbers Authority ](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml) in a csv format and passed it into the function once downloaded. 

### parse_lookup(filename)
This function creates a `lookup` map created after parsing the lookup table passed into the function. Each key was a tuple `(dstport, protocol)` mapping to a `tag` value. 

### parse_log_data(filename)
This function parses the flow log data and outputs two maps, `tag_matches` and `port_protocol_matches`. Each map contains the count of matches for each `tag` or `(port, protocol)` combination. 

### write_results(filename)
This function uses the output from `parse_log_data` and writes it to `filename`. 


## Instructions on How to Run Program 

1. Navigate to `src/testing.py` 
2. Run the program to execute a few of the test cases, including what was provided as a sample. 
3. Navigate to the `tests` directory to find the results files

### To Parse Other Records 
1. Navigate to the bottom of `src/testing.py`

```bash
if __name__ == "__main__":
    unittest.main()
    testing = TestMapping() 

    flow_log_filename = ""
    lookup_filename = ""
    results_filename = ""
    testing.test_mapping_general(flow_log_filename, lookup_filename, results_filename)
```
2. Set `flow_log_filename` to the file of the flow log data we want to pass in
3. Do the same for `lookup_filename` and `results_filename`
4. Then, run the program and find the output `results_filename` in the `tests` directory

## Tests 
I conducted some smaller tests, all of which can be found in `src/testing.py`. I manually verified the accuracy of the results file given I used a smaller subset of data. 

I also utilized the sample lookup table and flow log data provided in the instructions to guide my coding process, primarily testing with those and manually cross-checking. 

If I had more time, I would want to pass in larger datasets to test if my code can handle an input size of up to 10 MB with a lookup table having at most 10000 mappings. 

I had some challenges in finding flow log data with corresponding lookup tables and also how to verify my code produces the right output without manually determining so. 

## Assumptions
I assumed the input files, which include the flow log data and lookup tables, were well-formatted. Specifically, for the lookup table, I assumed the first line includes:  
```
dstport,protocol,tag
```


Followed by the data separated by commas. However, my code strips the data of any leading or trailing whitespaces and defaults to lowercase to accommodate for case insensitivity. 

For the flow log data, I assumed each record or row has no leading whitespace and each field is separated by whitespace to easily retrieve the `dstport` and `protocol` number in the 7th and 8th fields respectively. 
