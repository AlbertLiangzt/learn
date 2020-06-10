package stormHbase;

import backtype.storm.Config;
import backtype.storm.LocalCluster;
import backtype.storm.StormSubmitter;
import backtype.storm.spout.SchemeAsMultiScheme;
import backtype.storm.topology.TopologyBuilder;
import storm.kafka.*;
import stormKafka.PrinterBolt;

public class StormKafka {
    public static void main(String[] args) throws Exception {
        String topic = "storm_kafka";
        String zkRoot = "/storm_kafka";
        String spoutId = "kafkaSpout";

        BrokerHosts brokerHosts = new ZkHosts("master:2181");
        SpoutConfig kafkaConf = new SpoutConfig(brokerHosts, topic, zkRoot, spoutId);
        kafkaConf.forceFromStart = true;
        kafkaConf.scheme = new SchemeAsMultiScheme(new StringScheme());

        KafkaSpout kafkaSpout = new KafkaSpout(kafkaConf);

        TopologyBuilder topoBuilder = new TopologyBuilder();
        topoBuilder.setSpout("spout", kafkaSpout, 2);
        topoBuilder.setBolt("printer", new PrinterBolt())
                .shuffleGrouping("spout");

        Config conf = new Config();
        conf.setDebug(false);

        if (null != args && args.length > 0) {
            conf.setNumWorkers(3);
            StormSubmitter.submitTopology(args[0], conf, topoBuilder.createTopology());
        } else {
            conf.setMaxTaskParallelism(3);
            LocalCluster cluster = new LocalCluster();
            cluster.submitTopology("kafka", conf, topoBuilder.createTopology());
        }

    }
}
