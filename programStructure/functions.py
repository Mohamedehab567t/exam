import os
import random
import secrets

from flask_login import current_user

from programStructure import app, Setting_ID
from flask import render_template

from .models import Student, WS, QDB, ActiveExamsDB, SiDB
from wtforms.validators import ValidationError


def Validate_account(self, email):
    user = Student.find_one({'phone_number': email.data})
    if not user:
        raise ValidationError('No user with these Number')


def Validate_account_Arabic(self, email):
    user = Student.find_one({'phone_number': email.data})
    if not user:
        raise ValidationError('لا يجود مستخدم بهذا الرقم')


def Validate_password(self, password):
    user = Student.find_one({'phone_number': self.email.data})
    if not user:
        raise ValidationError('No user with these phone or you waiting an approval')
    else:
        if user['password'] != password.data:
            raise ValidationError('Wrong Password')


def Validate_password_Arabic(self, password):
    user = Student.find_one({'phone_number': self.email.data})
    if not user:
        raise ValidationError('لا يوجد حساب بهذا الرقم')
    else:
        if user['password'] != password.data:
            raise ValidationError('كلمة مرور خاطئة')


def Validate_if_waiting(self, email):
    user = WS.find_one({'phone_number': email.data})
    if user:
        raise ValidationError('This phone is used and waiting For Approval')


def Validate_if_waiting_Arabic(self, email):
    user = WS.find_one({'phone_number': email.data})
    if user:
        raise ValidationError('هذا الرقم مستخدم ومنتظر القبول')


def SendWaitingRequest(form):
    id = random.randint(1000000000000, 9999999999999)
    firstletter = list(form.first_name.data)[0]
    student = {'_id': id,
               'firstletter': firstletter,
               'first_name': form.first_name.data,
               'last_name': form.last_name.data,
               'phone_number': form.email.data,
               'gender': form.gender.data,
               'password': form.password.data,
               'type': 'student',
               'Messages': [],
               'Rank': {
                   'FullMark': 1,
                   'score': 0,
                   'rank': "0.0"
               }
               }
    WS.insert_one(student)


def AddStudent(id):
    user = WS.find_one({'_id': id})
    Student.insert_one(user)
    WS.delete_one({'_id': id})


def DeleteWaitingStudent(id):
    WS.delete_one({'_id': id})


def ReturnNewStudentNumber():
    WS_NUM = len(list(WS.find()))
    S_NUM = len(list(Student.find({'type': 'student'})))
    waiting = list(WS.find())
    students = list(Student.find({'type': 'student'}))
    temp1 = render_template('WaitingStudentPart.html', waiting=waiting, WS_NUM=WS_NUM)
    temp2 = render_template('StudentsPart.html', students=students, S_NUM=S_NUM)

    AdminHead = render_template('AdminHead.html')
    data = {
        'temp': temp1,
        'temp2': temp2,
        'AdminHead': AdminHead,
        'num1': "الطلاب المنتظرين [ " + str(WS_NUM) + " ]",
        'num2': "طلابي [ " + str(S_NUM) + "]"
    }
    return data


def ReturnNewStudentNumberVersionOfSearch(List, temp):
    students = List
    S_NUM = len(students)
    temp2 = render_template(temp + '.html', students=students, S_NUM=S_NUM)
    AdminHead = render_template('AdminHead.html')
    data = {
        'temp2': temp2,
        'AdminHead': AdminHead,
        'Nav': "طلابي [ " + str(S_NUM) + "]",
        'num2': str(S_NUM)
    }
    return data


def ReturnStudentOfSearchInRankedAdmin(val, DB, temp):
    AndExpressionForS = []
    for obj in val:
        expression = {'Addition.' + str(obj): val[obj]}
        AndExpressionForS.append(expression)
    global Ranked
    try:
        Ranked = Student.find({'type': 'student', '$and': AndExpressionForS}).sort(
            [("Rank.rank", -1), ("Rank.FullMark", -1)])
    except KeyError:
        pass
    temp2 = render_template(temp + '.html', Ranked=Ranked)
    data = {
        'temp2': temp2
    }
    return data


def ReturnExamsStatus():
    Exams = ActiveExamsDB.find()
    temp1 = render_template('ActiveExams.html', Exams=Exams)
    temp2 = render_template('PublishedExam.html', Exams=Exams)
    temp3 = render_template('SubmittedExam.html', Exams=Exams)

    data = {
        'temp': temp1,
        'temp2': temp2,
        'temp3': temp3
    }
    return data


def DeleteStudent(id):
    Student.delete_one({'_id': id})


def savepic(form_pic, id):
    rhex = form_pic.filename + str(id)
    _, fext = os.path.splitext(form_pic.filename)
    pic_name = rhex + fext
    pic_path = os.path.join(app.root_path, 'static/images', pic_name)
    form_pic.save(pic_path)
    return pic_name


def GenerateAccessCode(n):
    token = secrets.token_hex(n)
    token1 = secrets.token_hex(n)
    token2 = secrets.token_hex(n)
    token3 = secrets.token_hex(n)
    Access_Code = token + '-' + token2 + '-' + token1 + '-' + token3
    return Access_Code


