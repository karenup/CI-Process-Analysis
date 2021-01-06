package dataProcess;

import java.util.HashMap;
import java.util.List;

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

    public void caculate(String fileName){

    }
}
