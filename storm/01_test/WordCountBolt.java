import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.tuple.Tuple;

import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

public class WordCountBolt extends BaseRichBolt {
    OutputCollector outputCollector;

    public Map<String, Integer> countMap = new HashMap<>();

    @Override
    public void prepare(Map stormConf, TopologyContext context, OutputCollector collector) {
        outputCollector = collector;
    }

    @Override
    public void execute(Tuple input) {
        String word = input.getString(0);
        System.out.println("word: " + word);

        Integer count = this.countMap.get(word);
        if (null == count) {
            count = 0;
        }
        count++;
        this.countMap.put(word, count);

        Iterator<String> iterator = this.countMap.keySet().iterator();
        while (iterator.hasNext()) {
            String next = iterator.next();
            System.out.println(next + ":" + this.countMap.get(next));
        }

        outputCollector.ack(input);
    }

    @Override
    public void cleanup() {

    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {

    }

    @Override
    public Map<String, Object> getComponentConfiguration() {
        return null;
    }
}
