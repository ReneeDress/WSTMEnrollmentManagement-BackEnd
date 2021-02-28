import decimal
import pymysql
import json
import time, datetime


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)

class OnlyDateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)
        # print(obj)


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)
        # print(obj)


class NoSecondEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d %H:%M")
        else:
            return json.JSONEncoder.default(self, obj)
        # print(obj)


def connect(hostaddr, usr, pwd, hostport, database):
    # 打开数据库连接
    db = pymysql.connect(host=hostaddr, user=usr, password=pwd, port=hostport, db=database)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("SELECT VERSION()")

    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()

    print("Database version : %s " % data)

    # 关闭数据库连接
    db.close()


def change(hostaddr, usr, pwd, hostport, database, sqlphase, sqlheadphase):
    cols = selecthead(hostaddr, usr, pwd, hostport, database, sqlheadphase)
    # print(cols, len(cols))
    # 打开数据库连接
    db = pymysql.connect(host=hostaddr, user=usr, password=pwd, port=hostport, db=database)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 更新语句
    sql = sqlphase
    try:
        # 执行SQL语句
        cursor.execute(sql)
        print('success', sql)
        # 提交到数据库执行
        db.commit()
        # 关闭数据库连接
        db.close()
        return 'success'
    except:
        print('error')
        # 发生错误时回滚
        db.rollback()
        # 关闭数据库连接
        db.close()
        return 'error'

    # 关闭数据库连接
    db.close()
    return 'error'


def selecthead(hostaddr, usr, pwd, hostport, database, sqlphase):
    if sqlphase == None:
        return 'abcdefghijklmnopqrstuvwxyz'
    # 打开数据库连接
    db = pymysql.connect(host=hostaddr, user=usr, password=pwd, port=hostport, db=database)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = sqlphase
    cols = []
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            # fname = row[0]
            # lname = row[1]
            # age = row[2]
            # sex = row[3]
            # income = row[4]
            # # 打印结果
            # print("fname=%s,lname=%s,age=%s,sex=%s,income=%s" % \
            #       (fname, lname, age, sex, income))
            # print(len(row))
            # print(row)
            # print(row[3], row[-2])
            if row[3]!='Pwd':
                cols.append(row[3])
        # print(cols)

    except:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()

    return cols


def select(hostaddr, usr, pwd, hostport, database, sqlphase, sqlheadphase):
    cols = selecthead(hostaddr, usr, pwd, hostport, database, sqlheadphase)
    # print(cols, len(cols))
    # 打开数据库连接
    db = pymysql.connect(host=hostaddr, user=usr, password=pwd, port=hostport, db=database)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = sqlphase
    arr = []
    # print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # print(results)
        # print(list(results))
        # print(type(results))
        # results = list(results)
        for row in results:
            # print(row)
            rowdict = {}
            for i in range(0, len(row)):
                rowdict[cols[i]] = row[i]
            # rowjson = json.dumps(rowdict)
            # print(rowjson)
            arr.append(rowdict)
        # print(arr)

    except:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()

    return arr


