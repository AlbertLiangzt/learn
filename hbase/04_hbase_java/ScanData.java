import org.apache.derby.iapi.types.DataValueDescriptor;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.KeyValue;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.filter.*;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;


public class ScanData {
    public static final String TABLE_NAME = "m_table";
    public static final DataValueDescriptor CellUtil = null;

    public static Configuration conf = HBaseConfiguration.create();
    public static Connection connection = null;
    public static Table table = null;

    /**
     * 扫描所有数据
     *
     * @throws IOException
     */
    public static void getAllRecords() throws IOException {
        connection = ConnectionFactory.createConnection(conf);
        table = connection.getTable(TableName.valueOf(TABLE_NAME));

        Scan scan = new Scan();
        scan.setCaching(100);
        ResultScanner resScan = table.getScanner(scan);

        for (Result res : resScan) {
            System.out.println("----------scan----------all----------data----------");
            for (KeyValue kv : res.raw()) {
                System.out.print(new String(kv.getRow()) + " ");
                System.out.print(new String(kv.getFamily()) + " ");
                System.out.print(new String(kv.getQualifier()) + " ");
                System.out.print(kv.getTimestamp() + " ");
                System.out.println(new String(kv.getValue()));
            }
        }

        resScan.close();
        table.close();
        connection.close();
    }

    /**
     * 使用过滤器，扫描多条数据
     *
     * @param rowKey
     * @throws IOException
     */
    public static void getRecordsWithFilter(String rowKey) throws IOException {
        System.out.println("----------scan----------filter----------start----------");
        table = new HTable(conf, TABLE_NAME);
        Filter filter = new RowFilter(CompareFilter.CompareOp.EQUAL, new BinaryComparator(Bytes.toBytes(rowKey)));

        Scan scan = new Scan();
        scan.setCaching(100);
        scan.setFilter(filter);

        ResultScanner resScan = table.getScanner(scan);

        for (Result res : resScan) {
            System.out.println("----------scan----------filter----------with----------rowKey:" + rowKey + "----------");
            for (KeyValue kv : res.raw()) {
                System.out.print(new String(kv.getRow()) + " ");
                System.out.print(new String(kv.getFamily()) + " ");
                System.out.print(new String(kv.getQualifier()) + " ");
                System.out.print(kv.getTimestamp() + "");
                System.out.println(new String(kv.getValue()));
            }
        }

    }

    /**
     * 使用过滤器，扫描多条数据
     *
     * @param rowKeyList
     * @throws IOException
     */
    public static void getRecordsWithFilter(ArrayList<String> rowKeyList) throws IOException {
        table = new HTable(conf, TABLE_NAME);

        List<Filter> listFilter = new ArrayList<Filter>();
        for (int i = 0; i < rowKeyList.size(); i++) {
            listFilter.add(new RowFilter(CompareFilter.CompareOp.EQUAL, new BinaryComparator(Bytes.toBytes(rowKeyList.get(i)))));
        }
        FilterList filterList = new FilterList(FilterList.Operator.MUST_PASS_ONE, listFilter);

        Scan scan = new Scan();
        scan.setCaching(100);
        scan.setFilter(filterList);

        ResultScanner resScan = table.getScanner(scan);

        for (Result res : resScan) {
            System.out.println("----------scan----------filter----------with----------rowKeyList:" + rowKeyList + "----------");
            for (KeyValue kv : res.raw()) {
                System.out.print(new String(kv.getRow()) + " ");
                System.out.print(new String(kv.getFamily()) + " ");
                System.out.print(new String(kv.getQualifier()) + " ");
                System.out.print(kv.getTimestamp() + "");
                System.out.println(new String(kv.getValue()));
            }
        }

    }


    public static void main(String[] args) {
        conf.set("hbase:master", "192.168.224.10:60000");
        conf.set("hbase.zookeeper.quorum", "192.168.224.10, 192.168.224.11, 192.168.224.12");

        try {
            getAllRecords();
            getRecordsWithFilter("1001");

            ArrayList<String> rowKeyList = new ArrayList<>();
            rowKeyList.add("1002");
            rowKeyList.add("2001");

            getRecordsWithFilter(rowKeyList);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
