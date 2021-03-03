from flask import *
from db import *
from colors import *
from datetime import date, timedelta, datetime
from flask_cors import *
import copy

app = Flask(__name__)
app.secret_key = 'schooldatabase'  # Change this!

CORS(app, supports_credentials=True)

hostaddr = "cdb-l8bcqqr2.bj.tencentcdb.com"
usr = "root"
pwd = "061224renee"
hostport = 10157
database = "SCHOOL"

# view = "C"
# sqlheadphase = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (database, view)
# sqlphase = "SELECT * FROM %s;" % view


@app.route('/')
def hello_world():
    return 'Hello School!'


def ghmm():
    view = "T"
    sqlheadphase = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (database, view)
    sqlphase = "SELECT gh, mm FROM %s;" % view
    gh = select(hostaddr, usr, pwd, hostport, database, sqlphase, sqlheadphase)

    return gh


'''
    获取所有教师信息（不含密码）
'''
@app.route('/teacher', methods=["GET"])
def teacher():
    view = "T_NOP"
    sqlheadphase = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (database, view)
    sqlphase = "SELECT * FROM %s;" % view
    tea = select(hostaddr, usr, pwd, hostport, database, sqlphase, sqlheadphase)

    return json.dumps(tea, cls=OnlyDateEncoder)


def xhmm():
    view = "S"
    sqlheadphase = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (
    database, view)
    sqlphase = "SELECT xh, mm FROM %s;" % view
    xh = select(hostaddr, usr, pwd, hostport, database, sqlphase, sqlheadphase)

    return xh


'''
    获取所有学生信息（不含密码）
'''
@app.route('/student', methods=["GET"])
def student():
    view = "S_NOP"
    sqlheadphase = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (
        database, view)
    sqlphase = "SELECT * FROM %s;" % view
    stu = select(hostaddr, usr, pwd, hostport, database, sqlphase, sqlheadphase)

    return json.dumps(stu, cls=OnlyDateEncoder)


'''
    获取指定学生信息（不含密码）
'''
@app.route('/student/<xh>', methods=["GET"])
def studentXh(xh):
    view = "S_NOP"
    sqlheadphase = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (database, view)
    sqlphase = "SELECT * FROM %s WHERE xh='%s';" % (view, xh)
    stu = select(hostaddr, usr, pwd, hostport, database, sqlphase, sqlheadphase)

    return json.dumps(stu, cls=OnlyDateEncoder)


'''
    登录验证
'''
@app.route('/login', methods=["GET", "POST"])
def login():
    teacher = ghmm()
    student = xhmm()
    reqJson = request.get_json(silent=True)
    userid = reqJson['usr']
    passwd = reqJson['pwd']
    # print(userid, passwd)
    # userid = '20720610'
    # passwd = 'mztxy123'
    xhform = {
        'xh': userid,
        'xm': passwd
    }
    ghform = {
        'gh': userid,
        'xm': passwd
    }
    # userinfo = {}
    if ghform in teacher:
        userinfo = {
            'id': userid,
            'type': True,
            'status': 'success'
        }
    elif xhform in student:
        userinfo = {
            'id': userid,
            'type': False,
            'status': 'success'
        }
    else:
        userinfo = {
            'status': 'error'
        }

    return json.dumps(userinfo, cls=DateEncoder)


'''
    
'''
@app.route('/modifypwd', methods=["GET", "POST"])
def modifyPwd():
    teacher = ghmm()
    student = xhmm()
    reqJson = request.get_json(silent=True)
    print(reqJson)
    type = reqJson['usertype']
    id = reqJson['id']
    oldpwd = reqJson['oldpwd']
    newpwd = reqJson['newpwd']
    if type:
        tea = {
            'gh': id,
            'xm': oldpwd
        }
        if tea in teacher:
            sqlphase = "UPDATE T SET mm='%s' WHERE gh='%s';" %(newpwd, id)
            ret = change(hostaddr, usr, pwd, hostport, database, sqlphase, None)
            return ret
        else:
            return 'oldpwdwrong'
    else:
        stu = {
            'xh': id,
            'xm': oldpwd
        }
        if stu in student:
            sqlphase = "UPDATE S SET mm='%s' WHERE xh='%s';" % (newpwd, id)
            ret = change(hostaddr, usr, pwd, hostport, database, sqlphase, None)
            return ret
        else:
            return 'oldpwdwrong'


