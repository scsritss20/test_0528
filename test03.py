#!/usr/bin/python2.6
#-*- coding: utf-8 -*-

import ftplib
import os
import sys
import datetime
import random
import time
import json
import time
import logging
import datetime
FTP_IP = ''
STREXP = ''


# 执行的信息打印到日志文件默认为家目录下的Client.log
def getLog():
    logdir = "/tmp"
    logger = logging.getLogger('Clientlog')
    logger.setLevel(logging.DEBUG)
    logName = logdir + r"/" + "Client.log"
    fh = logging.FileHandler(logName)
    fh.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    log_format = logging.Formatter(
        "%(asctime)s-%(name)s-%(levelname)s-%(message)s-[%(filename)s:%(lineno)d]")
    fh.setFormatter(log_format)
    ch.setFormatter(log_format)
    logger.addHandler(fh)
    logger.addHandler(ch)
    # logger.warning(msg)
    return logger

logger = getLog()
# ftp工具类


class FtpTools():
    def __init__(self, ftpipstr, ftpuser, ftppasswd):
        self.ftp = ftplib.FTP()
        self.ftpiplist = ftpipstr.split(',')
        ftpip = random.choice(self.ftpiplist)
        global FTP_IP
        global STREXP
        FTP_IP = ftpip
        try:
            self.ftp.connect(ftpip, 21, 10)
            msg = 'conncet success'
            logger.info(msg)
        except Exception, e:
            STREXP = 'FTPIP:' + ftpip + " conncet failed - %s" % e
            msg = STREXP
            logger.error(msg)
            # print "conncet failed1 - %s" % e
            asdfgh.test="aaaaaa12wse"
        else:
            try:
                self.ftp.login(ftpuser, ftppasswd)
            except Exception, e:
                time.sleep(5)
                try:
                    self.ftp.login(ftpuser, ftppasswd)
                except Exception, e:
                    STREXP = 'FTPIP:' + ftpip + " login failed - %s" % e
                    msg = STREXP
                    logger.error(msg)

    def upLoad(self, srcFile, backPath):
        try:
            file_handler = open(srcFile, 'rb')
            bufsize = 1024
            self.ftp.storbinary("STOR %s" % os.path.basename(
                srcFile), file_handler, bufsize)
            file_handler.close()
        except Exception, e:
            msg = 'FTPIP:' + ftpip + \
                ' upLoad file[' + '] to [' + backPath + \
                '] failed! result is: ' + str(e)
            logger.error(msg)
            return 'FTPIP:' + ftpip + ' upLoad file[' + '] to [' + backPath + '] failed! result is: ' + str(e)
        return 0

    def quit(self):
        self.ftp.quit()

# 是否删除


def DelFile(filePath, isDel):
    if isDel == "Y":
        DelCmd = "rm -f %s " % filePath
        os.popen(DelCmd)

# 调web客户端上传json数据


def getResponse(starttime, endtime, gznum, count, status, des, ID):
    strI = """{"task_id":"%s","status":"%s","des":"%s","count":"%s","start_time":"%s","end_time":"%s"}""" % (
        ID, status, des, count, starttime, endtime)
    # 将接收的数据写入文件
    f = open('/tmp/logback.txt', 'a')
    f.write(strI + '\n')
    f.close()
    # 将文件中的数据进行拼接
    strlist = []
    with open('/tmp/logback.txt', 'r') as f:
        for i in f.readlines():
            strlist.append(i.strip('\n\r'))
    strII = ','.join(strlist)
    str1 = """{"data":[%s]}""" % strII
    # 判断curl命令是否存在，如果存在则用命令传输数据
    testcmd = "command -v curl >/dev/null;echo $?"
    if os.popen(testcmd).readlines()[0].strip('\n\r') == "0":
        try:
            cmd = """ curl --connect-timeout 10 -H "Content-type: application/json" -X POST -d '%s' http://itsmlogback.cnsuning.com/archive_result """ % str1
            results = os.popen(cmd).readlines()
            # 如果执行成功则清空文件，否则打印失败
            if results[0].strip('\n\r') == 'success':
                cmd = "> /tmp/logback.txt"
                os.popen(cmd)
                msg = 'curl success'
                logger.info(msg)
            else:
                print "curl failed"
        except:
            # print "curl failed!"
            msg = 'curl failed'
            logger.error(msg)
    # 如果没有curl命令则用requests的post方法
    else:
        data = {}
        dictlist = []
        strlist = []
        with open('/tmp/logback.txt', 'r') as f:
            for i in f.readlines():
                strlist.append(i.strip('\n\r'))
        for i in strlist:
            j = eval(i)
            dictlist.append(j)
        data = {"data": dictlist}
        try:
            url = 'http://itsmlogback.cnsuning.com/archive_result'
            import requests
            r = requests.post(url, data=json.dumps(data), timeout=10)
            print r.status_code
            if r.status_code == 200:
                cmd = "> /tmp/logback.txt"
                os.popen(cmd)
                msg = 'post success!'
                logger.info(msg)
            else:
                # print "Post failed!"
                msg = 'Post failed!'
                logger.error(msg)
        except:
            # print "Post failed!"
            msg = 'Post failed!'
            logger.error(msg)

