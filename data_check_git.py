#How to use:
#python data_recovery.py --output="<path/to/save/output>"

import argparse
import os
from datetime import datetime,date,timedelta
import io
from google.cloud import bigquery
import tarfile
import json,jsonschema
import subprocess
from jsonschema import validate
import ast
import requests

#--output is path to file stored in server, it can be a tgz file or a normal json/log file
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, help="output directory")
args = parser.parse_args()
if not os.path.isdir(args.output):
	print("Invalid output path")
	exit(2)

#Gets Date for yesterday
yesterday = date.today() - timedelta(1)

#Name of your BQ dataset
dataset = "dataset_name"

#List of tables to compare
tables = ["table_name1","table_name2","table_name3","table_name4"]

#Iterate over each entry in the list of tables mentioned above.
for table in tables:
	#Initiate count of rows for each table:
	tgzRows = 0
	for values in range(1,4):
		filepath = args.output + '/' + table + '-' + str(yesterday.year) + '-' + str(yesterday.month) + '-'+ str(yesterday.day) + '-' + str(values) + '.tgz'
		print("Filepath: ",filepath)
		tar = tarfile.open(filepath, "r:*")
		for member in tar.getmembers():
			f = tar.extractfile(member)
			for line in f:
				lines = line.decode("utf-8")
				tgzRows += 1
	print ("Total Rows:", tgzRows)
	
	
	#Count lines in the original bq partition and clean the string
	bqLinesCmd = ("bq query --quiet --format=csv 'SELECT COUNT(1) FROM " + dataset + "." + table + " WHERE _PARTITIONTIME = TIMESTAMP(\"" + str(yesterday.strftime('%Y-%m-%d')) + "\")'  | awk '{if(NR>1)print}'")
	
	#Convert the above bqLinesCmd resut into integer
	bqRows = int(subprocess.check_output(bqLinesCmd, shell=True).decode("utf-8"))
	print('BQ Rows: ', bqRows)
	
	#Compare if Bq Rows are not equal to the raw data Rows.
	if bqRows != tgzRows:
		slack_data = "Rows Mismatch in "
	#Compare if Bq Rows are equal to the raw data Rows.
	else:
		slack_data = "Everything is fine in "
	
	#Send/post a slack notification to bq_triggers channel on slack. You might want to set this slack channel up and get the slack hook for the channel which is then used in the below command. 
	os.system("curl -X POST --data-urlencode 'payload={\"channel\": \"#bq_triggers\", \"username\": \"webhookbot\", \"text\": \"" + str(yesterday) +": " + slack_data + table + "\", \"icon_emoji\": \":ghost:\"}' https://hooks.slack.com/services/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")