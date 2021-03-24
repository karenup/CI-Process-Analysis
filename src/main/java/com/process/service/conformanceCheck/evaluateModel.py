import pandas as pd
import sys
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.evaluation.replay_fitness import evaluator as replay_fitness_evaluator
from pm4py.evaluation.precision import evaluator as precision_evaluator
from pm4py.evaluation.generalization import evaluator as generalization_evaluator
from pm4py.evaluation.simplicity import evaluator as simplicity_evaluator

# 接口内部逻辑描述：
# 首先执行"导入csv日志文件并转换为事件日志对象"操作
# 然后判断使用的过程挖掘算法，如果是"alpha"，执行"应用alpha算法"操作，然后执行"计算并打印契合度、精确度、泛化程度、简单度"，最后执行"结果写入表格并保存为csv文件"操作，返回文件的存储路径
# 如果是"heuristic"，执行"应用heuristic算法"操作，然后执行"计算并打印契合度、精确度、泛化程度、简单度"，最后执行"结果写入表格并保存为csv文件"操作，返回文件的存储路径
# 注意保存文件时候的命名规则：如android_alpha.csv


def alpha(event_log):
    # 应用alpha算法
    parameters = {alpha_miner.Parameters.CASE_ID_KEY: "case:Job ID", alpha_miner.Parameters.ACTIVITY_KEY: "Activity"
        , alpha_miner.Parameters.START_TIMESTAMP_KEY: "Start Timestamp"}
    net, initial_marking, final_marking = alpha_miner.apply(event_log, parameters)

    # 计算并打印契合度、精确度、泛化程度、简单度
    parameters3 = {replay_fitness_evaluator.Variants.TOKEN_BASED.value.Parameters.ACTIVITY_KEY: "Activity"}
    fitness = replay_fitness_evaluator.apply(event_log, net, initial_marking, final_marking, parameters3)
    print("契合度：", fitness)

    parameters4 = {precision_evaluator.Variants.ETCONFORMANCE_TOKEN.value.Parameters.ACTIVITY_KEY: "Activity"}
    prec = precision_evaluator.apply(event_log, net, initial_marking, final_marking, parameters4)
    print("精确度：", prec)

    parameters5 = {generalization_evaluator.Variants.GENERALIZATION_TOKEN.value.Parameters.ACTIVITY_KEY: "Activity"}
    gen = generalization_evaluator.apply(event_log, net, initial_marking, final_marking, parameters5)
    print("泛化程度：", gen)

    simp = simplicity_evaluator.apply(net)
    print("模型简单度：", simp)

    # 把四个值放在list里返回
    list = [fitness.get('averageFitness'), prec, gen, simp]
    print(list)

def Heuristic(event_log):
    # 应用Heuristic算法
    parameters = {heuristics_miner.Variants.CLASSIC.value.Parameters.CASE_ID_KEY: "case:Job ID",
                  heuristics_miner.Variants.CLASSIC.value.Parameters.ACTIVITY_KEY: "Activity"
        , heuristics_miner.Variants.CLASSIC.value.Parameters.START_TIMESTAMP_KEY: "Start Timestamp"
        , heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.99}
    net, initial_marking, final_marking = heuristics_miner.apply(event_log, parameters)

    # 计算并打印契合度、精确度、泛化程度、简单度
    parameters3 = {replay_fitness_evaluator.Variants.TOKEN_BASED.value.Parameters.ACTIVITY_KEY: "Activity"}
    fitness = replay_fitness_evaluator.apply(event_log, net, initial_marking, final_marking, parameters3)
    print("契合度：", fitness)

    parameters4 = {precision_evaluator.Variants.ETCONFORMANCE_TOKEN.value.Parameters.ACTIVITY_KEY: "Activity"}
    prec = precision_evaluator.apply(event_log, net, initial_marking, final_marking, parameters4)
    print("精确度：", prec)

    parameters5 = {generalization_evaluator.Variants.GENERALIZATION_TOKEN.value.Parameters.ACTIVITY_KEY: "Activity"}
    gen = generalization_evaluator.apply(event_log, net, initial_marking, final_marking, parameters5)
    print("泛化程度：", gen)

    simp = simplicity_evaluator.apply(net)
    print("模型简单度：", simp)

    # 把四个值放在list里返回
    list = [fitness.get('averageFitness'), prec, gen, simp]
    print(list)



# 结果写入表格并保存为csv文件
# name_evaluate = {'契合度':[fitness.get('averageFitness')], '精确度':[prec], '泛化程度':[gen], '简单度':[simp]}
# data = pd.DataFrame(name_evaluate)
# print(data)
# data.to_csv('/Users/karen/nju-work/tool-test/evaluate/android_heuristic.csv', encoding='gbk')

def evaluateProcess(AlgNumber, eventLogFilePath):
    # 导入csv日志文件并转换为事件日志对象
    log_csv = pd.read_csv(eventLogFilePath, sep=',')
    log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
    log_csv = log_csv.sort_values('Start Timestamp')
    # parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'Job ID'}
    log_csv.rename(columns={'Job ID': 'case:Job ID'}, inplace=True)
    parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'case:Job ID'}
    event_log = log_converter.apply(log_csv, parameters=parameters, variant=log_converter.Variants.TO_EVENT_LOG)
    print(event_log)

    if AlgNumber=='1' :
        alpha(event_log)
    elif AlgNumber=='2' :
        Heuristic(event_log)


if __name__ == '__main__':
    # evaluateProcess('2', 'D:/Users/b/PycharmProjects/jobLogExtract/extract/' + 'android' + '_extract.csv')

    a = []
    for i in range(1, len(sys.argv)):
        a.append((sys.argv[i]))

    evaluateProcess(a[0], a[1])


