package com.process.service.dataProcess;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import com.process.service.CONSTANT.FilePath;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

public class ProcessData {

    public void CSVMerge(String projectName) {
        String exe = "/Users/karen/nju-work/graduate-design/code/CI-process-analysis/venv/bin/python";
        String command = "/Users/karen/nju-work/graduate-design/code/CI-process-analysis/src/main/java/com/process/service/dataProcess/mergeActivity.py";
        try {
            String[] cmdArr = new String[] {exe, command, projectName, FilePath.eventLogOutputPath};
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
    }

    public void addStatusRowTime(String projectName) {
        String exe = "/Users/karen/nju-work/graduate-design/code/CI-process-analysis/venv/bin/python";
        String command = "/Users/karen/nju-work/graduate-design/code/CI-process-analysis/src/main/java/com/process/service/dataProcess/AddStatusRowTime.py";
        try {
            String[] cmdArr = new String[] {exe, command, projectName, FilePath.eventLogOutputPath};
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
    }

    public String produceEventLog(String CIPath, String OUTPath, String JobLogpath){
        CIPath = FilePath.CIFilePath + CIPath + ".csv";
        OUTPath = FilePath.OutFilePath + OUTPath + ".csv";
        JobLogpath = FilePath.jobLogfilePath + JobLogpath;
        String exe = "/Users/karen/nju-work/graduate-design/code/CI-process-analysis/venv/bin/python";
        String command = "/Users/karen/nju-work/graduate-design/code/CI-process-analysis/src/main/java/com/process/service/dataProcess/JobLogToCSV.py";
        String resultCSV = null;

        try {
            String[] cmdArr = new String[] {exe, command, CIPath, OUTPath, JobLogpath, FilePath.eventLogOutputPath};
            Process proc = Runtime.getRuntime().exec(cmdArr);

            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            String line = null;
            String projectName = null;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
                projectName = line;
            }
            in.close();
            proc.waitFor();
            CSVMerge(projectName);
            addStatusRowTime(projectName);
//            resultCSV = "D:/Users/b/PycharmProjects/jobLogExtract/extract/" + projectName + "_extract.csv";  // 输出文件路径
            resultCSV = FilePath.eventLogOutputPath + projectName + "_extract.csv";
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
        return resultCSV;
    }


}
