package processMining;


import org.junit.Test;
import com.process.service.processMining.MiningAlgorithm;

import java.util.*;
import java.util.regex.Pattern;


public class TestMiningAlgorithm {

    @Test
    public void testProduceEventLog(){

        MiningAlgorithm miningAlgorithm = new MiningAlgorithm();

        String resultPDF = miningAlgorithm.processMiningAlg("2","cloudify");
        System.out.println(resultPDF);
    }
}
