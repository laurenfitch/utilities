import argparse
import subprocess
import json

parser = argparse.ArgumentParser(description = "Search all accessible Amazon S3 buckets for filename matching input string.")
parser.add_argument("search_string", metavar = "S", type = str, 
	help = "The string to search for matching file names.")
args = parser.parse_args()

cmd_get_buckets = "aws s3api list-buckets"

process = subprocess.Popen(cmd_get_buckets.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

response = json.loads(output.decode())

buckets = response["Buckets"]

for bucket in buckets:
	name = bucket["Name"]
	cmd_search_bucket = "aws s3 ls s3://" + name + " --recursive"
	process = subprocess.Popen(cmd_search_bucket.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()
	bucket_response = output.decode()
	br_lines = bucket_response.splitlines()
	for line in br_lines:
		if args.search_string in line:
			print(name, line)