'''
    获取前后yearrange年学期信息
'''
@app.route('/avaterm/<yearrange>', methods=['GET', 'POST'])
def avaterm(yearrange):
    try:
        yearrange = int(yearrange)
        avaxq = []
        curYear = (datetime.now()).strftime("%Y")
        curYear = int(curYear)
        for y in range(curYear - yearrange, curYear + 1 + yearrange):
            for t in range(1, 5):
                strt = '0' + str(t)
                stry = str(y)
                term = stry + strt
                dictterm = { 'xq': term }
                avaxq.append(dictterm)
        return json.dumps(avaxq, cls=OnlyDateEncoder)

    except:
        return 'error'


'''
    获取已有开课学期信息
'''
@app.route('/allterm', methods=['GET', 'POST'])
def allterm():
    view = "O"
    sqlheadphase = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (database, view)
    sqlphase = "SELECT DISTINCT xq FROM %s ORDER BY xq ASC;" % view
    allxq = select(hostaddr, usr, pwd, hostport, database, sqlphase, sqlheadphase)
    # allxq.insert(0, { 'xq': '所有学期' })

    return json.dumps(allxq, cls=OnlyDateEncoder)


'''
    获取所有院系信息
'''
@app.route('/alldept', methods=['GET', 'POST'])
def alldept():
    view = "D"
    sqlheadphase = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (database, view)
    sqlphase = "SELECT * FROM %s ORDER BY yxh ASC;" % view
    allxy = select(hostaddr, usr, pwd, hostport, database, sqlphase, sqlheadphase)

    return json.dumps(allxy, cls=OnlyDateEncoder)


'''
    新增学生/教师/院系信息
'''
@app.route('/addNew/<view>', methods=['GET', 'POST'])
def addNew(view):
    reqJson = request.get_json(silent=True)
    try:
        if view == 'S':
            xh = reqJson['xh']
            xm = reqJson['xm']
            xb = reqJson['xb']
            csrq = reqJson['csrq']
            jg = reqJson['jg']
            sjhm = reqJson['sjhm']
            yxh = reqJson['yxh']
            if csrq == '':
                csrq = 'Null'
            if jg == '':
                jg = '中国'
            if sjhm == '':
                sjhm = '13420160327'
            selsql = "SELECT xh FROM %s;" % view
            selres = select(hostaddr, usr, pwd, hostport, database, selsql, None)
            Dxh = {'a': xh}
            if Dxh in selres:
                return 'repeat'
            sqlphase = "INSERT INTO %s(xh, xm, xb, csrq, jg, sjhm, yxh) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (view, xh, xm, xb, csrq, jg, sjhm, yxh)
            sqlphase = sqlphase.replace("'Null'", "Null")
            print(sqlphase)
            resmsg = change(hostaddr, usr, pwd, hostport, database, sqlphase, None)
            return resmsg
        elif view == 'T':
            gh = reqJson['gh']
            xm = reqJson['xm']
            xb = reqJson['xb']
            csrq = reqJson['csrq']
            zc = reqJson['zc']
            yxh = reqJson['yxh']
            if csrq == '':
                csrq = 'Null'
            selsql = "SELECT gh FROM %s;" % view
            selres = select(hostaddr, usr, pwd, hostport, database, selsql, None)
            Dgh = {'a': gh}
            if Dgh in selres:
                return 'repeat'
            sqlphase = "INSERT INTO %s(gh, xm, xb, csrq, zc, yxh) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % (view, gh, xm, xb, csrq, zc, yxh)
            sqlphase = sqlphase.replace("'Null'", "Null")
            resmsg = change(hostaddr, usr, pwd, hostport, database, sqlphase, None)
            return resmsg
        elif view == 'D':
            yxh = reqJson['yxh']
            mc = reqJson['mc']
            dz = reqJson['dz']
            lxdh = reqJson['lxdh']
            selsql = "SELECT yxh FROM %s;" % view
            selres = select(hostaddr, usr, pwd, hostport, database, selsql, None)
            Dyxh = {'a': yxh}
            if Dyxh in selres:
                return 'repeat'
            sqlphase = "INSERT INTO %s(yxh, mc, dz, lxdh) VALUES ('%s', '%s', '%s', '%s');" % (view, yxh, mc, dz, lxdh)
            resmsg = change(hostaddr, usr, pwd, hostport, database, sqlphase, None)
            return resmsg
        else:
            return 'error'
    except:
        return 'error'



