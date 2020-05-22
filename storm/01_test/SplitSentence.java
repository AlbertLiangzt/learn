import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.tuple.Tuple;
import backtype.storm.tuple.Values;

import java.util.Map;

public class SplitSentence extends BaseRichBolt {
    OutputCollector outputCollector;

    @Override
    public void prepare(Map stormConf, TopologyContext context, OutputCollector collector) {
        outputCollector = collector;
    }

    /**
     * 模拟一个失败的场景，其他正常，并按空格分隔、输出
     *
     * @param input
     */
    @Override
    public void execute(Tuple input) {
        String sentence = input.getString(0);
        System.out.println("sentence: " + sentence);

        if ("how do you do".equals(sentence)) {
            outputCollector.fail(input);
        } else {
            for (String word : sentence.split(" ")) {
                outputCollector.emit("split_stream", new Values(word));
            }
            outputCollector.ack(input);
        }

    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {

    }
}
