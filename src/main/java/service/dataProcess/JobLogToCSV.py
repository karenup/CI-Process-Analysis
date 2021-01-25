# -*- coding: utf-8 -*-
# coding: utf-8
import pandas as pd
import numpy as np
import time
import csv
import math
import re
from datetime import datetime
import os
import sys

# def getabnormalBuildPushPrAfterBuild(targetOUT, CIinUse):
#     abnormalBuild = set()
#     target_out = targetOUT[['commit_id', 'commit_timestamp', 'tr_build_id', 'gh_build_started_at', 'build_way']]
#     for index, row in target_out[:].iterrows():
#         commitTime = str(row['commit_timestamp'])
#         buildId = row['tr_build_id']
#         buildTime = str(row['gh_build_started_at'])
#         if math.isnan(buildId): # commit在CI文件中没有对应，跳过
#             continue
#         buildId = str(int(buildId))
#         if not inTimeScope(buildTime): # 排除gh_build_started_at在2014-8-7之前的build记录
#             continue
#         isPr = CIinUse[buildId][1]
#         prTime = CIinUse[buildId][2]
#         pushTime = CIinUse[buildId][3]
#         commit_time = time.mktime(time.strptime(commitTime, '%Y-%m-%d %H:%M:%S'))
#         build_time = time.mktime(time.strptime(buildTime, '%Y-%m-%d %H:%M:%S'))
#         if isPr == 0:
#             if pushTime is not np.nan:
#                 pushTime = transferTimeCI(pushTime)
#                 push_time = time.mktime(time.strptime(pushTime, '%Y/%m/%d %H:%M:%S'))
#                 if commit_time > push_time:
#                     abnormalBuild.add(buildId)
#                 elif build_time < push_time:
#                     abnormalBuild.add(buildId)
#         else:
#             if pushTime is np.nan:
#                 prTime = transferTimeCI(prTime)
#                 pr_time = time.mktime(time.strptime(prTime, '%Y/%m/%d %H:%M:%S'))
#                 if commit_time > pr_time:
#                     abnormalBuild.add(buildId)
#                 elif build_time < pr_time:
#                     abnormalBuild.add(buildId)
#             else:
#                 pushTime = transferTimeCI(pushTime)
#                 push_time = time.mktime(time.strptime(pushTime, '%Y/%m/%d %H:%M:%S'))
#                 prTime = transferTimeCI(prTime)
#                 pr_time = time.mktime(time.strptime(prTime, '%Y/%m/%d %H:%M:%S'))
#                 if push_time > pr_time:
#                     if commit_time > push_time:
#                         abnormalBuild.add(buildId)
#                     elif build_time < push_time:
#                         abnormalBuild.add(buildId)
#                 else:
#                     if commit_time > pr_time:
#                         abnormalBuild.add(buildId)
#                     elif build_time < pr_time:
#                         abnormalBuild.add(buildId)
#     return abnormalBuild

def getabnormalBuild(targetOUT, CIinUse):
    abnormalBuild = set()
    target_out = targetOUT[['commit_id', 'commit_timestamp', 'tr_build_id', 'gh_build_started_at', 'build_way']]
    for index, row in target_out[:].iterrows():
        commitTime = str(row['commit_timestamp'])
        buildId = row['tr_build_id']
        buildTime = str(row['gh_build_started_at'])
        if math.isnan(buildId): # commit在CI文件中没有对应，跳过
            continue
        buildId = str(int(buildId))
        if not inTimeScope(buildTime): # 排除gh_build_started_at在2014-8-7之前的build记录
            continue
        isPr = CIinUse[buildId][1]
        prTime = CIinUse[buildId][2]
        pushTime = CIinUse[buildId][3]
        commit_time = time.mktime(time.strptime(commitTime, '%Y-%m-%d %H:%M:%S'))
        if isPr == 0:
            if pushTime is not np.nan:
                pushTime = transferTimeCI(pushTime)
                push_time = time.mktime(time.strptime(pushTime, '%Y/%m/%d %H:%M:%S'))
                if commit_time > push_time:
                    abnormalBuild.add(buildId)
        else:
            if pushTime is np.nan:
                prTime = transferTimeCI(prTime)
                pr_time = time.mktime(time.strptime(prTime, '%Y/%m/%d %H:%M:%S'))
                if commit_time > pr_time:
                    abnormalBuild.add(buildId)
            else:
                pushTime = transferTimeCI(pushTime)
                push_time = time.mktime(time.strptime(pushTime, '%Y/%m/%d %H:%M:%S'))
                prTime = transferTimeCI(prTime)
                pr_time = time.mktime(time.strptime(prTime, '%Y/%m/%d %H:%M:%S'))
                if push_time > pr_time:
                    if commit_time > push_time:
                        abnormalBuild.add(buildId)
                else:
                    if commit_time > pr_time:
                        abnormalBuild.add(buildId)
    return abnormalBuild

