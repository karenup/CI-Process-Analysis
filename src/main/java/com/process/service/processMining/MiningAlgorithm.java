package com.process.service.processMining;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import com.process.service.CONSTANT.FilePath;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

public class MiningAlgorithm {

    public String processMiningAlg(String AlgNumber, String ProName){
        String eventLogFilePath = FilePath.eventLogOutputPath + ProName + "_extract.csv";
        String outPutPDFPath = FilePath.PDFOutPutPath + ProName + "_" + AlgNumber + ".pdf";
        String exe = "/Users/karen/nju-work/graduate-design/code/CI-process-analysis/venv/bin/python";
        String command = "/Users/karen/nju-work/graduate-design/code/CI-process-analysis/src/main/java/com/process/service/processMining/pm4pyAlgorithm.py";
        String resultCSV = null;

        try {
            String[] cmdArr = new String[] {exe, command, AlgNumber, eventLogFilePath, outPutPDFPath};
            Process proc = Runtime.getRuntime().exec(cmdArr);// 执行py文件

            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            String line = null;
            while ((line = in.readLine()) != null) {
//                System.out.println(line);
            }
            in.close();
            proc.waitFor();
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

        return outPutPDFPath;

    }
}