def CreateAutoExamObject(INFO):
    Exam = {}
    E_Q = []
    Absent = []
    AndExpressionForQuestion = []
    AndExpressionForStudent = []
    ExamObject = {}
    QuestionObject = {}
    StudentsObject = {}
    FullMark = 0
    id = random.randint(10000000, 99999999)
    Exam['_id'] = id
    QuestionsObject = list(INFO['Question_Part'])
    StudentObject = list(INFO['Student_Part'])

    for obj in QuestionsObject:
        if isinstance(INFO['Question_Part'][obj], list):
            expression = {obj: {
                '$in': INFO['Question_Part'][obj]
            }}
            AndExpressionForQuestion.append(expression)
            QuestionObject[obj] = INFO['Question_Part'][obj]
        else:
            expression = {
                obj: INFO['Question_Part'][obj]
            }
            QuestionObject[obj] = INFO['Question_Part'][obj]
            AndExpressionForQuestion.append(expression)

    Multiple_Content = list(QDB.find({
        '$and': AndExpressionForQuestion
    }))

    num = len(Multiple_Content)
    if num > int(INFO['NoQ']):
        for x in range(0, num):
            r = random.randint(0, len(Multiple_Content) - 1)
            if Multiple_Content[r] in E_Q:
                num = num + 1
            else:
                E_Q.append(Multiple_Content[r])
                if len(E_Q) == int(INFO['NoQ']):
                    break
    else:
        INFO['NoQ'] = num
        E_Q = Multiple_Content

    for Question in E_Q:
        Score = list(Question['score'])
        for score in Score:
            FullMark += int(score)

    for obj in StudentObject:
        if isinstance(INFO['Student_Part'][obj], list):
            expression = {"Addition." + obj: {
                '$in': INFO['Student_Part'][obj]
            }}
            StudentsObject[obj] = INFO['Student_Part'][obj]
            AndExpressionForStudent.append(expression)
        else:
            expression = {
                "Addition." + obj: INFO['Student_Part'][obj]
            }
            StudentsObject[obj] = INFO['Student_Part'][obj]
            AndExpressionForStudent.append(expression)

    Absent = list(Student.find({
        '$and': AndExpressionForStudent
    }))

    QuestionObject['QNO'] = INFO['NoQ']
    ExamObject['Duration'] = INFO['duration']
    ExamObject['From'] = INFO['from']
    ExamObject['To'] = INFO['to']
    ExamObject['title'] = INFO['title']
    ExamObject['Status'] = 'Active'
    ExamObject['FullMark'] = FullMark
    ExamObject['AccessCode'] = GenerateAccessCode(2)
    StudentsObject['Absent'] = Absent
    StudentsObject['Attended'] = []

    Exam['ExamInformation'] = ExamObject
    Exam['QuestionInformation'] = QuestionObject
    Exam['StudentsInformation'] = StudentsObject
    Exam['r'] = 'false'
    Exam['showAnswers'] = 'show'
    Exam['Questions'] = E_Q

    ActiveExamsDB.insert_one(Exam)


def CreateManualExamObject(INFO):
    Exam = {}
    E_Q = []
    Absent = []
    AndExpressionForQuestion = []
    AndExpressionForStudent = []
    ExamObject = {}
    QuestionObject = {}
    StudentsObject = {}
    FullMark = 0
    id = random.randint(10000000, 99999999)
    Exam['_id'] = id
    QuestionsObject = list(INFO['Question_Part'])
    StudentObject = list(INFO['Student_Part'])

    for obj in QuestionsObject:
        if isinstance(INFO['Question_Part'][obj], list):
            expression = {obj: {
                '$in': INFO['Question_Part'][obj]
            }}
            AndExpressionForQuestion.append(expression)
            QuestionObject[obj] = INFO['Question_Part'][obj]
        else:
            expression = {
                obj: INFO['Question_Part'][obj]
            }
            QuestionObject[obj] = INFO['Question_Part'][obj]
            AndExpressionForQuestion.append(expression)

    Multiple_Content = list(QDB.find({
        '$and': AndExpressionForQuestion
    }))

    for obj in StudentObject:
        if isinstance(INFO['Student_Part'][obj], list):
            expression = {"Addition." + obj: {
                '$in': INFO['Student_Part'][obj]
            }}
            StudentsObject[obj] = INFO['Student_Part'][obj]
            AndExpressionForStudent.append(expression)
        else:
            expression = {
                "Addition." + obj: INFO['Student_Part'][obj]
            }
            StudentsObject[obj] = INFO['Student_Part'][obj]
            AndExpressionForStudent.append(expression)

    Absent = list(Student.find({
        '$and': AndExpressionForStudent
    }))

    ExamObject['Duration'] = INFO['duration']
    ExamObject['From'] = INFO['from']
    ExamObject['To'] = INFO['to']
    ExamObject['title'] = INFO['title']
    ExamObject['Status'] = 'Without'
    ExamObject['FullMark'] = FullMark
    ExamObject['AccessCode'] = GenerateAccessCode(2)
    StudentsObject['Absent'] = Absent
    StudentsObject['Attended'] = []

    Exam['ExamInformation'] = ExamObject
    Exam['QuestionInformation'] = QuestionObject
    Exam['StudentsInformation'] = StudentsObject
    Exam['r'] = 'false'
    Exam['showAnswers'] = 'show'
    ActiveExamsDB.insert_one(Exam)
    data = {
        'list': Multiple_Content,
        'id': id
    }
    return data