def transferTimeLog(time):
    list_i = list(time)  # str -> list
    list_i.insert(-9, '.')  # 注意不用重新赋值
    time = ''.join(list_i)  # list -> str
    time = time[:-3]
    time = datetime.utcfromtimestamp(float(time))
    timeStr = time.strftime('%Y/%m/%d %H:%M:%S')
    return timeStr

def transferTimeCI(time):
    pushPrTime = time[1:]
    cday = datetime.strptime(pushPrTime, '%Y-%m-%d %H:%M:%S')
    timeStr = cday.strftime('%Y/%m/%d %H:%M:%S')
    return  timeStr

def inTimeScope(buildTime):
    flag = False
    b_time = time.mktime(time.strptime(buildTime, '%Y-%m-%d %H:%M:%S'))
    s_time = time.mktime(time.strptime('2014-8-7 0:0:0', '%Y-%m-%d %H:%M:%S'))
    if b_time > s_time:
        flag = True
    return flag

def jobLogExists(buildId,CIinUse,path):
    jobId = CIinUse[buildId][0]
    path = path + '/' + jobId + '.txt' # 'D:/Users/b/PycharmProjects/jobLog/' + projectName + '/' + jobId + '.txt'
    isExists = os.path.exists(path)
    return isExists

def getCIDict(targetCI):
    target_start = targetCI[['tr_build_id', 'tr_job_id', 'gh_is_pr', 'gh_pr_created_at', 'gh_pushed_at','tr_status', 'git_trigger_commit', 'gh_build_started_at']]
    interval = {}
    for index, row in target_start.iterrows():
        buildId = str(row['tr_build_id'])
        jobId = str(row['tr_job_id'])
        isPr = row['gh_is_pr']
        prTime = row['gh_pr_created_at']
        pushTime = row['gh_pushed_at']
        status = row['tr_status']
        interval[buildId] = [jobId,isPr,prTime,pushTime,status]
    return interval


def jobLogLastStepTime(jobID,path):
    lastStepTime = 0
    path = path + '/' + jobID + '.txt' # 'D:/Users/b/PycharmProjects/jobLog/' + projectName + '/' + jobID + '.txt'
    days_file = open(path, 'r', encoding='UTF-8')
    reTime = re.compile(r'(travis_time):(end):(.*):(start)=(.*),(finish)=(.*),(duration)=(.*)')
    lines = days_file.readlines()
    i = 0
    while i < len(lines):
        if lines[i].find('travis_time') >= 0:
            time = reTime.search(lines[i])
            if time:
                lastStepTime = time.group(7)
                lastStepTime = transferTimeLog(lastStepTime)
        i = i+1
    return lastStepTime

def isPassed(buildId, CIinUse):
    status = CIinUse[buildId][4]
    if status == 'passed':
        return True
    else:
        return False

def nextPassCommitTime(target_out, index, CIinUse, abnormalBuild,path):
    for index, row in target_out[index+1:].iterrows():
        commitTime = row['commit_timestamp']
        buildTime = str(row['gh_build_started_at'])
        buildWay = row['build_way']
        buildId = row['tr_build_id']
        if math.isnan(buildId): # commit在CI文件中没有对应，跳过
            continue
        buildWay = int(buildWay)
        buildId = str(int(buildId))
        if not inTimeScope(buildTime): # 排除gh_build_started_at在2014-8-7之前的build记录
            continue
        if buildId in abnormalBuild:  # 排除gh_build_started_at在2014-8-7之前的build记录
            continue
        if buildWay == 7 or buildWay == 8 or buildWay == 9 :
            if not jobLogExists(buildId,CIinUse,path):  # 跳过找不到对应job log的trigger commit
                continue
            if isPassed(buildId, CIinUse):
                return commitTime
        # 若commit触发build（build_way为1/2/3/4/5/6，写入commit和pr/push和build各步骤
        if buildWay == 1 or buildWay == 2 or buildWay == 3 or buildWay == 4 or buildWay == 5 or buildWay == 6:
            if not jobLogExists(buildId,CIinUse,path):  # 跳过找不到对应job log的trigger commit
                continue
            if isPassed(buildId, CIinUse):
                return commitTime
    return