'''
    编辑学生/教师/院系信息
'''
@app.route('/modItem/<view>', methods=['GET', 'POST'])
def modifyItem(view):
    reqJson = request.get_json(silent=True)
    try:
        if view == 'S':
            xh = reqJson['xh']
            xm = reqJson['xm']
            xb = reqJson['xb']
            csrq = reqJson['csrq']
            jg = reqJson['jg']
            sjhm = reqJson['sjhm']
            yxh = reqJson['yxh']
            if csrq == '':
                csrq = 'Null'
            if jg == '':
                jg = '中国'
            if sjhm == '':
                sjhm = '13420160327'
            selsql = "SELECT xh FROM %s;" % view
            selres = select(hostaddr, usr, pwd, hostport, database, selsql, None)
            Dxh = {'a': xh}
            if Dxh not in selres:
                return 'repeat'
            sqlphase = "UPDATE %s SET xm='%s', xb='%s', csrq='%s', jg='%s', sjhm='%s', yxh='%s' WHERE xh='%s';" % (view, xm, xb, csrq, jg, sjhm, yxh, xh)
            sqlphase = sqlphase.replace("'Null'", "Null")
            print(sqlphase)
            resmsg = change(hostaddr, usr, pwd, hostport, database, sqlphase, None)
            return resmsg
        elif view == 'T':
            gh = reqJson['gh']
            xm = reqJson['xm']
            xb = reqJson['xb']
            csrq = reqJson['csrq']
            zc = reqJson['zc']
            yxh = reqJson['yxh']
            if csrq == '':
                csrq = 'Null'
            selsql = "SELECT gh FROM %s;" % view
            selres = select(hostaddr, usr, pwd, hostport, database, selsql, None)
            Dgh = {'a': gh}
            if Dgh not in selres:
                return 'repeat'
            sqlphase = "UPDATE %s SET xm='%s', xb='%s', csrq='%s', zc='%s', yxh='%s' WHERE gh='%s';" % (view, xm, xb, csrq, zc, yxh, gh)
            sqlphase = sqlphase.replace("'Null'", "Null")
            resmsg = change(hostaddr, usr, pwd, hostport, database, sqlphase, None)
            return resmsg
        elif view == 'D':
            yxh = reqJson['yxh']
            mc = reqJson['mc']
            dz = reqJson['dz']
            lxdh = reqJson['lxdh']
            selsql = "SELECT yxh FROM %s;" % view
            selres = select(hostaddr, usr, pwd, hostport, database, selsql, None)
            Dyxh = {'a': yxh}
            if Dyxh not in selres:
                return 'repeat'
            sqlphase = "UPDATE %s SET mc='%s', dz='%s', lxdh='%s' WHERE yxh='%s';" % (view, mc, dz, lxdh, yxh)
            resmsg = change(hostaddr, usr, pwd, hostport, database, sqlphase, None)
            return resmsg
        else:
            return 'error'
    except:
        return 'error'


'''
    删除学生/教师/院系信息
'''
@app.route('/delItem/<view>', methods=['GET', 'POST'])
def DelItem(view):
    reqJson = request.get_json(silent=True)
    if view == 'S':
        col = 'xh'
        key = reqJson['xh']
    elif view == 'T':
        col = 'gh'
        key = reqJson['gh']
    elif view == 'D':
        col = 'yxh'
        key = reqJson['yxh']
    else:
        return 'error'
    try:
        sqlphase = "DELETE FROM %s WHERE %s='%s';" % (view, col, key)
        resmsg = change(hostaddr, usr, pwd, hostport, database, sqlphase, None)
        return resmsg
    except:
        return 'error'


'''
    获取所有开课信息（含选课人数）
'''
@app.route('/courseedit', methods=['GET'])
def CourseEdit():
    view = "CourseEdit"
    sqlheadphase = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (database, view)
    sqlphase = "SELECT * FROM %s ORDER BY xq, kh, gh;" % view
    courseedit = select(hostaddr, usr, pwd, hostport, database, sqlphase, sqlheadphase)

    return json.dumps(courseedit, cls=OnlyDateEncoder)


'''
    获取所有开课信息（不含选课人数）
'''
@app.route('/courseall', methods=['GET', 'POST'])
def CourseAll():
    view = "CourseAll"
    sqlheadphase = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (database, view)
    sqlphase = "SELECT * FROM %s ORDER BY kh;" % view
    courseall = select(hostaddr, usr, pwd, hostport, database, sqlphase, sqlheadphase)

    return json.dumps(courseall, cls=OnlyDateEncoder)


