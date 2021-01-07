package dataProcess;

import CONSTANT.FilePath;

import java.io.*;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.stream.Collectors;

/**
 * @author songkaiwen
 * @date 2021/1/6 3:35 下午
 * 该类主要实现从csv中计算出节点和边
 */
public class Caculation {
    /**
     * filename:获取的eventLog.csv
     * nodeMap:存储模型中所有节点的容器类
     * edgeMap：存储模型中所有边的容器类
     * timeMap：用于时间实时计算的容器类
     */
    private String fileName;
    private HashMap<String, List<Integer>> nodeMap;
    private HashMap<String,List<Integer>> edgeMap;
    private HashMap<String,List<Integer>> timeMap;

    public Caculation(String fileName){
        this.fileName = fileName;
    }

    /**
     * 为数组中的活动按照开始时间排序
     * @param oneJob
     */
    public List<List<String>> sortedByStartTime(List<List<String>> oneJob){
        for(List<String> l : oneJob){
            if(!l.get(2).equals("nan")){
                Long sec = convert2Date(l.get(2));
                l.set(2,sec.toString());
            }
        }
        List<List<String>> newOneJob = new ArrayList<>();

        //比较逻辑
        for(List<String> l : oneJob){
            if(l.get(2).equals("nan")){
                newOneJob.add(l);
                continue;
            }
            if(newOneJob.isEmpty()){
                newOneJob.add(l);
                continue;
            }
            int location = 0;
            for(int i = 0;i < newOneJob.size();i++){
                if(newOneJob.get(i).get(2).equals("nan")){
                    location = i+1;
                    continue;
                }
                if(Long.valueOf(l.get(2))>=Long.valueOf(newOneJob.get(i).get(2))){
                    location = i+1;
                }
            }
            //为newOneJob扩一个容
            newOneJob.add(new ArrayList<>());
            //移动位置以完成排序
            for (int i = newOneJob.size()-2;i>=location;i--){
                newOneJob.set(i+1,newOneJob.get(i));
            }
            newOneJob.set(location,l);
        }
        return newOneJob;
    }

    /**
     * 转换日期格式并计算秒数
     * @param d
     * @return
     */
    public Long convert2Date(String d){
        if(d == null){
            return null;
        }
        DateFormat dmt = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
        Date date = null;
        Long second = null;
        try {
            date = dmt.parse(d);
            second = date.getTime()/1000;
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return second;
    }

    public void caculate(){
        File csv = new File(FilePath.csvFilePath+this.fileName+".csv");
        //将csv文件读取为text
        try{
            BufferedReader textFile = new BufferedReader(new FileReader(csv));
            String lineDta = "";
            List<List<String>> oneJob = new ArrayList<>();
            while ((lineDta = textFile.readLine()) != null){
                if (lineDta.split(",")[0].equals("Job ID")){
                    continue;
                }
                List<String> dataList = Arrays.asList(lineDta.split(","));
                if (oneJob.isEmpty()){
                    oneJob.add(dataList);
                }else {
                    if(dataList.get(0).equals(oneJob.get(oneJob.size()-1))){
                        oneJob.add(dataList);
                    }else {

                    }
                }

//                System.out.println(lineDta);

            }
        } catch (FileNotFoundException e){
            System.out.println("没有找到文件");
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}
