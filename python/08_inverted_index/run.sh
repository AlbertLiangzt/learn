
HADOOP_CMD="/usr/local/src/hadoop-2.6.5/bin/hadoop"
STREAM_JAR_PATH="/usr/local/src/hadoop-2.6.5/share/hadoop/tools/lib/hadoop-streaming-2.6.5.jar"

INPUT_FILE_PATH_1="/music_meta.txt.small"
OUTPUT_PATH_1="/output_step1"
OUTPUT_PATH_2="/output_step2"

$HADOOP_CMD fs -rmr -skipTrash $OUTPUT_PATH_1
$HADOOP_CMD fs -rmr -skipTrash $OUTPUT_PATH_2

# Step 1.
$HADOOP_CMD jar $STREAM_JAR_PATH \
	-input $INPUT_FILE_PATH_1 \
	-output $OUTPUT_PATH_1 \
	-mapper "python map_1_name_token.py" \
	-jobconf "mapred.reduce.tasks=0" \
	-jobconf "mapred.job.name=jieba_fenci_demo" \
	-file "./jieba.tar.gz" \
	-file "./map_1_name_token.py"

# Step 2.
$HADOOP_CMD jar $STREAM_JAR_PATH \
	-input $OUTPUT_PATH_1 \
	-output $OUTPUT_PATH_2 \
	-mapper "python map_2_token_name.py" \
	-reducer "python reduce.py" \
	-jobconf "mapred.job.name=jieba_fenci" \
	-file "./map_2_token_name.py" \
	-file "./reduce.py"

