import os
import random
import secrets
from programStructure import app
from flask import render_template

from .models import Student, WS, QDB, ActiveExamsDB
from wtforms.validators import ValidationError


def Validate_account(self, email):
    user = Student.find_one({'email': email.data})
    if not user:
        raise ValidationError('No user with these email')


def Validate_account_Arabic(self, email):
    user = Student.find_one({'email': email.data})
    if not user:
        raise ValidationError('لا يجود مستخدم بهذا البريد')


def Validate_password(self, password):
    user = Student.find_one({'email': self.email.data})
    if not user:
        raise ValidationError('No user with these email or you waiting an approval')
    else:
        if user['password'] != password.data:
            raise ValidationError('Wrong Password')


def Validate_password_Arabic(self, password):
    user = Student.find_one({'email': self.email.data})
    if not user:
        raise ValidationError('لا يوجد حساب بهذا البريد')
    else:
        if user['password'] != password.data:
            raise ValidationError('كلمة مرور خاطئة')


def Validate_if_waiting(self, email):
    user = WS.find_one({'email': email.data})
    if user:
        raise ValidationError('This email is used and waiting For Approval')


def Validate_if_waiting_Arabic(self, email):
    user = WS.find_one({'email': email.data})
    if user:
        raise ValidationError('هذا الاميل مستخدم ومنتظر القبول')


def SendWaitingRequest(form):
    id = random.randint(1000000000000, 9999999999999)
    firstletter = list(form.first_name.data)[0]
    student = {'_id': id,
               'firstletter': firstletter,
               'first_name': form.first_name.data,
               'last_name': form.last_name.data,
               'email': form.email.data,
               'gender': form.gender.data,
               'password': form.password.data,
               'type': 'student'
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
        'num1': "Waiting student [ " + str(WS_NUM) + " ]",
        'num2': "Student [ " + str(S_NUM) + "]"
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
    ExamObject['Status'] = 'Active'
    ExamObject['FullMark'] = FullMark
    ExamObject['AccessCode'] = GenerateAccessCode(2)
    StudentsObject['Absent'] = Absent
    StudentsObject['Attended'] = []

    Exam['ExamInformation'] = ExamObject
    Exam['QuestionInformation'] = QuestionObject
    Exam['StudentsInformation'] = StudentsObject
    ActiveExamsDB.insert_one(Exam)
    data = {
        'list': Multiple_Content,
        'id': id
    }
    return data