'''
    新增课程信息
'''
@app.route('/courseall/new', methods=['GET', 'POST'])
def CourseAllNew():
    view = "C"
    reqJson = request.get_json(silent=True)
    kh = reqJson['khNew']
    km = reqJson['kmNew']
    yxh = reqJson['yxhNew']
    xf = reqJson['xfNew']
    xs = reqJson['xsNew']

    selectsql = "SELECT kh FROM %s" % view
    allcourse = select(hostaddr, usr, pwd, hostport, database, selectsql, None)
    print(allcourse)
    jsonnew = {
        'a': kh
    }
    if jsonnew in allcourse:
        return 'repeat'
    sqlphase = "INSERT INTO %s(kh, km, yxh, xf, xs) VALUES('%s', '%s', '%s', %u, %u);" % (view, kh, km, yxh, xf, xs)
    try:
        ret = change(hostaddr, usr, pwd, hostport, database, sqlphase, None)
    except:
        return 'error'
    return ret


'''
    删除课程信息
'''
@app.route('/courseall/del', methods=['GET', 'POST'])
def CourseAllDel():
    view = "C"
    reqJson = request.get_json(silent=True)
    kh = reqJson['kh']
    selectsql = "SELECT kh FROM %s" % view
    allcourse = select(hostaddr, usr, pwd, hostport, database, selectsql, None)
    print(allcourse)
    jsonnew = {
        'a': kh
    }
    if jsonnew not in allcourse:
        return 'repeat'
    sqlphase = "DELETE FROM %s WHERE kh='%s';" % (view, kh)
    try:
        ret = change(hostaddr, usr, pwd, hostport, database, sqlphase, None)
    except:
        return 'error'
    return ret


'''
    获取所有开课信息（不含选课人数）
'''
@app.route('/courseopen', methods=['GET'])
def CourseOpen():
    view = "CourseOpen"
    sqlheadphase = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (database, view)
    sqlphase = "SELECT * FROM %s ORDER BY xq, kh, gh;" % view
    courseopen = select(hostaddr, usr, pwd, hostport, database, sqlphase, sqlheadphase)

    return json.dumps(courseopen, cls=OnlyDateEncoder)


'''
    获取指定学期开课信息
'''
@app.route('/courseopen/<xq>', methods=['GET'])
def CourseOpenTerm(xq):
    view = "CourseOpen"
    sqlheadphase = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (database, view)
    sqlphase = "SELECT * FROM %s WHERE xq='%s' ORDER BY kh, gh;" % (view, xq)
    courseopenterm = select(hostaddr, usr, pwd, hostport, database, sqlphase, sqlheadphase)

    return json.dumps(courseopenterm, cls=OnlyDateEncoder)


'''
    新增开课信息
'''
@app.route('/courseopenNew', methods=['GET', 'POST'])
def CourseOpenNew():
    view = "O"
    reqJson = request.get_json(silent=True)
    xqNew = reqJson['xqNew']
    khNew = reqJson['khNew']
    ghNew = reqJson['ghNew']
    sksjNew = reqJson['sksjNew']

    try:
        sqlphase = "INSERT INTO O(xq, kh, gh, sksj) VALUES ('%s', '%s', '%s', '%s');" % (xqNew, khNew, ghNew, sksjNew)
        resmsg = change(hostaddr, usr, pwd, hostport, database, sqlphase, None)
        return resmsg
    except:
        return 'error'


'''
    删除开课信息
'''
@app.route('/courseopenDel', methods=['GET', 'POST'])
def CourseOpenDel():
    view = "O"
    reqJson = request.get_json(silent=True)
    xqDel = reqJson['xq']
    khDel = reqJson['kh']
    ghDel = reqJson['gh']
    courseDel = {
        'a': xqDel,
        'b': khDel,
        'c': ghDel,
    }

    try:
        # selectsqlhead = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='E';" % database
        selectsql = "SELECT DISTINCT xq, kh, gh FROM E;"
        hasstudents = select(hostaddr, usr, pwd, hostport, database, selectsql, None)
        # print(hasstudents)
        if courseDel in hasstudents:
            return 'deletestudentfirst'
        else:
            sqlphase = "DELETE FROM %s WHERE xq='%s' AND kh='%s' AND gh='%s';" % (view, xqDel, khDel, ghDel)
            resmsg = change(hostaddr, usr, pwd, hostport, database, sqlphase, None)
            return resmsg
    except:
        return 'error'


'''
    强制删除开课信息
'''
@app.route('/courseopenDel/force', methods=['GET', 'POST'])
def CourseOpenDelForce():
    view = "O"
    reqJson = request.get_json(silent=True)
    xqDel = reqJson['xq']
    khDel = reqJson['kh']
    ghDel = reqJson['gh']

    try:
        Esqlphase = "DELETE FROM E WHERE xq='%s' AND kh='%s' AND gh='%s';" % (xqDel, khDel, ghDel)
        Eresmsg = change(hostaddr, usr, pwd, hostport, database, Esqlphase, None)
        if Eresmsg == 'success':
            sqlphase = "DELETE FROM %s WHERE xq='%s' AND kh='%s' AND gh='%s';" % (view, xqDel, khDel, ghDel)
            resmsg = change(hostaddr, usr, pwd, hostport, database, sqlphase, None)
            return resmsg
        else:
            return Eresmsg
    except:
        return 'error'


