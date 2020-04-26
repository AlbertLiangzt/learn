CREATE TABLE rating_table_partition(
userid string,
movieid string,
rating string
)
partitioned by(dt STRING)
row format delimited fields terminated by '\t'
lines terminated by '\n'
