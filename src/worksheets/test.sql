
-- create a sample connection
create connection s3 sqlake_action_test_conn
   aws_role = 'arn:aws:iam::433987883887:role/royon_ro_role'
   external_id = 'ROYON'
;

-- create a sample table
CREATE TABLE default_glue_catalog.sqlake_action.test_table_1(
    source_account_id string,
    action string,
    bytes_sent string,
    source_ip_address string,
    source_port string,
    destination_ip_address string,
    destination_port string,
    first_packet_received_time timestamp,
    last_packet_received_time timestamp,
    interface_id string,
    log_status string,
    num_packets_transferred bigint,
    protocol double,
    flowlogs_version string,
    dt date
)
PARTITIONED BY dt
TABLE_DATA_RETENTION = 5 DAYS
COMPUTE_CLUSTER = "Default Compute"
;

-- drop the connection
drop connection sqlake_action_test_conn;

-- drop table
drop table default_glue_catalog.sqlake_action.test_table_1 
  DELETE_DATA = TRUE 
  COMPUTE_CLUSTER = "Default Compute";