'''
    获取指定课程开课信息
'''
@app.route('/courseopen/<xq>/<kh>/<gh>', methods=['GET', 'POST'])
def CourseOpenInfo(xq, kh, gh):
    view = "CourseOpen"
    sqlheadphase = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (database, view)
    sqlphase = "SELECT * FROM %s WHERE xq='%s' AND kh='%s' AND gh='%s';" % (view, xq, kh, gh)
    courseopeninfo = select(hostaddr, usr, pwd, hostport, database, sqlphase, sqlheadphase)

    return json.dumps(courseopeninfo, cls=OnlyDateEncoder)


'''
    获取指定课程选课信息（不含成绩）
'''
@app.route('/coursedetail/<xq>/<kh>/<gh>', methods=['GET', 'POST'])
def CourseDetail(xq, kh, gh):
    view = "FullE"
    sqlheadphase = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (database, view)
    sqlphase = "SELECT * FROM %s WHERE xq='%s' AND kh='%s' AND gh='%s';" % (view, xq, kh, gh)
    coursedetail = select(hostaddr, usr, pwd, hostport, database, sqlphase, sqlheadphase)

    return json.dumps(coursedetail, cls=DecimalEncoder)


'''
    获取指定学生学期选课信息
'''
@app.route('/coursedetail/<xq>/<xh>', methods=['GET', 'POST'])
def CourseDetailStuTerm(xq, xh, type=True):
    view = "FullE"
    # sqlheadphase = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (database, view)
    sqlphase = "SELECT kh, km, gh, txm, sksj, yxh, mc, xf, (CASE WHEN pscj IS NULL AND kscj IS NULL THEN 'candelete' ELSE 'cannotdelete' END) zt FROM %s WHERE xq='%s' AND xh='%s' ORDER BY kh, gh;" % (view, xq, xh)
    coursedetailstuterm = select(hostaddr, usr, pwd, hostport, database, sqlphase, None)
    for eachcourse in coursedetailstuterm:
        eachcourse['kh'] = eachcourse.pop('a')
        eachcourse['km'] = eachcourse.pop('b')
        eachcourse['gh'] = eachcourse.pop('c')
        eachcourse['txm'] = eachcourse.pop('d')
        eachcourse['sksj'] = eachcourse.pop('e')
        eachcourse['yxh'] = eachcourse.pop('f')
        eachcourse['mc'] = eachcourse.pop('g')
        eachcourse['xf'] = eachcourse.pop('h')
        eachcourse['zt'] = eachcourse.pop('i')
    if type:
        return json.dumps(coursedetailstuterm, cls=DecimalEncoder)
    else:
        return coursedetailstuterm


'''
    获取指定课程选课信息（含成绩）
'''
@app.route('/gradedetail/<xq>/<kh>/<gh>', methods=['GET', 'POST'])
def GradeDetail(xq, kh, gh):
    view = "FullE"
    sqlheadphase = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (database, view)
    sqlphase = "SELECT * FROM %s WHERE xq='%s' AND kh='%s' AND gh='%s';" % (view, xq, kh, gh)
    gradedetail = select(hostaddr, usr, pwd, hostport, database, sqlphase, sqlheadphase)

    return json.dumps(gradedetail, cls=DecimalEncoder)


'''
    指定学生选课
'''
@app.route('/newelection', methods=['GET', 'POST'])
def NewElection():
    view = "E"
    reqJson = request.get_json(silent=True)
    xhNewE = reqJson['xh']
    xqNewE = reqJson['xq']
    khNewE = reqJson['kh']
    ghNewE = reqJson['gh']
    newE = {
        'xh': xhNewE,
        'xq': xqNewE,
        'kh': khNewE,
        'gh': ghNewE
    }

    try:
        selectsqlhead = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (database, view)
        selectsql = "SELECT xh, xq, kh, gh FROM %s;" % view
        already = select(hostaddr, usr, pwd, hostport, database, selectsql, selectsqlhead)
        if newE in already:
            return 'repeat'
        else:
            sqlphase = "INSERT INTO E(xh, xq, kh, gh) VALUES ('%s', '%s', '%s', '%s')" % (xhNewE, xqNewE, khNewE, ghNewE)
            resmsg = change(hostaddr, usr, pwd, hostport, database, sqlphase, None)
            return resmsg
    except:
        return 'error'


