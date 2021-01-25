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
import os
import sys

def transformAct(activity):
    activityName = activity
    reActivity = re.compile(r'(.*)(\.[0-9]*$)')
    if activity.find('between') >= 0:
            activityName = 'script'
    else:
        if reActivity.match(activity):
            activityMatch = reActivity.search(activity)
            activityName = activityMatch.group(1)
    return activityName

def writeOneRow(preJobId, preActivity, preStartTime, preEndTime, preBuildStatus,writer):
    result = []
    result.append(preJobId)
    activityName = transformAct(preActivity)
    result.append(activityName)
    result.append(preStartTime)
    result.append(preEndTime)
    result.append(preBuildStatus)
    print(preJobId + ',' + activityName + ',' + preStartTime + ',' + preEndTime + '' + preBuildStatus)
    writer.writerow(result)

def betweenSame(activity):
    reActivity = re.compile(r'(between) (.*)(\.[0-9]*) (and) (.*)(\.[0-9]*)')
    if reActivity.match(activity) :
        activityMatch = reActivity.search(activity)
        preActivityName = activityMatch.group(2)
        LastActivityName = activityMatch.group(5)
        if preActivityName == LastActivityName:
            return True
    return False

def same(activity, preActivity):
    if activity == preActivity:
        return True
    reActivity = re.compile(r'(.*)(\.[0-9]*$)')
    if reActivity.match(activity) and reActivity.match(preActivity):
        activityMatch = reActivity.search(activity)
        preActivityMatch = reActivity.search(preActivity)
        activityName = activityMatch.group(1)
        preActivityName = preActivityMatch.group(1)
        if activityName == preActivityName:
            return True
    return False

def CSVMerge(projectName,outputFile):
    title = ['Job ID','Activity','Start Timestamp','Complete Timestamp','build status']
    # output = "D:/Users/b/PycharmProjects/jobLogExtract/merge/" + projectName + "_extract_merge.csv"  # 输出文件路径
    output = outputFile + projectName + "_extract_merge.csv"
    outfile = open(output, 'w', encoding='gb18030', newline='')
    writer = csv.writer(outfile)
    writer.writerow(title)

    # fileExtractTemp = "D:/Users/b/PycharmProjects/jobLogExtract/temp/" + projectName + "_extract_temp.csv"
    fileExtractTemp = outputFile + projectName + "_extract_temp.csv"
    targetTemp = pd.read_csv(fileExtractTemp, encoding="unicode_escape")
    target_start = targetTemp[['Job ID', 'Activity', 'Start Timestamp', 'Complete Timestamp', 'build status']]

    preJobId = ''
    preActivity = ''
    preStartTime = ''
    preEndTime = ''
    preBuildStatus = ''
    for index, row in target_start.iterrows():
        jobId = str(row['Job ID'])
        activity = str(row['Activity'])
        startTime = str(row['Start Timestamp'])
        endTime = str(row['Complete Timestamp'])
        buildStatus = str(row['build status'])
        # print(jobId + ' ' + activity + ' ' + startTime + ' ' + endTime + ' ' + buildStatus)
        if index == 0:
            # updatePre(jobId, activity, startTime, endTime, buildStatus)
            preJobId = jobId
            preActivity = activity
            preStartTime = startTime
            preEndTime = endTime
            preBuildStatus = buildStatus
            continue
        if activity.find('between') >= 0 and betweenSame(activity):
                continue
        elif same(activity, preActivity) != True :
            writeOneRow(preJobId, preActivity, preStartTime, preEndTime, preBuildStatus,writer)
            # updatePre(jobId, activity, startTime, endTime, buildStatus)
            preJobId = jobId
            preActivity = activity
            preStartTime = startTime
            preEndTime = endTime
            preBuildStatus = buildStatus
        elif same(activity, preActivity) == True:
            preEndTime = endTime
        if index == len(target_start)-1:
            writeOneRow(jobId, activity, startTime, endTime, buildStatus,writer)

if __name__ == '__main__':
    a = []
    for i in range(1, len(sys.argv)):
        a.append((sys.argv[i]))
    CSVMerge(a[0], a[1])

