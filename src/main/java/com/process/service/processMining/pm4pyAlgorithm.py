import os
import pandas as pd
import sys
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.visualization.petrinet import visualizer as pn_visualizer
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.visualization.dfg import visualizer as dfg_visualization


# 使用heuristic算法,directly-follows gragh算法,应用alpha算法
def alpha(event_log, outPutPDFPath):
    parameters = {alpha_miner.Parameters.CASE_ID_KEY:"case:Job ID",alpha_miner.Parameters.ACTIVITY_KEY:"Activity"
                  ,alpha_miner.Parameters.START_TIMESTAMP_KEY:"Start Timestamp"}
    net, initial_marking, final_marking = alpha_miner.apply(event_log,parameters)

    #  模型的可视化
    # gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters={pn_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT:"pdf"})
    # pn_visualizer.view(gviz)
    pn_visualizer.save(gviz,outPutPDFPath)

def Heuristic(event_log, outPutPDFPath):
    parameters = {heuristics_miner.Variants.CLASSIC.value.Parameters.CASE_ID_KEY:"case:Job ID",
                  heuristics_miner.Variants.CLASSIC.value.Parameters.ACTIVITY_KEY:"Activity"
                  ,heuristics_miner.Variants.CLASSIC.value.Parameters.START_TIMESTAMP_KEY:"Start Timestamp"
                  ,heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH:0.99}
    heu_net = heuristics_miner.apply_heu(event_log, parameters)

    # gviz = hn_visualizer.apply(heu_net)
    gviz = hn_visualizer.apply(heu_net, parameters={hn_visualizer.Variants.PYDOTPLUS.value.Parameters.FORMAT:"pdf"})
    # hn_visualizer.view(gviz)
    hn_visualizer.save(gviz,outPutPDFPath)

def dfg(event_log, outPutPDFPath):
    parameters = {dfg_visualization.Variants.PERFORMANCE.value.Parameters.START_TIMESTAMP_KEY:"Start Timestamp"
                  ,dfg_visualization.Variants.PERFORMANCE.value.Parameters.ACTIVITY_KEY:"Activity"
                  }
    dfg = dfg_discovery.apply(event_log, parameters)

    parameters = {dfg_visualization.Variants.PERFORMANCE.value.Parameters.FORMAT: "svg"
                  ,dfg_visualization.Variants.PERFORMANCE.value.Parameters.ACTIVITY_KEY:"Activity"
                  ,dfg_visualization.Variants.PERFORMANCE.value.Parameters.START_TIMESTAMP_KEY:"Start Timestamp"}
    gviz = dfg_visualization.apply(dfg, variant=dfg_visualization.Variants.FREQUENCY, parameters={dfg_visualization.Variants.PERFORMANCE.value.Parameters.FORMAT:"pdf"})
    # gviz = dfg_visualization.apply(dfg, variant=dfg_visualization.Variants.FREQUENCY)
    # dfg_visualization.view(gviz)
    dfg_visualization.save(gviz, outPutPDFPath)

def miningProcess(AlgNumber, eventLogFilePath, outPutPDFPath):
    # 导入csv日志文件并转换为事件日志对象
    log_csv = pd.read_csv(eventLogFilePath, sep=',')
    log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
    log_csv = log_csv.sort_values('Start Timestamp')
    # parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'Job ID'}

    log_csv.rename(columns={'Job ID': 'case:Job ID'}, inplace=True)
    parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'case:Job ID'}
    event_log = log_converter.apply(log_csv, parameters=parameters, variant=log_converter.Variants.TO_EVENT_LOG)
    # print(event_log)
    if AlgNumber=='1' :
        alpha(event_log, outPutPDFPath)
    elif AlgNumber=='2' :
        Heuristic(event_log, outPutPDFPath)
    elif AlgNumber=='3' :
        dfg(event_log, outPutPDFPath)

if __name__ == '__main__':
    # miningProcess('3', 'D:/Users/b/PycharmProjects/jobLogExtract/extract/' + 'android' + '_extract.csv',
    #               'D:/Users/b/PycharmProjects/jobLogExtract/pdf/' + 'android' + "_" + '3' + ".pdf")
    a = []
    for i in range(1, len(sys.argv)):
        a.append((sys.argv[i]))

    miningProcess(a[0], a[1], a[2])

