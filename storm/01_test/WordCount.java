import backtype.storm.Config;
import backtype.storm.LocalCluster;
import backtype.storm.StormSubmitter;
import backtype.storm.generated.AlreadyAliveException;
import backtype.storm.generated.InvalidTopologyException;
import backtype.storm.topology.TopologyBuilder;
import backtype.storm.tuple.Fields;

public class WordCount {
    public static void main(String[] args) {
        TopologyBuilder builder = new TopologyBuilder();

        builder.setSpout("1", new WordCountSpout(), 3);
        builder.setBolt("2", new SplitSentence(), 5)
                .shuffleGrouping("1", "spout_stream");
        builder.setBolt("3", new WordCountBolt(), 5)
                .fieldsGrouping("2", "split_stream", new Fields("word"));

        Config conf = new Config();
        conf.setDebug(false);

        if (args[0].equals("local")) {
            LocalCluster localCluster = new LocalCluster();
            localCluster.submitTopology("WordCount_local_demo", conf, builder.createTopology());
        } else {
            try {
                StormSubmitter.submitTopology("WordCount_cluster_demo", conf, builder.createTopology());
            } catch (AlreadyAliveException e) {
                System.out.println("[AlreadyAliveException] error:" + e);
            } catch (InvalidTopologyException e) {
                System.out.println("[InvalidTopologyException] error:" + e);
            }
        }
    }

}
