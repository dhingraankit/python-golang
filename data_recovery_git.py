#How to use:
#python data_recovery.py --output="<path/to/save/output>" --date="<yyyy-mm-dd for date to replace>" <dataset> <table>

import argparse
import os
import boto3
import botocore
from datetime import datetime
import io
from google.cloud import bigquery
import tarfile
import json,jsonschema
import subprocess
from jsonschema import validate
import ast

#Function to read a file
def readFile(filename):
	with open(filename,"r") as somefile:
		startIndex = somefile.index('{')
		endIndex = somefile.index('}') + 1 
		return ast.literal_eval(somefile[startIndex:endIndex])
		exit(1)
		
parser = argparse.ArgumentParser()

#pass dataset name as an argument while running
parser.add_argument("dataset", type=str, choices=['dataset_1','dataset_2'], 
					help="To work on this dataset")

#pass table name as an argument while running
parser.add_argument("table", type=str, choices=['table1','table2','table3','table4'], 
					help="To work on this table")

#pass dataset name as an argument while running
parser.add_argument("--output", type=str, help="output directory")
parser.add_argument('--date', type=lambda d: datetime.strptime(d, '%Y-%m-%d'), help="Date to replace for")
args = parser.parse_args()
if not os.path.isdir(args.output):
	print("Invalid output path")
	exit(2)

print("Table: ",args.table)
print("Date: ",args.date)
print("Year: ",args.date.year)
print("Month: ",args.date.month)
print("Day: ",args.date.day)

#Create partition date
partitionMonth = str("%02d"%args.date.month)
partitionDay = str("%02d"%args.date.day)
partitionDate = str(args.date.year) + partitionMonth + partitionDay
print("Partition Date: ", partitionDate)

#Download s3 logs from AWS.
BUCKET_NAME = '<BucketName>' # replace with your bucket name
for value in range(0,4):
	KEY = args.table + '-' + str(args.date.year) + '-' + str(args.date.month) + '-'+ str(args.date.day) + '-' + str(value) + '.tgz'
	PATH = 'bq/' + args.table + '/' + str(args.date.year) + '/' + str(args.date.month) + '/' + args.table + '-' + str(args.date.year) + '-' + str(args.date.month) + '-'+ str(args.date.day) + '-' + str(value) + '.tgz'
	print(KEY)
	print(PATH)	
	s3 = boto3.resource('s3')
	try:
	    s3.Bucket(BUCKET_NAME).download_file(PATH, KEY)
	except botocore.exceptions.ClientError as e:
	    if e.response['Error']['Code'] == "404":
	        print("The object does not exist.",e.response)
	        exit(3)
	    else:
	        raise

#Make a compiled json with this name.
compiledJsonName = args.table + partitionDate + ".json"

#Count rows in tgzFiles and append it for compiledJsonName one by one.
tgzRows = 0
with open(compiledJsonName, "a") as compiledJson:
	for values in range(0,4):
		filepath = args.output + '/' + args.table + '-' + str(args.date.year) + '-' + str(args.date.month) + '-'+ str(args.date.day) + '-' + str(values) + '.tgz'
		print("Filepath: ",filepath)
		tar = tarfile.open(filepath, "r:*")
		for member in tar.getmembers():
			f = tar.extractfile(member)
			for line in f:
				lines = line.decode("utf-8")
				tgzRows += 1
				compiledJson.write(lines)
print ("Total Rows:", tgzRows)

schemaName = args.table + "_schema.json"
tableSchema = os.system("bq show --format=prettyjson dataset_1." + args.table + " | jq '.schema.fields' > " + schemaName)


#Count lines in the original bq partition and convert to an integer.
bqLinesCmd = ("bq query --quiet --format=csv 'SELECT COUNT(1) FROM " + args.dataset+ "." + args.table + " WHERE _PARTITIONTIME = TIMESTAMP(\"" + str(args.date.strftime('%Y-%m-%d')) + "\")'  | awk '{if(NR>1)print}'")
bqRows = int(subprocess.check_output(bqLinesCmd, shell=True).decode("utf-8"))
print('BQ Rows: ', bqRows)


#Compare bqRows and tgzRows
if bqRows != tgzRows:
	#create empty partition table in dataset_2 as backup for replacement date.
	makeBackupTable = os.system("bq mk --time_partitioning_type=DAY dataset_2." + args.table + "_backup")
	print("Backup partition table created.")
	
	#Take backup to the above table
	print("bq query --use_legacy_sql=false --allow_large_results --replace --destination_table 'dataset_2." + args.table + "_backup$"+ partitionDate + "' 'SELECT * FROM dataset_1." + args.table + " WHERE _PARTITIONTIME = TIMESTAMP(\"" + str(args.date.strftime('%Y-%m-%d')) + "\")'")
	takeBackup = os.system("bq query --use_legacy_sql=false --allow_large_results --replace --destination_table 'dataset_2." + args.table + "_backup$"+ partitionDate + "' 'SELECT * FROM dataset_1." + args.table + " WHERE _PARTITIONTIME = TIMESTAMP(\"" + str(args.date.strftime('%Y-%m-%d')) + "\")'")
	
	#Replace partition with compiledJsonName using Schema for production table.
	print("bq load --replace --source_format=NEWLINE_DELIMITED_JSON '" + args.dataset + "." + args.table + "$"+ partitionDate + "' " + compiledJsonName + " " + schemaName)
	takeBackup = os.system("bq load --replace --source_format=NEWLINE_DELIMITED_JSON '" + args.dataset + "." + args.table + "$"+ partitionDate + "' " + compiledJsonName + " " + schemaName)

	#Remove files from the server.
	removeCompressedFiles = os.system("cd args.output | " + "rm " + args.table + "-" + str(args.date.year) + "-" + str(args.date.month) + "-" + str(args.date.day) + "-*.tgz")
	removeBQSchema = os.system("cd args.output | rm " + schemaName)
	removeCompiledJson = os.system("cd args.output | rm " + args.table + partitionDate + ".json")
else:
	#If bqRows and tgzRows are equal, do nothing.
	print("Everything seems. No need to replace the partition.")