'''
    指定学生退课
'''
@app.route('/delelection', methods=['GET', 'POST'])
def DelElection():
    view = "E"
    reqJson = request.get_json(silent=True)
    xhDelE = reqJson['xh']
    xqDelE = reqJson['xq']
    khDelE = reqJson['kh']
    ghDelE = reqJson['gh']
    delE = {
        'xh': xhDelE,
        'xq': xqDelE,
        'kh': khDelE,
        'gh': ghDelE
    }

    try:
        selectsqlhead = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (database, view)
        selectsql = "SELECT xh, xq, kh, gh FROM %s;" % view
        already = select(hostaddr, usr, pwd, hostport, database, selectsql, selectsqlhead)
        if delE not in already:
            return 'repeat'
        else:
            sqlphase = "DELETE FROM E WHERE xh='%s' AND xq='%s' AND kh='%s' AND gh='%s';" % (xhDelE, xqDelE, khDelE, ghDelE)
            resmsg = change(hostaddr, usr, pwd, hostport, database, sqlphase, None)
            return resmsg
    except:
        return 'error'


'''
    更新指定课程选课信息（含成绩）
'''
@app.route('/gradeUpdate', methods=['GET', 'POST'])
def GradeUpdate():
    view = "E"
    reqJson = request.get_json(silent=True)
    tableData = reqJson['grade']
    percent = reqJson['percent'] / 100
    for row in tableData:
        print(row)
        xh = row['xh']
        xq = row['xq']
        kh = row['kh']
        gh = row['gh']
        pscj = row['pscj']
        kscj = row['kscj']
        if kscj == None or kscj == '':
            kscj == None
            if pscj == None or pscj == '':
                pscj == None
            else:
                pscj = int(row['pscj'])
            zpcj = None
        else:
            kscj = int(row['kscj'])
            if pscj == None or pscj == '':
                pscj == None
                zpcj = kscj
            else:
                pscj = int(row['pscj'])
                zpcj = pscj * percent + kscj * (1 - percent)
        jdsql = "(CASE WHEN zpcj IS NULL THEN NULL " \
                "WHEN zpcj<60 THEN 0.0 " \
                "WHEN zpcj<64 THEN 1.0 " \
                "WHEN zpcj<66 THEN 1.5 " \
                "WHEN zpcj<68 THEN 1.7 " \
                "WHEN zpcj<72 THEN 2.0 " \
                "WHEN zpcj<75 THEN 2.3 " \
                "WHEN zpcj<78 THEN 2.7 " \
                "WHEN zpcj<82 THEN 3.0 " \
                "WHEN zpcj<85 THEN 3.3 " \
                "WHEN zpcj<90 THEN 3.7 " \
                "ELSE 4.0 " \
                "END)"
        sqlphase = "UPDATE %s SET pscj=%s, kscj=%s, zpcj=%s, jd=%s WHERE xh='%s' AND xq='%s' AND kh='%s' AND gh='%s';" % (view, str(pscj), str(kscj), str(zpcj), jdsql, xh, xq, kh, gh)
        sqlphase = sqlphase.replace('None', 'Null')
        sqlphase = sqlphase.replace('=,', '=Null,')
        # print(sqlphase)
        try:
            resmsg = change(hostaddr, usr, pwd, hostport, database, sqlphase, None)
        except:
            return 'error'
    return resmsg


'''
    获取指定学生学期选课信息（含成绩）
'''
@app.route('/gradeAll/<xh>', methods=['GET', 'POST'])
def GradeAll(xh):
    view = "FullE"
    sqlheadphase = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (database, view)
    sqlphase = "SELECT * FROM %s WHERE xh='%s' ORDER BY xq, kh, gh;" % (view, xh)
    try:
        gradeall = select(hostaddr, usr, pwd, hostport, database, sqlphase, sqlheadphase)
        return json.dumps(gradeall, cls=DecimalEncoder)
    except:
        return 'error'


