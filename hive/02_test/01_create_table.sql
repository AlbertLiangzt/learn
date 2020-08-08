CREATE TABLE rating_table(
userid string,
movieid string,
rating string,
ts string
)
row format delimited fields terminated by ','
stored as textfile
location '/rating_table';
