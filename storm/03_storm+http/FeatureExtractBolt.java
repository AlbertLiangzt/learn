package stormHttp;

import backtype.storm.topology.BasicOutputCollector;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseBasicBolt;
import backtype.storm.tuple.Tuple;
import org.apache.storm.http.HttpEntity;
import org.apache.storm.http.client.methods.CloseableHttpResponse;
import org.apache.storm.http.client.methods.HttpGet;
import org.apache.storm.http.impl.client.CloseableHttpClient;
import org.apache.storm.http.impl.client.HttpClients;
import org.apache.storm.http.util.EntityUtils;

import java.io.IOException;

public class FeatureExtractBolt extends BaseBasicBolt {

    @Override
    public void execute(Tuple tuple, BasicOutputCollector basicOutputCollector) {
        System.out.println("----tuple----" + tuple);
        String content = tuple.toString();

        CloseableHttpClient httpClient = HttpClients.createDefault();

        System.out.println("----content----" + content);
        HttpGet httpGet = new HttpGet("http://192.168.224.10:8808/?content=" + content);

        try {
            CloseableHttpResponse response = httpClient.execute(httpGet);
            HttpEntity entity = response.getEntity();

            System.out.println("----response.getStatusLine----" + response.getStatusLine());
            if (null != entity) {
                System.out.println("----Response content length:----" + entity.getContentLength());

                String responseStr = new String(EntityUtils.toString(entity));
                responseStr = new String(responseStr.getBytes("ISO-8859-1"), "utf-8");
                System.out.println("----responseStr----" + responseStr);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                httpClient.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer outputFieldsDeclarer) {

    }
}
