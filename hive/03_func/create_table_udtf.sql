create table udtf_table(
id_score string
)
row format delimited fields terminated by '\t'
stored as textfile
location '/udtf_test'
