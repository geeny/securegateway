CREATE EXTERNAL TABLE IF NOT EXISTS test_table_vpclogs (
  version int,
  account_id string,
  interface_id string,
  srcaddr string,
  dstaddr string,
  srcport int,
  dstport int,
  protocol bigint,
  packets bigint,
  bytes bigint,
  start bigint,
  `end` bigint,
  action string,
  log_status string
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ' '
STORED AS PARQUET
LOCATION 's3://BUCKET_NAME/device-flow-logs/'
TBLPROPERTIES
(
"skip.header.line.count"="1",
"projection.enabled" = "true",
"projection.day.type" = "date",
"projection.day.range" = "2021/01/01,NOW",
"projection.day.format" = "yyyy/MM/dd"
)

select * from test_table_vpclogs where protocol = 6 and not dstaddr = '10.100.30.2';
