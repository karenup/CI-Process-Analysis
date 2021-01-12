package com.paper.CIprocessanalysis;

import org.python.core.PyString;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.python.core.PyFunction;
import org.python.core.PyInteger;
import org.python.core.PyObject;
import org.python.util.PythonInterpreter;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

@SpringBootApplication
public class CiProcessAnalysisApplication {

    public void CSVMerge(String projectName) {
        String exe = "python";
        String command = "src\\main\\java\\com\\paper\\CIprocessanalysis\\mergeActivity.py";
        try {
            String[] cmdArr = new String[] {exe, command, projectName};
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
        String exe = "python";
        String command = "src\\main\\java\\com\\paper\\CIprocessanalysis\\AddStatusRowTime.py";
        try {
            String[] cmdArr = new String[] {exe, command, projectName};
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
        String exe = "python";
        String command = "src\\main\\java\\com\\paper\\CIprocessanalysis\\JobLogToCSV.py";
        String resultCSV = null;

        try {
            String[] cmdArr = new String[] {exe, command, CIPath, OUTPath, JobLogpath};
            Process proc = Runtime.getRuntime().exec(cmdArr);// 执行py文件

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
            resultCSV = "D:/Users/b/PycharmProjects/jobLogExtract/extract/" + projectName + "_extract.csv";  // 输出文件路径
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
        return resultCSV;
    }

	public static void main(String[] args) {
		SpringApplication.run(CiProcessAnalysisApplication.class, args);
		CiProcessAnalysisApplication ciProcessAnalysisApplication = new CiProcessAnalysisApplication();

        String CI = "D:/南京大学/研一/Thesis/日志整理/CI/vagrant_CI.csv";
        String OUT = "D:/南京大学/研一/Thesis/日志整理/COtoCI/vagrant_out.csv";
        String path = "D:/Users/b/PycharmProjects/jobLog/vagrant";
        String resultCSV = ciProcessAnalysisApplication.produceEventLog(CI,OUT,path);
        System.out.println(resultCSV);

    }

}