def writeCommitActivity(buildId, commitTime, CIinUse,writer):
    result = []
    commitTime = commitTime.strftime('%Y/%m/%d %H:%M:%S')
    if buildId in CIinUse:
        jobID = CIinUse[buildId][0]
        status = CIinUse[buildId][4]
        writeStatus = 0
        if status == 'passed' :
            writeStatus = 0
        elif status == 'failed':
            writeStatus =1
        elif status == 'errored':
            writeStatus = 2
        elif status == 'canceled':
            writeStatus = 3
        result.append(jobID)
        result.append("commit")
        result.append(commitTime)
        result.append('')
        result.append(writeStatus)
        print(jobID + " commit," + str(commitTime) + ' ' + str(writeStatus))
    writer.writerow(result)

def  writePushPrActivity(buildId, CIinUse,writer):
    result = []
    if buildId in CIinUse:
        jobID = CIinUse[buildId][0]
        isPr = CIinUse[buildId][1]
        prTime = CIinUse[buildId][2]
        pushTime = CIinUse[buildId][3]
        status = CIinUse[buildId][4]
        writeStatus = 0
        if status == 'passed' :
            writeStatus = 0
        elif status == 'failed':
            writeStatus =1
        elif status == 'errored':
            writeStatus = 2
        elif status == 'canceled':
            writeStatus = 3
        result.append(jobID)
        if isPr == 0:
            result.append('push')
            if pushTime is not np.nan:
                pushTime = transferTimeCI(pushTime)
                result.append(pushTime)
                result.append('')
                result.append(writeStatus)
                print(jobID + "push," + str(pushTime) + ' ' + str(writeStatus))
            else:
                result.append('')
                result.append('')
                result.append(writeStatus)
                print(jobID + "push," + ' ' + ' ' + str(writeStatus))
            writer.writerow(result)
        else:
            if pushTime is np.nan:
                result.append('pull request')
                prTime = transferTimeCI(prTime)
                result.append(prTime)
                result.append('')
                result.append(writeStatus)
                print(jobID + "pr," + str(prTime) + ' ' + str(writeStatus))
            else:
                pushTime = transferTimeCI(pushTime)
                push_time = time.mktime(time.strptime(pushTime, '%Y/%m/%d %H:%M:%S'))
                prTime = transferTimeCI(prTime)
                pr_time = time.mktime(time.strptime(prTime, '%Y/%m/%d %H:%M:%S'))
                if push_time > pr_time:
                    result.append('push')
                    result.append(pushTime)
                    result.append('')
                    result.append(writeStatus)
                    print(jobID + "push," + str(pushTime) + ' ' + str(writeStatus))
                else:
                    result.append('pull request')
                    result.append(prTime)
                    result.append('')
                    result.append(writeStatus)
                    print(jobID + "pr," + str(prTime) + ' ' + str(writeStatus))
            writer.writerow(result)

def writeEndLabel(isTrigger, buildId, CIinUse,writer):
    result = []
    jobID = CIinUse[buildId][0]
    status = CIinUse[buildId][4]
    writeStatus = 0
    if status == 'passed':
        writeStatus = 0
    elif status == 'failed':
        writeStatus = 1
    elif status == 'errored':
        writeStatus = 2
    elif status == 'canceled':
        writeStatus = 3
    if not isTrigger:
        result.append(jobID)
        result.append('skipped')
        result.append('')
        result.append('')
        result.append(writeStatus)
        writer.writerow(result)
    elif isTrigger:
        result.append(jobID)
        result.append(status)
        result.append('')
        result.append('')
        result.append(writeStatus)
        writer.writerow(result)

def writeFixActivity(buildId, CIinUse, target_out, index,abnormalBuild,path,writer):
    result = []
    jobID = CIinUse[buildId][0]
    status = CIinUse[buildId][4]
    if status == 'failed':
        fixStartTime = jobLogLastStepTime(jobID,path)
        fixEndTime = nextPassCommitTime(target_out, index, CIinUse,abnormalBuild,path)
        result.append(jobID)
        result.append('fix')
        result.append(fixStartTime)
        result.append(fixEndTime)
        result.append(1)
        writer.writerow(result)