# 日志备份函数


def Backup(date, ip, sysname, soft_type, logback_tag, logFile, backPath, isDel, isGzip, ftpipstr, ftpuser, ftppasswd, ID):
    starttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # 取出备份日志的路径和日志名称
    logDir = os.path.dirname(logFile)
    logName = os.path.basename(logFile)
    # 判断日志路径和日志是否存在
    dirExsitCmd = """ test -d %s; echo $? """ % logDir
    fileExsitCmd = """ find %s -maxdepth 1 -name "%s" | wc -l""" % (
        logDir, logName)
    fileExsitRet = os.popen(dirExsitCmd).readlines()[0].strip('\r\n')
    if fileExsitRet != "0":
        des = 'logDir[' + logDir + '] not exsit!'
        msg = des
        logger.warning(msg)
        status = '1002'
        endtime = data()
        count = 0
        gznum = 0
        getResponse(starttime, endtime, gznum, count, status, des, ID)
        sys.exit()
    fileExsitRet = os.popen(fileExsitCmd).readlines()[0].strip('\r\n')
    if fileExsitRet == "0":
        des = 'No logFile[' + logName + '] found in [' + logDir + ']!'
        msg = des
        logger.warning(msg)
        print des
        status = '2001'
        endtime = data()
        count = 0
        gznum = 0
        getResponse(starttime, endtime, gznum, count, status, des, ID)
        sys.exit()
    # 是否压缩
    if isGzip == 'Y':
        gzipFinishedCmd = """ find %s -maxdepth 1 -name "%s" ! -name "*.gz" | wc -l """ % (
            logDir, logName)
        gznum = os.popen(gzipFinishedCmd).readlines()[0].strip('\r\n')
        compressFilesCmd = """ ls %s | grep -v gz$ | xargs -I {} gzip {} """ % logFile
        os.popen(compressFilesCmd)
    else:
        gznum = 0
    ftpInstalledCmd = "command -v ftp >/dev/null; echo $?"
    if os.popen(ftpInstalledCmd).readlines()[0].strip('\r\n') != "0":
        des = "ftp Command not found!"
        msg = des
        logger.error(msg)
        print des
        endtime = data()
        status = '1003'
        count = 0
        getResponse(starttime, endtime, gznum, count, status, des, ID)
        sys.exit()

    # 判断目录是否存在，存在就进去，不存在就创建
    try:
        FtpClient = FtpTools(ftpipstr, ftpuser, ftppasswd)
        if STREXP:
            raise ftplib.Error(STREXP)
        else:
            for path in backPath.split('/'):
                try:
                    FtpClient.ftp.cwd(path)
                    msg = 'Get into' + path + ' successfully'
                    logger.info(msg)
                except Exception, e:
                    try:
                        msg = 'Get into' + path + ' failed'
                        logger.error(msg)
                        time.sleep(random.uniform(3, 5))
                        FtpClient.ftp.mkd(path)
                        msg = 'The dir' + path + ' was created successfully!'
                        logger.info(msg)
                        FtpClient.ftp.cwd(path)
                        msg = 'Second entry' + path + ' successfully'
                        logger.info(msg)
                    except Exception, e:
                        try:
                            msg = 'create dir ' + path + ' failed!'
                            logger.error(msg)
                            time.sleep(random.uniform(3, 5))
                            FtpClient.ftp.cwd(path)
                            msg = 'Try to entry ' + path + ' successfully!'
                            logger.info(msg)
                        except Exception, e:
                            raise ftplib.Error(
                                FTP_IP + " mkdir " + path + " failed:" + str(e))
    except Exception, e:
        des = str(e)
        msg = des
        logger.error(msg)
        print des
        endtime = data()
        status = '1004'
        count = 0
        getResponse(starttime, endtime, gznum, count, status, des, ID)
        sys.exit()
    # 进行日志备份
    try:
        count = 0
        listFilesCmd = """ find %s -maxdepth 1 -name "%s" """ % (
            logDir, logName)
        fileList = os.popen(listFilesCmd).readlines()
        # 记录传输失败的文件的列表
        faillist = []
        for file in fileList:
            srcFile = file.strip('\r\n')
            uploadRet = FtpClient.upLoad(srcFile, backPath)
            if uploadRet == 0:
                DelFile(srcFile, isDel)
                count += 1
                msg = file + 'upload sucess'
                logger.info(msg)
            else:
                faillist.append(srcFile)
                print uploadRet
                msg = uploadRet
                logger.warning(msg)
        if len(faillist) != 0:
            status = '1001'
            des = 'upLoad file' + ' to ' + FTP_IP + ":" + backPath + ' failed! '
            endtime = data()
            getResponse(starttime, endtime, gznum, count, status, des, ID)
            msg = des
            logger.error(msg)
            sys.exit()
        else:
            status = '0'
            endtime = data()
            des = "Success"
            msg = 'All file upload success!'
            logger.info(msg)
            # return endtime, gznum,str(count),status
            getResponse(starttime, endtime, gznum, count, status, des, ID)
    finally:
        FtpClient.quit()
        sys.exit()


