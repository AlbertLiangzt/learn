import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.client.Result;
import org.apache.log4j.BasicConfigurator;

import java.io.IOException;

public class GetData {
    public static final String TABLE_NAME = "m_table";

    public static Configuration conf = HBaseConfiguration.create();
    private static HTable table;

    public static void selectRowKey(String rowKey) throws IOException {
        table = new HTable(conf, TABLE_NAME);
        Get g = new Get(rowKey.getBytes());
        Result res = table.get(g);

        System.out.println("=======" + new String(res.getRow()));

        for (Cell cell : res.rawCells()) {
            System.out.println("--------------------" + new String(cell.getRow()) + "----------------------------");
            System.out.println("Column Family: " + new String(cell.getFamily()));
            System.out.println("Column: " + new String(cell.getQualifier()));
            System.out.println("value: " + new String(cell.getValue()));
        }
    }

    public static void main(String[] args) {
        BasicConfigurator.configure(); //自动快速地使用缺省Log4j环境。
        conf.set("hbase.master", "192.168.224.10:60000");
        conf.set("hbase.zookeeper.quorum", "192.168.224.10, 192.168.224.11, 192.168.224.12");

        try {
            selectRowKey("1001");
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}
