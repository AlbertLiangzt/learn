import org.apache.hadoop.hive.ql.exec.UDFArgumentException;
import org.apache.hadoop.hive.ql.exec.UDFArgumentLengthException;
import org.apache.hadoop.hive.ql.metadata.HiveException;
import org.apache.hadoop.hive.ql.udf.generic.GenericUDTF;
import org.apache.hadoop.hive.serde2.objectinspector.ObjectInspector;
import org.apache.hadoop.hive.serde2.objectinspector.ObjectInspectorFactory;
import org.apache.hadoop.hive.serde2.objectinspector.StructObjectInspector;
import org.apache.hadoop.hive.serde2.objectinspector.primitive.PrimitiveObjectInspectorFactory;

import java.util.ArrayList;

public class HiveExplode extends GenericUDTF {

    // IllegalStateException Should not be called directly
    @Override
    public StructObjectInspector initialize(ObjectInspector[] args) throws UDFArgumentException {
        if (args.length !=1) {
            throw new UDFArgumentLengthException("ExplodeMap takes only one argument");
        }
        if(args[0].getCategory() != ObjectInspector.Category.PRIMITIVE) {
            throw new UDFArgumentException("ExplodeMap takes string as a parameter");
        }

        ArrayList<String> fieldName = new ArrayList<String>();
        ArrayList<ObjectInspector> fieldOI = new ArrayList<ObjectInspector>();

        fieldName.add("id");
        fieldOI.add(PrimitiveObjectInspectorFactory.javaStringObjectInspector);
        fieldName.add("score");
        fieldOI.add(PrimitiveObjectInspectorFactory.javaStringObjectInspector);

        return ObjectInspectorFactory.getStandardStructObjectInspector(fieldName,fieldOI);

    }

    @Override
    public void process(Object[] args) throws HiveException {
        String input = args[0].toString();
        String[] test = input.split(";");

        for (int i = 0; i < test.length; i++) {
            try {
                String[] res = test[i].split(":");
                forward(res);
            } catch (Exception e) {
                continue;
            }
        }
    }

    @Override
    public void close() throws HiveException {

    }
}
