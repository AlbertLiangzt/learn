HADOOP_CMD="/usr/local/src/hadoop-2.6.5/bin/hadoop"
STREAM_JAR_PATH="/usr/local/src/hadoop-2.6.5/share/hadoop/tools/lib/hadoop-streaming-2.6.5.jar"

INPUT_FILE_PATH="/music_uis.data"
OUTPUT_PATH_1="/output1"
OUTPUT_PATH_2="/output2"
OUTPUT_PATH_3="/output3"

$HADOOP_CMD fs -rmr -skipTrash $OUTPUT_PATH_1
$HADOOP_CMD fs -rmr -skipTrash $OUTPUT_PATH_2
$HADOOP_CMD fs -rmr -skipTrash $OUTPUT_PATH_3

# ster1
$HADOOP_CMD jar $STREAM_JAR_PATH \
	-input $INPUT_FILE_PATH \
	-output $OUTPUT_PATH_1 \
	-mapper "python map_1_normalized.py" \
	-reducer "python reduce_1_normalized.py" \
	-file ./map_1_normalized.py \
	-file ./reduce_1_normalized.py 

# step2
$HADOOP_CMD jar $STREAM_JAR_PATH \
	-input $OUTPUT_PATH_1 \
	-output $OUTPUT_PATH_2 \
	-mapper "python map_2_pair.py" \
	-reducer "python reduce_2_pair.py" \
	-file ./map_2_pair.py \
	-file ./reduce_2_pair.py

# step3
$HADOOP_CMD jar $STREAM_JAR_PATH \
	-input $OUTPUT_PATH_2 \
	-output $OUTPUT_PATH_3 \
	-mapper "python map_3_sum.py" \
	-reducer "python reduce_3_sum.py" \
	-file ./map_3_sum.py \
	-file ./reduce_3_sum.py

