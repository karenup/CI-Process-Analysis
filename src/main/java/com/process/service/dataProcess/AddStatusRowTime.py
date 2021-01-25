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



def writeOneRow(preJobId, preActivity, preStartTime, preEndTime, preBuildStatus, writer):
    result = []
    result.append(preJobId)
    result.append(preActivity)
    result.append(preStartTime)
    result.append(preEndTime)
    result.append(preBuildStatus)
    print(preJobId + ',' + preActivity + ',' + preStartTime + ',' + preEndTime + '' + preBuildStatus)
    writer.writerow(result)

def addStatusRowTime(projectName):
    title = ['Job ID', 'Activity', 'Start Timestamp', 'Complete Timestamp', 'build status']
    output = "D:/Users/b/PycharmProjects/jobLogExtract/extract/" + projectName + "_extract.csv"  # 输出文件路径
    outfile = open(output, 'w', encoding='gb18030', newline='')
    writer = csv.writer(outfile)
    writer.writerow(title)

    fileExtractTemp = "D:/Users/b/PycharmProjects/jobLogExtract/merge/" + projectName + "_extract_merge.csv"
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
        if activity == 'passed' or activity == 'failed' or activity == 'errored' or activity == 'canceled':
            startTime = preEndTime
            endTime = preEndTime
            writeOneRow(jobId, activity, startTime, endTime, buildStatus, writer)
            continue
        if activity == 'skipped':
            startTime = preStartTime
            endTime = preStartTime
            writeOneRow(jobId, activity, startTime, endTime, buildStatus, writer)
            continue
        writeOneRow(jobId, activity, startTime, endTime, buildStatus, writer)
        preJobId = jobId
        preActivity = activity
        preStartTime = startTime
        preEndTime = endTime
        preBuildStatus = buildStatus

if __name__ == '__main__':
    a = []
    for i in range(1, len(sys.argv)):
        a.append((sys.argv[i]))
    addStatusRowTime(a[0])
