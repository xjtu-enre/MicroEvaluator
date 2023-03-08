import re
import subprocess
import os
import csv
from pathlib import Path

from featureextractor.utils.commitextractor.basedata import ModifyDetail, CommitDetail

def generateLog(url):
    mcDir = url + "/mc/"

    if os.path.exists(mcDir) == False:
        Path(mcDir).mkdir(exist_ok=True)

    gitlogFile = mcDir + "gitlog"
    cmd = "git log --numstat --date=iso > " + gitlogFile
    subprocess.call(cmd, shell=True)

    #os.chdir("C:\\Users\\ding7\\Desktop\\gitrepo\\pythonbug")
    return gitlogFile


#git log --numstat --date=iso > ../celery-gitlog.txt
def processGitLog(fileName, fileList_all, fileList_java, fileList_notest):
    commitCollection_all = list()
    commitCollection_java = list()
    commitCollection_notest = list()

    commitId = ""
    authorName = ""
    date = ""
    fileList = list()
    delList = list()
    addList = list()
    issueIds = list()
    fp = open(fileName, encoding="utf8", errors='ignore')
    num = 0
    for line in fp:
        num += 1
        #print(num)
        if re.match("commit\s[0-9a-zA-Z]+", line):
            if(commitId != ""):
                [isKept, oneCommit] = processPreCmt(commitId, authorName, date, fileList, addList, delList, issueIds, fileList_all)
                if isKept:
                    commitCollection_all.append(oneCommit)
                [isKept, oneCommit] = processPreCmt(commitId, authorName, date, fileList, addList, delList, issueIds, fileList_java)
                if isKept:
                    commitCollection_java.append(oneCommit)
                [isKept, oneCommit] = processPreCmt(commitId, authorName, date, fileList, addList, delList, issueIds, fileList_notest)
                if isKept:
                    commitCollection_notest.append(oneCommit)
                #print("clear", print (len(commitCollection)))
                #clear
                fileList = list()
                delList = list()
                addList = list()
                issueIds = list()

            match = re.match("commit\s[0-9a-zA-Z]+", line)
            commitId = match.group().split("commit ")[1]

        elif re.match("Author: ", line):
            strList = line.split("Author: ")[1].split("<")
            authorName = strList[0].strip()
            #authorEmail = strList[1].split(">")[0]

        elif re.match("Date:   ", line):
            date = line.split("Date:   ")[1].strip("\n")

        elif re.match("[0-9]+	[0-9]+	", line):
            strList = line.strip("\n").split("	")
            addLoc = int(strList[0])
            delLoc = int(strList[1])
            fileName = strList[2]
            fileList.append(fileName)
            addList.append(addLoc)
            delList.append(delLoc)
        elif re.findall("#[0-9]+", line):
            match = re.findall("#[0-9]+", line)
            for issueId in match:
                issueIds.append(int(issueId.split("#")[1]))


    [isKept, oneCommit] = processPreCmt(commitId, authorName, date, fileList, addList, delList, issueIds, fileList_all)
    if isKept:
        commitCollection_all.append(oneCommit)
    [isKept, oneCommit] = processPreCmt(commitId, authorName, date, fileList, addList, delList, issueIds, fileList_java)
    if isKept:
        commitCollection_java.append(oneCommit)
    [isKept, oneCommit] = processPreCmt(commitId, authorName, date, fileList, addList, delList, issueIds, fileList_notest)
    if isKept:
        commitCollection_notest.append(oneCommit)

    fp.close()
    return commitCollection_all, commitCollection_java, commitCollection_notest


def processPreCmt(commitId, authorName, date, fileList, addList, delList, issueIds, filterList):
    newFileList = list()
    newDelList = list()
    newAddList = list()
    for index in range(0, len(fileList)):
        if fileList[index] in filterList: #should be kept
            newFileList.append(fileList[index])
            newDelList.append(delList[index])
            newAddList.append(addList[index])

    #save
    if len(newFileList) == 0:
        isKept = False
    else:
        isKept = True
    modifyDetail = ModifyDetail(newFileList, newAddList, newDelList)
    oneCommit = CommitDetail(commitId, authorName, date, issueIds, modifyDetail)
    return isKept, oneCommit


def getAllFilesByFilter(url):
    # print(dir)
    fileList_all = list()
    fileList_java = list()
    fileList_notest = list()
    # print("dir:"+dir)
    for filename, dirs, files in os.walk(url, topdown=True):
        filename = filename.split(url)[1]
        filename = filename.replace("\\", "/")
        if(filename.startswith(".git") or filename.startswith(".github")):
            continue
        for file in files:
            file_temp = filename + "\\" + file
            file_temp = file_temp[1:]
            file_temp = file_temp.replace("\\", "/")
            fileList_all.append(file_temp)
            if(file.endswith(".java")):
                fileList_java.append(file_temp)
                if "tests\\" not in file and "test\\" not in file:
                    fileList_notest.append(file_temp)

    # print("file benchmark: ", len(fileList_all), len(fileList_py), len(fileList_notest))
    return fileList_all, fileList_java, fileList_notest


def writeCSV(aList, fileName):
    with open(fileName, "w", newline="", encoding='utf-8') as fp:
        writer = csv.writer(fp, delimiter=",")
        writer.writerows(aList)
    # print("commit len: ", len(aList))


def saveCommitCollection(commitCollection):
    resList = list()
    for oneCommit in commitCollection:
        row = oneCommit.toList()
        resList.append(row)
        #print(row)
    return resList


def gitlog(url):
    gitlogFile = generateLog(url)
    [fileList_all, fileList_java, fileList_notest] = getAllFilesByFilter(url)
    [commitCollection_all, commitCollection_java, commitCollection_nontest] = processGitLog(gitlogFile, fileList_all, fileList_java, fileList_notest)
    resList = saveCommitCollection(commitCollection_java)
    java_file_path = url + "/mc/history-java.csv"
    writeCSV(resList, java_file_path)
    return java_file_path

