package conformanceCheck;

import org.junit.Test;
import com.process.service.conformanceCheck.CheckAlgorithm;
import com.process.service.conformanceCheck.EvaluateModel;

import java.util.*;
import java.util.regex.Pattern;

public class TestCheckAlgorithm {

    @Test
    public void testConformanceCheck(){

        CheckAlgorithm checkAlgorithm = new CheckAlgorithm();

        String resultCSV = checkAlgorithm.conformanceCheck("1","1","android");
        System.out.println(resultCSV);
    }

    @Test
    public void testEvaluateModel(){

        EvaluateModel evaluateModel = new EvaluateModel();
        List<String> list = evaluateModel.modelEvaluate("1","android");
        System.out.println(list);

    }

}
