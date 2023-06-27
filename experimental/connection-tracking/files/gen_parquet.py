from datetime import datetime
import json
import os
import sys
import time
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np
import boto3

DEBUG=True
AWS_PROFILE=foo
BUCKET=bar
PREFIX=CONNLOGS

def debug(message):
    if DEBUG == True:
        print(message)

while True:
    files = os.listdir(".")
    files.sort()

    json_file = ""

    for file in files:
        if 'ulogd.json-' in file:
            json_file = file
            time_stamp_str = json_file.split("-")[1]
            time_stamp_int = int(time_stamp_str)

    if json_file == "":
        debug("No JSON files found. Sleeping.")
        time.sleep(30)
        continue

    print("Found ulog JSON file of " + json_file)

    with open(json_file) as f:
        json_lines = f.readlines()

    # Define the columns as used by AWS for VPC Flowlogs, version 2:
    # https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html#flow-logs-fields
    p_version      = []
    p_account_id   = []
    p_interface_id = []
    p_srcaddr      = []
    p_dstaddr      = []
    p_srcport      = []
    p_dstport      = []
    p_protocol     = []
    p_packets      = []
    p_bytes        = []
    p_start        = []
    p_end          = []
    p_action       = []
    p_log_status   = []
    names = ["version", "account-id", "interface-id", "srcaddr",
             "dstaddr", "srcport", "dstport", "protocol", "packets",
             "bytes", "start", "end", "action", "log-status"]

    for line in json_lines:
        try:
            ulog_inputs = json.loads(line)
            key_missing = False

            # We must test the existance of all needed keys from the JSON

            keys = ["oob.out", "src_ip", "dest_ip", "src_port", 
                    "dest_port", "ip.protocol", "raw.pktcount",
                    "raw.pktlen", "oob.time.sec"]

            for key in keys:
                if key not in ulog_inputs:
                    debug("Key: " + key + " missing. Skipping this entry.")
                    key_missing = True
 
            if key_missing == False:
                p_version.append(np.int32(2))
                p_account_id.append("account") #TODO: get account info
                p_interface_id.append(ulog_inputs["oob.out"])
                p_srcaddr.append(ulog_inputs["src_ip"]) #TODO: match subnets
                p_dstaddr.append(ulog_inputs["dest_ip"])
                p_srcport.append(np.int32(ulog_inputs["src_port"]))
                p_dstport.append(np.int32(ulog_inputs["dest_port"]))
                p_protocol.append(np.int32(ulog_inputs["ip.protocol"]))
                p_packets.append(np.int64(ulog_inputs["raw.pktcount"]))
                p_bytes.append(np.int64(ulog_inputs["raw.pktlen"]))
                p_start.append(np.int64(ulog_inputs["oob.time.sec"]))
                p_end.append(np.int64(0)) #TODO: verify this cannot be calculated by the data given
                p_action.append("ACCEPT")
                p_log_status.append("OK")

        except Exception as e:
            print(e)

    parquet_schema = pa.schema([('version', pa.int32()),
                                ('account-id', pa.string()),
                                ('interface-id', pa.string()),
                                ('srcaddr', pa.string()),
                                ('dstaddr', pa.string()),
                                ('srcport', pa.int32()),
                                ('dstport', pa.int32()),
                                ('protocol', pa.int32()),
                                ('packets', pa.int64()),
                                ('bytes', pa.int64()),
                                ('start', pa.int64()),
                                ('end', pa.int64()),
                                ('action', pa.string()),
                                ('log-status', pa.string())
                               ])

    table = pa.Table.from_arrays([p_version, p_account_id,
                                  p_interface_id, p_srcaddr, p_dstaddr,
                                  p_srcport, p_dstport, p_protocol,
                                  p_packets, p_bytes, p_start, p_end,
                                  p_action, p_log_status], names=names)

    pqwriter = pq.ParquetWriter(time_stamp_str + ".parquet", schema=parquet_schema, compression='gzip')
    pqwriter.write_table(table)
    pqwriter.close()

    # to read file:
    # (requires pandas)
    # pq.read_table(time_stamp_str + ".parquet").to_pandas()

    year = datetime.utcfromtimestamp(time_stamp_int).strftime("%Y")
    month = datetime.utcfromtimestamp(time_stamp_int).strftime("%m")
    day = datetime.utcfromtimestamp(time_stamp_int).strftime("%d")
    hour = datetime.utcfromtimestamp(time_stamp_int).strftime("%H")
    minute = datetime.utcfromtimestamp(time_stamp_int).strftime("%M")
    second = datetime.utcfromtimestamp(time_stamp_int).strftime("%S")

    session = boto3.Session(profile_name=AWS_PROFILE)

    s3_client = session.client('s3')

    s3_client.upload_file(time_stamp_str + ".parquet", BUCKET,
                          PREFIX + year + "/" + month + "/" + day + "/" + hour + "-" + minute + "-" + time_stamp_str + ".parquet")

    os.remove(json_file)
    os.remove(time_stamp_str + ".parquet")

    print("done")

    break
