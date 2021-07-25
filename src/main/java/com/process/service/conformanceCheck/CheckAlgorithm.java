package com.process.service.conformanceCheck;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import com.process.service.CONSTANT.FilePath;

public class CheckAlgorithm {

    public String conformanceCheck(String miningAlgNum, String conCheckAlgNum, String ProName){
        String eventLogFilePath = FilePath.eventLogOutputPath + ProName + "_extract.csv";
        String outPutPath = "";
        if("1".equals(conCheckAlgNum) &&  "1".equals(miningAlgNum)){
            outPutPath = FilePath.CheckOutPutPath1 + ProName + "_" + "alpha" + ".csv";
        }else if("1".equals(conCheckAlgNum) &&  "2".equals(miningAlgNum)){
            outPutPath = FilePath.CheckOutPutPath1 + ProName + "_" + "heuristic" + ".csv";
        }else if("2".equals(conCheckAlgNum) &&  "1".equals(miningAlgNum)){
            outPutPath = FilePath.CheckOutPutPath2 + ProName + "_" + "alpha" + ".csv";
        }else if("2".equals(conCheckAlgNum) &&  "2".equals(miningAlgNum)){
            outPutPath = FilePath.CheckOutPutPath2 + ProName + "_" + "heuristic" + ".csv";
        }
        String exe = "/Users/karen/nju-work/graduate-design/code/CI-process-analysis/venv/bin/python";

        String command = "/Users/karen/nju-work/graduate-design/code/CI-process-analysis/src/main/java/com/process/service/conformanceCheck/conformanceCheck.py";

        try {
            String[] cmdArr = new String[] {exe, command, miningAlgNum, conCheckAlgNum, eventLogFilePath, outPutPath};
            //String str = "python3 /Users/karen/nju-work/graduate-design/code/CI-process-analysis/src/main/java/com/process/service/conformanceCheck/conformanceCheck.py  1 1 /Users/karen/nju-work/tool-test/extract/android_extract.csv /Users/karen/nju-work/tool-test/conformance/tokenReplay/xxx111.csv";

            Process proc = Runtime.getRuntime().exec(cmdArr);// 执行py文件

            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            String line = null;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
            }
            in.close();
            proc.waitFor();
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

        return outPutPath;

    }

}