def data():
    endtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return endtime

# 进程如有僵死则先等待十秒钟，在检查一边发现进程还在就之前的进程杀掉，将信息返回，然后在执行新的任务


def Execute(date, ip, sysname, soft_type, logback_tag,
            logFile, backPath, isDel, isGzip, ftpipstr, ftpuser, ftppasswd, ID, logid):
    cmd = """ ps -ef | grep LogClient.py|grep %s|grep -v grep |awk '{print $NF}' """ % logid
    taskId = os.popen(cmd).readlines()
    if user == "root":
        if len(taskId) > 1:
            time.sleep(60)
            taskId = os.popen(cmd).readlines()
            if len(taskId) > 1:
                starttime = data()
                endtime = data()
                gznum = 0
                count = 0
                status = '1007'
                des = 'The logback process LogClient.py is dead and it has been killed by root'
                msg = des
                logger.error(msg)
                cmd1 = """ ps -ef | grep LogClient.py|grep %s|grep -v grep|grep -v %s |awk '{print $(NF-2)}'|head -1 """ % (
                    logid, ID)
                old_id = os.popen(cmd1).read().strip('\n')
                getResponse(starttime, endtime, gznum,
                            count, status, des, old_id)
                cmd2 = """ ps -ef | grep LogClient.py|grep %s|grep -v grep|grep -v %s |awk '{print $2}'|xargs kill -9 """ % (
                    logid, ID)
                result = os.popen(cmd2).readlines()
                Backup(date, ip, sysname, soft_type, logback_tag,
                       logFile, backPath, isDel, isGzip, ftpipstr, ftpuser, ftppasswd, ID)
            else:
                Backup(date, ip, sysname, soft_type, logback_tag,
                       logFile, backPath, isDel, isGzip, ftpipstr, ftpuser, ftppasswd, ID)
        else:
            Backup(date, ip, sysname, soft_type, logback_tag,
                   logFile, backPath, isDel, isGzip, ftpipstr, ftpuser, ftppasswd, ID)
    elif user == "logback":
        if len(taskId) > 2:
            time.sleep(60)
            taskId = os.popen(cmd).readlines()
            if len(taskId) > 2:
                starttime = data()
                endtime = data()
                gznum = 0
                count = 0
                status = '1008'
                des = 'The process LogClient.py of logback was dead !'
                msg = des
                logger.error(msg)
                cmd1 = """ ps -ef | grep LogClient.py|grep %s|grep -v grep|grep -v %s |awk '{print $(NF-2)}'|head -1' """ % (
                    logid, ID)
                old_id = os.popen(cmd1).read().strip('\n')
                getResponse(starttime, endtime, gznum,
                            count, status, des, old_id)
                getResponse(starttime, endtime, gznum, count, status, des, ID)
            else:
                Backup(date, ip, sysname, soft_type, logback_tag,
                       logFile, backPath, isDel, isGzip, ftpipstr, ftpuser, ftppasswd, ID)
        else:
            Backup(date, ip, sysname, soft_type, logback_tag,
                   logFile, backPath, isDel, isGzip, ftpipstr, ftpuser, ftppasswd, ID)
    else:
        msg = 'No back user find!'
        logger.error(msg)

def clearLog():
    file = "/tmp" + r"/" + "Client.log"
    if os.path.exists(file):
	fsize = os.path.getsize(file)
	if fsize > 10485760:
		cmd = """ > %s """ % file
		os.popen(cmd)
	else:
		print "The Client.log will be cleaned up when it is larger than 10M"
    else:
        print file + 'not exists!'

if __name__ == "__main__":
    clearLog()
    if len(sys.argv) != 15:
        endtime = data()
        print "The paranum must be 15 !"
        msg = 'The paranum must be 15 !'
        logger.error(msg)
        sys.exit()
    else:
        date = sys.argv[1]
        ip = sys.argv[2]
        sysname = sys.argv[3]
        soft_type = sys.argv[4]
        logback_tag = sys.argv[5]
        logFile = sys.argv[6]
        backPath = date + "/" + sysname + "/" + ip + \
            "/" + soft_type + "/" + logback_tag + "/"
        isDel = sys.argv[7]
        isGzip = sys.argv[8]
        ftpipstr = sys.argv[9]
        ftpuser = sys.argv[10]
        ftppasswd = sys.argv[11]
        ID = sys.argv[12]
        logid = sys.argv[13]
        user = sys.argv[14]
        msg = 'The whole arguments is' + date + ip + sysname + soft_type + logback_tag + \
            logFile + backPath + isDel + isGzip + ftpipstr + \
            ftpuser + ftppasswd + ID + logid + user
        logger.info(msg)
        Execute(date, ip, sysname, soft_type, logback_tag,
                logFile, backPath, isDel, isGzip, ftpipstr, ftpuser, ftppasswd, ID, logid)
