# Python parquet code

This could can be found in `files/gen_parquet.py`

## What this code does

1 - Reads JSON from the current directory it is run from
2 - Validates that each JSON line has the required data. If a line does not, it skips.
3 - Creates gzipped parquet files
4 - Uploads them an S3 bucket

## What this code does NOT do

1 - Run as a deamon, or engage in any kind of persistent backgrounding
2 - Any form of AWS permissions management. It simply reads profile information in `.aws/credentials` via the `boto3` library
3 - Be async, multi-threaded, performant, etc. Not even close. This code has not been tested at scale.

## Further notes

The data is modeled after the VPC flow logs generated inside AWS. All tooling expecting the AWS specified flow log data fields should have no problems using this data.
