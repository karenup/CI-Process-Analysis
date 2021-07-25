import pandas as pd
import sys
from pm4py import conformance_tbr
from pm4py.algo.conformance import tokenreplay, alignments
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner


# 接口内部逻辑描述：
# 首先执行"导入csv日志文件并转换为事件日志对象"操作，
# 然后判断传入的过程挖掘算法，如果是alpha算法，则执行"应用alpha"算法操作，如果是heuristic算法，则执行"应用heuristic算法"操作。
# 然后判断传入的一致性检验算法，如果是"token-replay算法"，则执行"应用token-replay方法"操作，然后执行"打印token-replay结果"、"输出token-replay结果到csv文件"操作，最后返回对应的csv文件路径。
# 如果是"alignment算法"，则执行"应用alignment算法"操作，然后执行"打印alignment结果"、"将alignment结果写入csv文件"操作，最后返回结果文件路径。
# （文件结果路径的命名要注意，按照不同的一致性检验算法（token-replay和alignment）分两个文件夹存储，在结果文件名上要有过程挖掘算法的后缀，比如"android_alpha.csv"）


def alphaMiningAlg(event_log):
    # 应用alpha算法
    parameters = {alpha_miner.Parameters.CASE_ID_KEY: "case:Job ID", alpha_miner.Parameters.ACTIVITY_KEY: "Activity"
        , alpha_miner.Parameters.START_TIMESTAMP_KEY: "Start Timestamp"}
    net, initial_marking, final_marking = alpha_miner.apply(event_log, parameters)
    return net, initial_marking, final_marking

def HeuristicMiningAlg(event_log):
    # 应用Heuristic算法
    parameters = {heuristics_miner.Variants.CLASSIC.value.Parameters.CASE_ID_KEY: "case:Job ID",
                  heuristics_miner.Variants.CLASSIC.value.Parameters.ACTIVITY_KEY: "Activity"
        , heuristics_miner.Variants.CLASSIC.value.Parameters.START_TIMESTAMP_KEY: "Start Timestamp"
        , heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.99}
    net, initial_marking, final_marking = heuristics_miner.apply(event_log, parameters)
    return net, initial_marking, final_marking

def tokenReplayCheckAlg(event_log, net, initial_marking, final_marking, outPutPDFPath):
    # 应用token-replay方法
    parameters1 = {tokenreplay.variants.token_replay.Parameters.CASE_ID_KEY: "case:Job ID",
                   tokenreplay.variants.token_replay.Parameters
                       .ACTIVITY_KEY: "Activity"}
    replayed_traces = tokenreplay.algorithm.token_replay.apply(event_log, net, initial_marking, final_marking,
                                                               parameters1)
    # 打印token-replay结果
    print(replayed_traces)

    # 输出token-replay结果到csv文件
    name = ['trace_is_fit', 'trace_fitness', 'activated_transitions', 'reached_marking',
            'enabled_transitions_in_marking', 'transitions_with_problems', 'missing_tokens', 'consumed_tokens',
            'remaining_tokens', 'produced_tokens']

    test = pd.DataFrame(columns=name, data=replayed_traces)
    print(test)
    test.to_csv(outPutPDFPath, encoding='gbk')

def alignmentsCheckAlg(event_log, net, initial_marking, final_marking, outPutPDFPath):
    # 应用alignments方法
    parameters2 = {alignments.algorithm.Parameters.CASE_ID_KEY: "case:Job ID",
                   alignments.algorithm.Parameters.ACTIVITY_KEY: "Activity"}
    aligned_traces = alignments.algorithm.apply_log(event_log, net, initial_marking, final_marking, parameters2)

    # 打印alignments结果
    print(aligned_traces)

    # 输出alignments结果到csv文件
    name_alignments = ['alignment', 'cost', 'queued_states', 'visited_states',
                       'closed_set_length', 'num_visited_markings', 'exact_heu_calculations', 'fitness']
    test_alignments = pd.DataFrame(columns=name_alignments, data=aligned_traces)
    print(test_alignments)
    test_alignments.to_csv(outPutPDFPath,encoding='gbk')


def conformanceCheckPython(miningAlgNum, conCheckAlgNum, eventLogFilePath, outPutPDFPath):
    # 导入csv日志文件并转换为事件日志对象
    log_csv = pd.read_csv(eventLogFilePath, sep=',')
    log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
    log_csv = log_csv.sort_values('Start Timestamp')
    # parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'Job ID'}
    log_csv.rename(columns={'Job ID': 'case:Job ID'}, inplace=True)
    parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'case:Job ID'}
    event_log = log_converter.apply(log_csv, parameters=parameters, variant=log_converter.Variants.TO_EVENT_LOG)
    print(event_log)
    if miningAlgNum=='1' and conCheckAlgNum=='1' :
        net, initial_marking, final_marking = alphaMiningAlg(event_log)
        tokenReplayCheckAlg(event_log, net, initial_marking, final_marking, outPutPDFPath)
    elif miningAlgNum=='1' and conCheckAlgNum=='2' :
        net, initial_marking, final_marking = alphaMiningAlg(event_log)
        alignmentsCheckAlg(event_log, net, initial_marking, final_marking, outPutPDFPath)
    elif miningAlgNum == '2' and conCheckAlgNum == '1':
        net, initial_marking, final_marking = HeuristicMiningAlg(event_log)
        tokenReplayCheckAlg(event_log, net, initial_marking, final_marking, outPutPDFPath)
    elif miningAlgNum == '2' and conCheckAlgNum == '2':
        net, initial_marking, final_marking = HeuristicMiningAlg(event_log)
        alignmentsCheckAlg(event_log, net, initial_marking, final_marking, outPutPDFPath)

if __name__ == '__main__':
    # conformanceCheckPython('1','2', 'D:/Users/b/PycharmProjects/jobLogExtract/extract/' + 'android' + '_extract.csv',
    #               'D:/Users/b/PycharmProjects/jobLogExtract/conformance/' + 'alignment/' + 'android' + "_" + '1' + ".csv")

    a = []
    for i in range(1, len(sys.argv)):
        a.append((sys.argv[i]))

    conformanceCheckPython(a[0], a[1], a[2], a[3])