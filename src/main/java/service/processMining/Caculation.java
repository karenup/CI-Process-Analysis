package service.processMining;

import service.CONSTANT.FilePath;
import service.fileformat.UnicodeReader;

import java.io.*;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.regex.Pattern;
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
    private HashMap<String, List<Long>> nodeMap = new HashMap<>();
    private HashMap<String,List<Long>> edgeMap = new HashMap<>();
    private HashMap<String,List<Long>> timeMap = new HashMap<>();

    public String getFileName() {
        return fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

    public HashMap<String, List<Long>> getNodeMap() {
        return nodeMap;
    }

    public void setNodeMap(HashMap<String, List<Long>> nodeMap) {
        this.nodeMap = nodeMap;
    }

    public HashMap<String, List<Long>> getEdgeMap() {
        return edgeMap;
    }

    public void setEdgeMap(HashMap<String, List<Long>> edgeMap) {
        this.edgeMap = edgeMap;
    }

    public HashMap<String, List<Long>> getTimeMap() {
        return timeMap;
    }

    public void setTimeMap(HashMap<String, List<Long>> timeMap) {
        this.timeMap = timeMap;
    }



    public Caculation(String fileName){
        this.fileName = fileName;
    }

    /**
     * 把List中的缺失删除并按照开始时间进行排序
     * @param primaryList
     */
    public List<List<String>> sortedByStartTime(List<List<String>> primaryList){
        Iterator<List<String>> itOfList = primaryList.iterator();
        Integer flag = 1;
        while(itOfList.hasNext()){
            List<String> l = itOfList.next();
            if("nan".equals(l.get(2))){
                flag = 0;
                break;
            }
            Long startTime = convert2Date(l.get(2));
            l.set(2,startTime.toString());
            if(!"nan".equals(l.get(3))){
                Long endTime = convert2Date(l.get(3));
                l.set(3,endTime.toString());
            }
        }

        List<List<String>> newOneJob = new ArrayList<>();
        if(flag.equals(1)){
            newOneJob = primaryList.stream()
                    .sorted(Comparator.comparingLong(t -> Long.parseLong(t.get(2))))
                    .collect(Collectors.toList());
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
        DateFormat dmt = new SimpleDateFormat("yyyy/MM/dd HH:mm");
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

    /**
     * 更新nodeMap和edgeMap
     */
    public void updateNodeMap(){
        List<Long> nodeValue = Arrays.asList(0L,0L,0L,0L);

        /**
         * 计算时间参数
         */
        for(Map.Entry<String,List<Long>> entry:timeMap.entrySet()){
            List<Long> timeValue = entry.getValue();
            Long totalTime = timeValue.stream().reduce(Long::sum).orElse(0L);
            if(timeValue.size() <= 1){
                System.out.println(entry.getKey()+timeValue);
            }
            Long medianTime = timeValue.get(timeValue.size()/2);
            if(timeValue.size()%2 == 0){
                medianTime = (timeValue.get(timeValue.size()/2)+timeValue.get(timeValue.size()/2))/2;
            }
            Long averageTime = totalTime/timeValue.size();
            Long totalCount = (long)timeValue.size();

            nodeValue.set(0,totalTime);
            nodeValue.set(1,averageTime);
            nodeValue.set(2,medianTime);
            nodeValue.set(3,totalCount);

            //判断是点还是边
            String nodeName = entry.getKey();
            String pattern1 = ".*[a-z]2[a-z].*";
            String pattern2 = ".*[a-z].[0-9]2[a-z].*";
            if(Pattern.matches(pattern1,nodeName) || Pattern.matches(pattern2,nodeName)){
                edgeMap.put(nodeName,new ArrayList<>(nodeValue));
            }else {
                nodeMap.put(nodeName,new ArrayList<>(nodeValue));
            }
        }

    }

    /**
     * 更新timeMap
     * @param newJob
     */
    public void updateTimeMap(List<List<String>> newJob){
        String nodeName = null;
        String edgeName = null;


        for(int i = 0; i<newJob.size();i++){
            nodeName = newJob.get(i).get(1);
            if(i>0){
                edgeName = newJob.get(i-1).get(1)+"2"+newJob.get(i).get(1);
            }

            Long startTime = Long.parseLong(newJob.get(i).get(2));

            //计算活动的持续时间
            Long timeDiff = 0L;
            if(!"nan".equals(newJob.get(i).get(3))){
                Long endTime = Long.parseLong(newJob.get(i).get(3));
                timeDiff = endTime - startTime;
            }

            //计算活动之间的间隔时间
            Long timeInterval = 0L;
            if(i>0){
                if(!"nan".equals(newJob.get(i-1).get(3))){
                    Long lastEndTime = Long.parseLong(newJob.get(i-1).get(3));
                    timeInterval = startTime - lastEndTime;
                }
            }

            //更新timeMap
            if(timeMap.containsKey(nodeName)){
                timeMap.get(nodeName).add(timeDiff);

            }else {
                List<Long> timeValueList = new ArrayList<>();
                timeValueList.add(timeDiff);
                timeMap.put(nodeName,timeValueList);
            }
            if(edgeName != null){
                if(timeMap.containsKey(edgeName)){
                    timeMap.get(edgeName).add(timeInterval);

                }else{
                    List<Long> timeInterList = new ArrayList<>();
                    timeInterList.add(timeInterval);
                    timeMap.put(edgeName,timeInterList);
                }
            }
        }
    }

    /**
     * 计算点、边参数
     */
    public void calculate(){
        File csv = new File(FilePath.csvFilePath+this.fileName+".csv");


        //将csv文件读取为text
        try{
            FileInputStream fis = new FileInputStream(csv);
            UnicodeReader ur = new UnicodeReader(fis, "utf-8");
            BufferedReader textFile = new BufferedReader(ur);
            String lineDta = "";
            List<List<String>> oneJob = new ArrayList<>();
            while ((lineDta = textFile.readLine()) != null){
                if ("Job ID".equals(lineDta.split(",")[0])){
                    continue;
                }
                List<String> dataList = Arrays.asList(lineDta.split(","));
                if (oneJob.isEmpty()){
                    oneJob.add(dataList);
                }else {
                    if (!dataList.get(0).equals(oneJob.get(oneJob.size() - 1).get(0))) {
                        List<List<String>> newJob = sortedByStartTime(oneJob);
                        if (!newJob.isEmpty()) {
                            //更新timeMap
                            updateTimeMap(newJob);
                        }
                        oneJob.clear();
                    }
                    oneJob.add(dataList);
                }

//                System.out.println(lineDta);
            }
            //更新nodeMap和edgeMap
            updateNodeMap();
        } catch (FileNotFoundException e){
            System.out.println("没有找到文件");
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}
