package dataProcess;

import com.process.service.processMining.MiningAlgorithm;
import org.junit.Test;
import com.process.service.dataProcess.ProcessData;

import java.util.*;
import java.util.regex.Pattern;


public class TestProcessData {

    @Test
    public void testProduceEventLog(){

        ProcessData processData = new ProcessData();

        String CI = "android_CI";
        String OUT = "android_out";
        String path = "android";
        String resultCSV = processData.produceEventLog(CI,OUT,path);
        System.out.println(resultCSV);
    }

    @Test
    public void testProcessMiningAlg(){
        MiningAlgorithm ma = new MiningAlgorithm();
        String modelPath = ma.processMiningAlg("2","sonarqube");
        System.out.println(modelPath);
    }

}