def DoRank(user, exam, Submit):
    try:
        if user['Rank']:
            FullMark = exam['ExamInformation']['FullMark'] + user['Rank']['FullMark']
            Score = Submit['score'] + user['Rank']['score']
            Student.update_one({'_id': Submit['_id']}, {
                '$set': {
                    'Rank.FullMark': FullMark,
                    'Rank.score': Score,
                    'Rank.rank': "%.1f" % (((Score / FullMark) * 100) / 10)

                }
            })
    except KeyError:
        FullMark = exam['ExamInformation']['FullMark']
        Score = Submit['score']
        Rank = {
            'FullMark': FullMark,
            'score': Score,
            'rank': "%.1f" % (((Score / FullMark) * 100) / 10)
        }
        Student.update_one({'_id': Submit['_id']}, {
            '$set': {
                'Rank': Rank
            }
        })


def GetExamDetailsFromMessagesId(user):
    ExamsMessages = []
    if 'Messages' in user:
        for id in user['Messages']:
            exam = ActiveExamsDB.find_one({'_id': id['_id']})
            ExamsMessages.append(exam)
        return ExamsMessages
    else:
        return []


def find_index(lst, value):
    for i in range(0, len(lst)):
        if lst[i] == value:
            return i
    return -1


def GetKeysFromQ_Configuration():
    Si = SiDB.find_one({'_id': Setting_ID})
    QC = Si['Q-Configuration']
    return QC


def GetFilteredListOnSearchQ(val, DB):
    AndExpressionForQuestion = []
    for obj in val:
        expression = {obj: val[obj]}
        AndExpressionForQuestion.append(expression)
    List = list(DB.find({
        '$and': AndExpressionForQuestion
    }))
    return List


def GetFilteredListOnSearchS(val, DB):
    AndExpressionForQuestion = []
    for obj in val:
        expression = {'Addition.' + str(obj): val[obj]}
        AndExpressionForQuestion.append(expression)
    List = list(DB.find({
        '$and': AndExpressionForQuestion
    }))
    return List


def GetFilteredListOnDeleteQ(val):
    QuestionsToGet = []
    QDB.delete_one({'_id': val['id']})
    if 'AndExpression' in val:
        AndExpressionForQuestion = []
        for obj in val['AndExpression']:
            expression = {obj: val['AndExpression'][obj]}
            AndExpressionForQuestion.append(expression)

        QuestionsToGet = list(QDB.find({
            '$and': AndExpressionForQuestion
        }))
    else:
        QuestionsToGet = list(QDB.find())
    return QuestionsToGet


def GetFilteredListOnDeleteS(val):
    DS = []
    if 'AndExpression' in val:
        AndExpressionForQuestion = []
        for obj in val['AndExpression']:
            expression = {obj: val['AndExpression'][obj]}
            AndExpressionForQuestion.append(expression)

        DS = list(Student.find({'type': 'student'}, {
            '$and': AndExpressionForQuestion
        }))
    else:
        DS = list(Student.find({'type': 'student'}))
    return DS


def ReturnSToAddInActiveExam(exam):
    StudentConfiguration = SiDB.find_one({'_id': Setting_ID})['Addition-Information']
    Configs = []
    AndExpression = []
    for OBJ in StudentConfiguration:
        if OBJ['InfoValue'] == 'Exam':
            Configs.append(OBJ['label'])
    for val in Configs:
        for value in exam['StudentsInformation'][val]:
            expression = {
                'Addition.' + val: value
            }
            AndExpression.append(expression)

    lst = list(Student.find({'$and': AndExpression}))
    return lst


def GetAbsentFromPublished(exam_id):
    exam = ActiveExamsDB.find_one({'_id': exam_id})
    S = []
    for user in exam['StudentsInformation']['Absent']:
        S.append(user['_id'])
    for user in exam['StudentsInformation']['Attended']:
        S.append(user['_id'])
    StudentConfiguration = SiDB.find_one({'_id': Setting_ID})['Addition-Information']
    Configs = []
    AndExpression = []
    for OBJ in StudentConfiguration:
        if OBJ['InfoValue'] == 'Exam':
            Configs.append(OBJ['label'])
    for val in Configs:
        for value in exam['StudentsInformation'][val]:
            expression = {
                'Addition.' + val: value
            }
            AndExpression.append(expression)

    lst = list(Student.find({'$and': AndExpression}))
    lst2 = []
    for usr in lst:
        if usr['_id'] not in S:
            lst2.append(usr)
    return lst2