import org.apache.hadoop.hive.ql.exec.UDF;
import org.apache.hadoop.io.Text;

public class HiveUppercase extends UDF {
    public Text evaluate(final Text s) {
        return new Text(s.toString().toUpperCase());
    }
}