'''
    获取指定学生所有成绩统计信息
'''
@app.route('/gradeAll/GPA/<xh>', methods=['GET', 'POST'])
def GradeAllGPA(xh):
    view = "FullE"
    # sqlheadphase = "SELECT * FROM information_schema.columns WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';" % (database, view)
    # sqlphase = "SELECT xq, SUM(xf) zxf, ROUND(AVG(zpcj), 2) pjcj, Round(SUM(xf*jd)/SUM(xf), 3) pjjd FROM %s WHERE xh='%s' AND zpcj IS NOT NULL AND jd IS NOT NULL GROUP BY xq ORDER BY xq;" % (view, xh)
    sqlphase = "SELECT DISTINCT O.xq, zxf, pjcj, pjjd FROM O LEFT JOIN (SELECT xq, SUM(xf) zxf, ROUND(AVG(zpcj), 2) pjcj, Round(SUM(xf*jd)/SUM(xf), 3) pjjd FROM %s WHERE xh='%s' AND zpcj IS NOT NULL AND jd IS NOT NULL GROUP BY xq) GPA ON O.xq = GPA.xq ORDER BY xq;" % (view, xh)
    try:
        allGPA = select(hostaddr, usr, pwd, hostport, database, sqlphase, None)
        for xqGPA in allGPA:
            xqGPA['xq'] = xqGPA.pop('a')
            xqGPA['zxf'] = xqGPA.pop('b')
            xqGPA['pjcj'] = xqGPA.pop('c')
            xqGPA['pjjd'] = xqGPA.pop('d')
        return json.dumps(allGPA, cls=DecimalEncoder)
    except:
        return 'error'


color = colors()
scheduleTemplate = [{
                    'cls': '1',
                    'Mon': { 'kh': '', 'km': '', 'js': 0 },
                    'Tue': { 'kh': '', 'km': '', 'js': 0 },
                    'Wed': { 'kh': '', 'km': '', 'js': 0 },
                    'Thu': { 'kh': '', 'km': '', 'js': 0 },
                    'Fri': { 'kh': '', 'km': '', 'js': 0 },
                }, {
                    'cls': '2',
                    'Mon': { 'kh': '', 'km': '', 'js': 0 },
                    'Tue': { 'kh': '', 'km': '', 'js': 0 },
                    'Wed': { 'kh': '', 'km': '', 'js': 0 },
                    'Thu': { 'kh': '', 'km': '', 'js': 0 },
                    'Fri': { 'kh': '', 'km': '', 'js': 0 },
                }, {
                    'cls': '3',
                    'Mon': { 'kh': '', 'km': '', 'js': 0 },
                    'Tue': { 'kh': '', 'km': '', 'js': 0 },
                    'Wed': { 'kh': '', 'km': '', 'js': 0 },
                    'Thu': { 'kh': '', 'km': '', 'js': 0 },
                    'Fri': { 'kh': '', 'km': '', 'js': 0 },
                }, {
                    'cls': '4',
                    'Mon': { 'kh': '', 'km': '', 'js': 0 },
                    'Tue': { 'kh': '', 'km': '', 'js': 0 },
                    'Wed': { 'kh': '', 'km': '', 'js': 0 },
                    'Thu': { 'kh': '', 'km': '', 'js': 0 },
                    'Fri': { 'kh': '', 'km': '', 'js': 0 },
                }, {
                    'cls': '5',
                    'Mon': { 'kh': '', 'km': '', 'js': 0 },
                    'Tue': { 'kh': '', 'km': '', 'js': 0 },
                    'Wed': { 'kh': '', 'km': '', 'js': 0 },
                    'Thu': { 'kh': '', 'km': '', 'js': 0 },
                    'Fri': { 'kh': '', 'km': '', 'js': 0 },
                }, {
                    'cls': '6',
                    'Mon': { 'kh': '', 'km': '', 'js': 0 },
                    'Tue': { 'kh': '', 'km': '', 'js': 0 },
                    'Wed': { 'kh': '', 'km': '', 'js': 0 },
                    'Thu': { 'kh': '', 'km': '', 'js': 0 },
                    'Fri': { 'kh': '', 'km': '', 'js': 0 },
                }, {
                    'cls': '7',
                    'Mon': { 'kh': '', 'km': '', 'js': 0 },
                    'Tue': { 'kh': '', 'km': '', 'js': 0 },
                    'Wed': { 'kh': '', 'km': '', 'js': 0 },
                    'Thu': { 'kh': '', 'km': '', 'js': 0 },
                    'Fri': { 'kh': '', 'km': '', 'js': 0 },
                }, {
                    'cls': '8',
                    'Mon': { 'kh': '', 'km': '', 'js': 0 },
                    'Tue': { 'kh': '', 'km': '', 'js': 0 },
                    'Wed': { 'kh': '', 'km': '', 'js': 0 },
                    'Thu': { 'kh': '', 'km': '', 'js': 0 },
                    'Fri': { 'kh': '', 'km': '', 'js': 0 },
                }, {
                    'cls': '9',
                    'Mon': { 'kh': '', 'km': '', 'js': 0 },
                    'Tue': { 'kh': '', 'km': '', 'js': 0 },
                    'Wed': { 'kh': '', 'km': '', 'js': 0 },
                    'Thu': { 'kh': '', 'km': '', 'js': 0 },
                    'Fri': { 'kh': '', 'km': '', 'js': 0 },
                }, {
                    'cls': '10',
                    'Mon': { 'kh': '', 'km': '', 'js': 0 },
                    'Tue': { 'kh': '', 'km': '', 'js': 0 },
                    'Wed': { 'kh': '', 'km': '', 'js': 0 },
                    'Thu': { 'kh': '', 'km': '', 'js': 0 },
                    'Fri': { 'kh': '', 'km': '', 'js': 0 },
                },{
                    'cls': '11',
                    'Mon': { 'kh': '', 'km': '', 'js': 0 },
                    'Tue': { 'kh': '', 'km': '', 'js': 0 },
                    'Wed': { 'kh': '', 'km': '', 'js': 0 },
                    'Thu': { 'kh': '', 'km': '', 'js': 0 },
                    'Fri': { 'kh': '', 'km': '', 'js': 0 },
                }, {
                    'cls': '12',
                    'Mon': { 'kh': '', 'km': '', 'js': 0 },
                    'Tue': { 'kh': '', 'km': '', 'js': 0 },
                    'Wed': { 'kh': '', 'km': '', 'js': 0 },
                    'Thu': { 'kh': '', 'km': '', 'js': 0 },
                    'Fri': { 'kh': '', 'km': '', 'js': 0 },
                }, {
                    'cls': '13',
                    'Mon': { 'kh': '', 'km': '', 'js': 0 },
                    'Tue': { 'kh': '', 'km': '', 'js': 0 },
                    'Wed': { 'kh': '', 'km': '', 'js': 0 },
                    'Thu': { 'kh': '', 'km': '', 'js': 0 },
                    'Fri': { 'kh': '', 'km': '', 'js': 0 },
                }]


