package dataProcess;

import CONSTANT.FilePath;
import org.camunda.feel.syntaxtree.In;

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
    private HashMap<String, List<Long>> nodeMap;
    private HashMap<String,List<Long>> edgeMap;

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

    private HashMap<String,List<Long>> timeMap;

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

    /**
     * 更新nodeMap, edgemap, timeMap
     * @param newJob
     */
    public void updateNodeMap(List<List<String>> newJob){
        String nodeName = null;
        String edgeName = null;
        List<Long> nodeValue = new ArrayList<>();
        List<Long> edgeValue = new ArrayList<>();

        for(int i = 0; i<newJob.size();i++){
            nodeName = newJob.get(i).get(1);
            if(i>0){
                edgeName = newJob.get(i-1).get(1)+newJob.get(i).get(1);
            }

            Long startTime = Long.parseLong(newJob.get(i).get(2));

            //计算活动的开始结束时间
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

            //更新nodeMap
            if(nodeMap.containsKey(nodeName)){
                Long totalTime = timeMap.get(nodeName).stream().reduce(Long::sum).orElse(0L);
                List<Long> sortedList = timeMap.get(nodeName).stream().sorted().collect(Collectors.toList());
                Long medianTime = sortedList.get(sortedList.size()/2);
                Long averageTime = totalTime/sortedList.size();
                Long absoluteCount = (long)sortedList.size();
                Long caseCount = nodeMap.get(nodeName).get(4);
                if(i == 0){
                    caseCount = caseCount + 1;
                }
                nodeValue.set(0,totalTime);
                nodeValue.set(1,medianTime);
                nodeValue.set(2,averageTime);
                nodeValue.set(3,absoluteCount);
                nodeValue.set(4,caseCount);
                nodeMap.put(nodeName,nodeValue);
            }else{
                nodeValue.set(0,timeMap.get(nodeName).get(0));
                nodeValue.set(1,timeMap.get(nodeName).get(1));
                nodeValue.set(2,timeMap.get(nodeName).get(2));
                nodeValue.set(3,1L);
                nodeValue.set(4,1L);
            }

            //更新edgeMap

        }
    }

    public void caculate(){
        File csv = new File(FilePath.csvFilePath+this.fileName+".csv");
        //将csv文件读取为text
        try{
            BufferedReader textFile = new BufferedReader(new FileReader(csv));
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
                    if (!dataList.get(0).equals(oneJob.get(oneJob.size() - 1))) {
                        List<List<String>> newJob = sortedByStartTime(oneJob);
                        if (!newJob.isEmpty()) {
                            //更新nodeMap,edgeMap和timeMap

                        }
                        oneJob.clear();
                    }
                    oneJob.add(dataList);
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
