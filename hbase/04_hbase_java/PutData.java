import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;

public class PutData {
    public static final String TABLE_NAME = "m_table";
    public static final String ColumnFamily = "meta_data";

    public static Configuration conf = HBaseConfiguration.create();
    public static HTable table;

    public static void insData(String rowKey, String family, String qualifier, String value) throws IOException {
        table = new HTable(conf, TABLE_NAME);
        Put put = new Put(Bytes.toBytes(rowKey));
        put.add(Bytes.toBytes(family), Bytes.toBytes(qualifier), Bytes.toBytes(value));
        table.put(put);
        System.out.println("insert data " + rowKey + " to table " + TABLE_NAME + " success");

    }

    public static void main(String[] args) {
        conf.set("hbase:master", "192.168.224.10:60000");
        conf.set("hbase.zookeeper.quorum", "192.168.224.10, 192.168.224.11, 192.168.224.12");

        try {
            insData("0517", ColumnFamily, "name", "Jack");
            insData("0517", ColumnFamily, "age", "17");
            insData("0517", ColumnFamily, "gender", "male");

            insData("0518", ColumnFamily, "name", "Mike");
            insData("0518", ColumnFamily, "age", "28");
            insData("0518", ColumnFamily, "gender", "male");

            insData("0519", ColumnFamily, "name", "Rose");
            insData("0519", ColumnFamily, "age", "16");
            insData("0519", ColumnFamily, "gender", "female");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
