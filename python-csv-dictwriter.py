# =========================================
# Filename:  python-csv-dictwriter.py
# =========================================
'''
This is useful when ingesting Rest API into Redshift table.
Assumes this code is run from AWS Lambda, e.g. /tmp/ folder used for CSV file output path.
'''

# create list of expected 
ls_rs_api_col = ['items', 'in', 'both', 'dict', 'and', 'redshift_cols']

# create copy of list of API keys
ls_api_copy = ls_api_keys.copy()

# create list of API keys to to filter/exclude from Redshift
ls_exclude_keys = ['description']

# create list of new API columns (i.e. not in Redshift) that are not expected/ignored
# if this list is not empty, it will be sent to SNS message notifying new columns
ls_api_copy_exclude_keys = [x for x in ls_api_copy if x not in ls_exclude_keys]
ls_cols_new_unexpected = [x for x in ls_api_copy_exclude_keys if x not in ls_rs_api_col]

if flag == 0:
  #empty output file just in case lambda runs again and tries to use same /tmp space
  if os.path.exists("/tmp/" + filename):
      os.remove("/tmp/" + filename)
      print("Removed the file %s" % "/tmp/" + filename)

  # To avoid sending the SNS message every time, just send it when flag == 0
  # if any new cols, send SNS message with new columns
  if len( ls_cols_new_unexpected )>0:

      subject_newcols = "Subject error message"
      str_lambda_function = "Name of Lambda function"
      message_newcols = f"The following are new columns in {str_lambda_function} Lambda function, not added to Redshift: {ls_cols_new_unexpected}"
      sendSNSNotification(subject_newcols, message_newcols, sns_failure_TopicArn)

      print("SNS re: new columns sent successfully.")

  else:
      print("Good news.  All of the API columns match the expected columns for Redshift.  None are new/unexpected columns.")
    
    #Write the data as Pipe delimited format
    csv.register_dialect('myDialect', delimiter = '|', quoting=csv.QUOTE_ALL)
    with open("/tmp/" + filename, 'a',newline = '',encoding = "utf-8-sig") as csvfile:

      #Initializing DictWriter
      writer = csv.DictWriter(csvfile, fieldnames=ls_header_reorder, extrasaction='ignore', dialect="myDialect")

      #Writes header only once when flag equals to zero
      if flag == 0:
          writer.writeheader()

      #Writing actual list
      writer.writerows(content_list)
