package stormHbase;

import backtype.storm.topology.BasicOutputCollector;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseBasicBolt;
import backtype.storm.tuple.Tuple;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.client.Result;

import java.io.IOException;

public class PrinterBolt extends BaseBasicBolt {
    public static final String TableName = "storm_hbase_table";
    public static Configuration conf = HBaseConfiguration.create();
    public static HTable table;

    public static void selectRowKey(String tableName, String rowKey) throws IOException {
        System.out.println("--------");
        table = new HTable(conf, tableName);
        System.out.println("--------");
        Get g = new Get(rowKey.getBytes());
        System.out.println("--------");
        Result res = table.get(g);
        System.out.println("--------");

        System.out.println("----row----" + new String(res.getRow()));

        for (Cell kv : res.rawCells()) {
            System.out.println("------" + new String(kv.getRow()) + "----");
            System.out.println("------Column Family: " + new String(kv.getFamily()));
            System.out.println("------Column       : " + new String(kv.getQualifier()));
            System.out.println("------value        : " + new String(kv.getValue()));
        }
    }


    @Override
    public void execute(Tuple tuple, BasicOutputCollector basicOutputCollector) {
        System.out.println(tuple.getString(0));
        conf.set("hbase.master", "192.168.224.10:60000");
        conf.set("hbase.zookeeper.quorum", "192.168.224.10, 192.168.224.11, 192.168.224.12");

        try {
            System.out.println("[1]=============");
            selectRowKey(TableName, tuple.getString(0));
            System.out.println("[2]=============");
        } catch (Exception e) {
            System.out.println("[3]=============");
            System.out.println(tuple);
            e.printStackTrace();
        }

    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer outputFieldsDeclarer) {

    }
}