if __name__=="__main__":
    hostaddr = "cdb-l8bcqqr2.bj.tencentcdb.com"
    usr = "root"
    pwd = "061224renee"
    hostport = 10157
    database = "ECUPL"
    view = "ARCHIVE"
    sqlheadphase = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (
    database, view)
    sqlphase = "SELECT * FROM %s;" % view
    connect(hostaddr, usr, pwd, hostport, database)
    # selecthead(hostaddr, usr, pwd, hostport, database, sqlheadphase)
    arr = select(hostaddr, usr, pwd, hostport, database, sqlphase, sqlheadphase)
    # print(arr)

    # print('\n\n==========\n本节功能：用户提交法援申请。\n获取参数：案件分类-CaseCate、持续法援-LastCaseNum、当事人Id-UserId、案情陈述-CaseDetail、当事文件-CaseFile。')
    # caseCate = '婚姻家事'
    # nowY = time.strftime("%Y", time.localtime())
    # numHead = nowY+caseCate[0]
    # print('案件编号前缀：'+numHead)
    # selectCaseNumMax = "SELECT MAX(RIGHT(CaseNum, 5)) FROM CaseInfo WHERE LEFT(CaseNum, 5)='%s';" % numHead
    # print(select(hostaddr, usr, pwd, hostport, database, selectCaseNumMax, None))
    # if (select(hostaddr, usr, pwd, hostport, database, selectCaseNumMax, None))[0]['D'] == None:
    #     nowCaseNumMax = 0
    # else:
    #     nowCaseNumMax = int((select(hostaddr, usr, pwd, hostport, database, selectCaseNumMax, None))[0]['D'])
    # print('当前前缀最大编号：'+str(nowCaseNumMax))
    #
    # numTail = '{:0>5}'.format(str(nowCaseNumMax + 1))
    # caseNum = numHead + numTail
    # print('案件编号：'+caseNum)
    # lastCaseNum = None
    # print('持续法援：' + str(lastCaseNum))
    # userId = 1
    # print('当事人Id：' + '{:0>10}'.format(str(userId)))
    # caseDetail = ''
    # print('案情陈述：' + caseDetail)
    # caseFile = []
    # print('当事文件：' + ', '.join(caseFile))
    #
    # state = '待分配'
    # adminId2 = ''
    # selectAdminId2 = "SELECT StudentId FROM Admin WHERE AGroup='%s' AND AType='%s';" % (caseCate, '研究生成员')
    # adminId2 = select(hostaddr, usr, pwd, hostport, database, selectAdminId2, None)[0]['D']
    # print('审核人Id：' + adminId2)
    # insertNewCaseByUser = "INSERT INTO CaseInfo(CaseNum, CaseCate, SubmitTime, LastCaseNum, UserId, CaseDetail, CaseFile) VALUES ('%s', '%s', '%s', '%s', %u, '%s', '%s')" \
    #                       %(caseNum, caseCate, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), lastCaseNum, userId, caseDetail, caseFile)
    # print(insertNewCaseByUser)
    # time.sleep(0.1)
    # insertNewCaseState = "INSERT INTO CaseState(CaseNum, State, AdminId2) VALUES ('%s', '%s', '%s')" \
    #                      % (caseNum, state, adminId2)
    # print(insertNewCaseState)
    #
    # # change(hostaddr, usr, pwd, hostport, database, insertNewCaseByUser, None)
    # time.sleep(0.1)
    # change(hostaddr, usr, pwd, hostport, database, insertNewCaseState, None)

    # print('\n\n==========\n本节功能：法援人员接收申请。\n获取参数：案件编号-CaseNum、经办人Id-AdminId1。')
    # caseNum = caseNum
    # adminId1 = ''
    # state = '待处理'
    # updateCaseInfo = "UPDATE CaseInfo SET CreateTime='%s' WHERE CaseNum='%s'" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), caseNum)
    # print(updateCaseInfo)
    # updateCaseState = "UPDATE CaseState SET AdminId1='%s' AND State='%s' WHERE CaseNum='%s'" % (adminId1, state, caseNum)
    # print(updateCaseState)
    #
    # print('\n\n==========\n本节功能：法援人员处理申请。\n获取参数：案件编号-CaseNum、法援意见-LegalAid、法援文件-LegalAidFile、案件摘要-Abstract。')
    # caseNum = '2021劳00001'
    # legalAid = ''
    # legalAidFile = []
    # abstract = ''
    # state = '待审核'
    # updateCaseInfoByAdmin1 = "UPDATE CaseInfo SET LegalAid='%s' AND LegalAidFile='%s' WHERE CaseNum='%s'" % (legalAid, legalAidFile, caseNum)
    # print(updateCaseInfoByAdmin1)
    # updateCaseStateByAdmin1 = "UPDATE CaseState SET Abstract='%s' AND State='%s' WHERE CaseNum='%s'" % (abstract, state, caseNum)
    # print(updateCaseStateByAdmin1)
    #
    # print('\n\n==========\n本节功能：审核人员处理法援。\n获取参数：案件编号-CaseNum、审核意见-Audit、是否通过-isPass、法援意见-LegalAid、法援文件-LegalAidFile、案件摘要-Abstract。')
    # caseNum = caseNum
    # isPass = True
    # audit = ''
    # newLegalAid = legalAid
    # newLegalAidFile = legalAidFile
    # newAbstract = abstract
    # if isPass:
    #     state = '待评价'
    # else:
    #     state = '待处理'
    # updateCaseInfoByAdmin2 = "UPDATE CaseInfo SET LegalAid='%s' AND LegalAidFile='%s' WHERE CaseNum='%s'" % (newLegalAid, newLegalAidFile, caseNum)
    # print(updateCaseInfoByAdmin2)
    # updateCaseStateByAdmin2 = "UPDATE CaseState SET Audit='%s' AND AuditTime='%s' AND Abstract='%s' AND State='%s' WHERE CaseNum='%s'" % (audit, time.strftime("%Y-%m-%d %H:%M:%S"), newAbstract, state, caseNum)
    # print(updateCaseStateByAdmin2)
    #
    # print('\n\n==========\n本节功能：用户评价法援意见。\n获取参数：案件编号-CaseNum、评价-Comment。')
    # caseNum = caseNum
    # comment = ''
    # state = '已归档'
    # updateCaseInfoByUser = "UPDATE CaseInfo SET Comment='%s' WHERE CaseNum='%s'" % (comment, caseNum)
    # print(updateCaseInfoByUser)
    # updateCaseStateByUser = "UPDATE CaseState SET State='%s' WHERE CaseNum='%s'" % (state, caseNum)
    # print(updateCaseStateByUser)
    #
    # # change(hostaddr, usr, pwd, hostport, database, insertsql, sqlheadphase)
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    '''
        待分配 - AdminId1 IS NULL AND AdminId2 IS NOT NULL
        待处理 - LegalAid IS NULL AND AdminId1 IS NOT NULL
        待审核 - Audit IS NULL AND AdminId2 IS NOT NULL AND LegalAid IS NOT NULL
        待评价 - Comment IS NULL AND Audit IS NOT NULL ???
        已归档 - Comment IS NOT NULL
    '''
    '''
        等待处理 - CreateTime IS NULL
        正在处理 - (CreateTime IS NOT NULL AND LegalAid IS NULL) OR Audit IS NULL ???
        确认评价 - LegalAid IS NOT NULL
    '''