def extractOneFile(buildId,CIinUse,path, writer):
    jobId = CIinUse[buildId][0]
    status = CIinUse[buildId][4]
    writeStatus = 0
    if status == 'passed':
        writeStatus = 0
    elif status == 'failed':
        writeStatus = 1
    elif status == 'errored':
        writeStatus = 2
    elif status == 'canceled':
        writeStatus = 3
    path = path + '/' + jobId + '.txt'  # 'D:/Users/b/PycharmProjects/jobLog/' + projectName + '/' + jobId + '.txt'
    days_file = open(path, 'r', encoding='UTF-8')
    reFold = re.compile(r'(travis_fold):(start|end):(.*)')
    reTime = re.compile(r'(travis_time):(end):(.*):(start)=(.*),(finish)=(.*),(duration)=(.*)')
    preFold = ''
    preFoldState = ''
    startTime = 0
    finishTime = 0
    timeSHA = ''
    preFoldInFile = ''
    lines = days_file.readlines()
    i=0
    # for i in range(len(lines)):
    while i < len(lines):
        result = []
        result.append(jobId)
        if lines[i].find('travis_fold') >= 0 or lines[i].find('travis_time') >= 0 :
            fold = reFold.search(lines[i])
            time = reTime.search(lines[i])
            if fold :
                preFoldState = fold.group(2)
                preFold = fold.group(3)
            if time :
                startTime = time.group(5)
                startTimeList = [transferTimeLog(startTime)]
                finishTime = time.group(7)
                finishTimeList = [transferTimeLog(finishTime)]
                if preFoldState == 'start':
                    print(preFold + ',' + startTimeList[0] + ',' + finishTimeList[0] + ',' + str(writeStatus))
                    result.append(preFold)
                    result.append(startTimeList[0])
                    result.append(finishTimeList[0])
                    result.append(writeStatus)
                    preFoldInFile = preFold
                    writer.writerow(result)
                else:
                    nextFold = ''
                    timeCount = 1
                    for j in range(i+1,len(lines)):
                        if lines[j].find('travis_time') >= 0:
                            time = reTime.search(lines[j])
                            if time:
                                timeCount = timeCount + 1
                                startTime = time.group(5)
                                startTimeList.append(transferTimeLog(startTime))
                                finishTime = time.group(7)
                                finishTimeList.append(transferTimeLog(finishTime))
                        if lines[j].find('travis_fold') >= 0:
                            fold = reFold.search(lines[j])
                            nextFold = fold.group(3)
                            i = j-1
                            break
                        if j == len(lines) - 1:
                            nextFold = status
                            i = j-1
                            break
                    timeSHA = ''
                    if timeCount == 1:
                        timeSHA = 'between ' + preFoldInFile + ' and ' + nextFold
                        result.append(timeSHA)
                        result.append(startTimeList[0])
                        result.append(finishTimeList[0])
                        result.append(writeStatus)
                        print(timeSHA + ',' + startTimeList[0] + ',' + finishTimeList[0] + ',' + str(writeStatus))
                        writer.writerow(result)
                    elif timeCount>1:
                        k = 1
                        while k <= timeCount :
                            timeSHA = 'between ' + preFoldInFile + ' and ' + nextFold + '.' + str(k)
                            result = []
                            result.append(jobId)
                            result.append(timeSHA)
                            result.append(startTimeList[k-1])
                            result.append(finishTimeList[k-1])
                            result.append(writeStatus)
                            print(timeSHA + ',' + startTimeList[0] + ',' + finishTimeList[0] + ',' + str(writeStatus))
                            writer.writerow(result)
                            k = k+1
        i=i+1
    days_file.close()