def WeekDayChange(Chinese):
    if Chinese == '一':
        return 'Mon'
    elif Chinese == '二':
        return  'Tue'
    elif Chinese == '三':
        return  'Wed'
    elif Chinese == '四':
        return  'Thu'
    elif Chinese == '五':
        return  'Fri'
    else:
        return 'error'


'''
    获取指定学期学生课表
'''
@app.route('/schedule/<xq>/<xh>', methods=['GET', 'POST'])
def schedule(xq, xh):
    coursedetail = CourseDetailStuTerm(xq, xh, False)
    # print(coursedetail)
    scheduleData = copy.deepcopy(scheduleTemplate)
    for record in coursedetail:
        sksjList = record['sksj'].split(' ')
        kh = record['kh']
        km = record['km']
        # print(sksjList)
        for sksj in sksjList:
            # print(sksj)
            day = sksj[0]
            day = WeekDayChange(day)
            jcList = sksj[1:].split('-')
            # print(day, jcList)
            jcStart = jcList[0]
            js = int(jcList[1]) - int(jcList[0]) + 1
            print(kh, km, day, jcStart, js)
            index = int(jcStart) - 1
            # print(scheduleData[index])
            scheduleData[index][day]['kh'] = kh
            scheduleData[index][day]['km'] = km
            scheduleData[index][day]['js'] = js
            # print(scheduleData[index])
    return json.dumps(scheduleData, cls=DecimalEncoder)


@app.route('/schedule/realtime', methods=['GET', 'POST'])
def scheduleRealtime():
    reqJson = request.get_json(silent=True)
    coursedetail = reqJson
    # print(coursedetail)
    scheduleData = copy.deepcopy(scheduleTemplate)
    for record in coursedetail:
        sksjList = record['sksj'].split(' ')
        kh = record['kh']
        km = record['km']
        # print(sksjList)
        for sksj in sksjList:
            # print(sksj)
            day = sksj[0]
            day = WeekDayChange(day)
            jcList = sksj[1:].split('-')
            # print(day, jcList)
            jcStart = jcList[0]
            js = int(jcList[1]) - int(jcList[0]) + 1
            print(kh, km, day, jcStart, js)
            index = int(jcStart) - 1
            # print(scheduleData[index])
            scheduleData[index][day]['kh'] = kh
            scheduleData[index][day]['km'] = km
            scheduleData[index][day]['js'] = js
            # print(scheduleData[index])
    return json.dumps(scheduleData, cls=DecimalEncoder)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
