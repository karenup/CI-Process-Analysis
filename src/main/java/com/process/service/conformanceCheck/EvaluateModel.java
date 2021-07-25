package com.process.service.conformanceCheck;

import java.util.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import com.process.service.CONSTANT.FilePath;

public class EvaluateModel {

    public String modelEvaluate(String miningAlgNum, String ProName){
        String eventLogFilePath = FilePath.eventLogOutputPath + ProName + "_extract.csv";
        String exe = "/Users/karen/nju-work/graduate-design/code/CI-process-analysis/venv/bin/python";
        String command = "src/main/java/com/process/service/conformanceCheck/evaluateModel.py";
        List<String> list = new ArrayList<String>();
        String listString = null;

        try {
            String[] cmdArr = new String[] {exe, command, miningAlgNum, eventLogFilePath};
            Process proc = Runtime.getRuntime().exec(cmdArr);// 执行py文件

            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            String line = null;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
                listString = line;
            }
            in.close();
            proc.waitFor();
//            listString = listString.substring(1,listString.length()-1);
//            list = Arrays.asList(listString.split(", "));
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

        return listString;

    }

}
