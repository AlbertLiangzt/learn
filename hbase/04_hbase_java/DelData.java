import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Delete;
import org.apache.hadoop.hbase.client.HTable;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;


public class DelData {
    public static final String TABLE_NAME = "m_table";
    public static Configuration conf = HBaseConfiguration.create();
    public static HTable table;

    public static void delData(String rowKey) throws IOException {
        table = new HTable(conf, TABLE_NAME);
        List<Delete> list = new ArrayList<Delete>();
        Delete delete = new Delete(rowKey.getBytes());

        list.add(delete);
        table.delete(list);

        System.out.println("----------delete----------rowKey:" + rowKey + "----------success!----------");

    }

    public static void main(String[] args) {
        conf.set("hbase:master", "192.168.224.10:60000");
        conf.set("hbase.zookeeper.quorum", "192.168.224.10, 192.168.224.11, 192.168.224.12");

        try {
            delData("1001");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }


}