def writeExtractFile(targetOUT,CIinUse,abnormalBuild,path,writer):
    target_out = targetOUT[['commit_id', 'commit_timestamp','tr_build_id','gh_build_started_at', 'build_way']]
    for index, row in target_out[:].iterrows():
        commitTime = row['commit_timestamp']
        buildTime = str(row['gh_build_started_at'])
        buildWay = row['build_way']
        buildId = row['tr_build_id']
        if math.isnan(buildId): # commit在CI文件中没有对应，跳过
            continue
        buildWay = int(buildWay)
        buildId = str(int(buildId))
        if not inTimeScope(buildTime): # 排除gh_build_started_at在2014-8-7之前的build记录
            continue
        if buildId in abnormalBuild: # 排除commit时间在对应的pr/push之后的commit
            continue
        # 若commit没有触发build（build_way为7/8/9，只写入commit和pr/push
        if buildWay == 7 or  buildWay == 8 or buildWay == 9 :
            if not jobLogExists(buildId,CIinUse,path):  # 跳过找不到对应job log的trigger commit
                continue
            writeCommitActivity(buildId, commitTime, CIinUse,writer)  # 将git_trigger_commit的时间戳并写入结果文件
            # writePushPrActivity(buildId, CIinUse)  # 判断并结果写入pr/push的时间戳，若CI中缺少记录则为空
            # writeFixActivity(buildId, CIinUse, target_out, index)
            writeEndLabel(False, buildId, CIinUse,writer)
        # 若commit触发build（build_way为1/2/3/4/5/6，写入commit和pr/push和build各步骤
        if buildWay == 1 or buildWay == 2 or buildWay == 3 or buildWay == 4 or buildWay == 5 or buildWay == 6:
            if not jobLogExists(buildId,CIinUse,path):  # 跳过找不到对应job log的trigger commit
                continue
            writeCommitActivity(buildId, commitTime, CIinUse,writer)  # 将git_trigger_commit的时间戳并写入结果文件
            writePushPrActivity(buildId, CIinUse,writer)  # 判断并结果写入pr/push的时间戳，若CI中缺少记录则为空
            extractOneFile(buildId,CIinUse,path, writer) # 到对应job log中查询build的各个步骤的时间戳并写入
            writeEndLabel(True, buildId, CIinUse,writer)
            writeFixActivity(buildId, CIinUse, target_out, index,abnormalBuild,path,writer)

# 运行程序需要改"output","fileOUT","fileCI"文件路径,和“extractOneFile”、“jobLogLastStepTime”、“jobLogExists”方法里的"path"路径

def CIOutJoblogToCSV(fileCI,fileOUT,path):
    CIname = fileCI.split('/')[-1]
    projectName = CIname.split('_')[0]
    title = ['Job ID', 'Activity', 'Start Timestamp', 'Complete Timestamp', 'build status']
    output = "D:/Users/b/PycharmProjects/jobLogExtract/temp/" + projectName + "_extract_temp.csv"  # 输出文件路径
    outfile = open(output, 'w', encoding='gb18030', newline='')
    writer = csv.writer(outfile)
    writer.writerow(title)

    fileOUT = fileOUT  # "D:/南京大学/研一/Thesis/日志整理/COtoCI/" + projectName + "_out.csv"  # CO对应CI文件（XXX_out）文件路径
    targetOUT = pd.read_csv(fileOUT, encoding="unicode_escape")
    targetOUT['commit_timestamp'] = pd.to_datetime(targetOUT['commit_timestamp'])  # 将数据类型转换为日期类型
    targetOUT = targetOUT.sort_values('commit_timestamp', ascending=True)
    targetOUT = targetOUT.reset_index(drop=True)

    fileCI = fileCI  # "D:/南京大学/研一/Thesis/日志整理/CI/" + projectName + "_CI.csv"  # CI文件路径
    targetCI = pd.read_csv(fileCI, encoding="unicode_escape")
    CIinUse = getCIDict(targetCI)  # 从CI中得到{buildId,[jobId,isPr,prTime,pushTime,status]}字典

    abnormalBuild = getabnormalBuild(targetOUT, CIinUse)

    writeExtractFile(targetOUT, CIinUse, abnormalBuild,path,writer)
    return projectName


if __name__ == '__main__':
    a = []
    for i in range(1, len(sys.argv)):
        a.append((sys.argv[i]))

    projectName = CIOutJoblogToCSV(a[0], a[1],a[2])
    print(projectName)
    # CIOutJoblogToCSV('D:/南京大学/研一/Thesis/日志整理/CI/android_CI.csv',
    #                              'D:/南京大学/研一/Thesis/日志整理/COtoCI/android_out.csv',
    #                              'D:/Users/b/PycharmProjects/jobLog/android')