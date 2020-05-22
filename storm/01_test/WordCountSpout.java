import backtype.storm.spout.SpoutOutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.IRichSpout;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichSpout;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Values;

import java.util.Map;
import java.util.Random;

public class WordCountSpout extends BaseRichSpout implements IRichSpout {
    SpoutOutputCollector outputCollector;

    @Override
    public void open(Map conf, TopologyContext context, SpoutOutputCollector collector) {
        outputCollector = collector;
    }

    @Override
    public void close() {

    }

    @Override
    public void activate() {

    }

    @Override
    public void deactivate() {

    }

    /**
     * 将数据随机发送
     */
    @Override
    public void nextTuple() {
        String[] words = new String[]{"how do you do", "how you doing", "do you know", "I do not know"};
        Random rand = new Random();
        String word = words[rand.nextInt(words.length)];

        Object msgid = rand.hashCode();
        System.out.println("msgid: " + msgid);

        outputCollector.emit("spout_stream", new Values(word), msgid);

        // 控制入口流量
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void ack(Object msgid) {
        System.out.println("Receive Ack---, msgid: " + msgid);
    }

    @Override
    public void fail(Object msgid) {
        System.out.println("Receive Fail---, msgid: " + msgid);
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer declare) {
        declare.declareStream("spout_stream", new Fields("sentence"));
    }

    @Override
    public Map<String, Object> getComponentConfiguration() {
        return null;
    }
}
