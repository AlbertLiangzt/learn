set hive.enforce.bucketing=true;
CREATE TABLE rating_table_bucket(
userid string,
movieid string,
rating string
)
clustered by (userid) INTO 16 buckets
