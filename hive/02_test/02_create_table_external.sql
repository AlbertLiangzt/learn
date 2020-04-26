CREATE EXTERNAL TABLE movie_table(
movieid string,
title string,
genres string
)
row format delimited fields terminated by ','
stored as textfile
