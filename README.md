# python-csv-dictwriter
Playbook for converting Python dictionary into CSV file (e.g. when ingesting Rest API into Redshift tables)

Python CSV library provides nice functionality to convert Python dictionary to CSV file output.  In particular:
* The csv.DictWriter() class takes multiple parameters that are useful 
* The parameter "f" is the path to CSV file output
* The parameter "fieldnames" is a list of dictionary keys, order of columns in CSV
* The parameter "extrasaction" indicates what action to take if the dictionary keys do not completely match the "fieldnames" (e.g. some keys not included in fieldnames)
* The parameter "dialect" customizes delimiter and quotes

### Reference: 
* https://docs.python.org/3/library/csv.html#csv.DictWriter
