import os
import random

import werkzeug

from programStructure import app, log, Setting_ID
from flask import render_template, url_for, redirect, flash, request, jsonify, session
from .models import GetUser, Student, WS, SiDB, QDB, ActiveExamsDB
from .forms import SignUp, LoginForm
from .functions import SendWaitingRequest, savepic, GenerateAccessCode, CreateAutoExamObject, AddStudent, \
    DeleteWaitingStudent, \
    ReturnNewStudentNumber, \
    DeleteStudent
from flask_login import login_user, current_user, logout_user, login_required
from .User import User


@log.user_loader
def load_user(id):
    return GetUser(id)


@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('redirectto'))
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    loginCss = url_for('static', filename='css/login.css')
    Sett = SiDB.find_one({'_id': Setting_ID})
    form = LoginForm()
    if form.validate_on_submit():
        user = Student.find_one({'email': form.email.data})
        this_user = User(user['_id'])
        login_user(this_user)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('redirectto'))
    if form.errors:
        for errorfield in form.errors:
            for errorM in form[errorfield].errors:
                errorC = errorM
                return render_template('Login.html', errorM=errorC, form=form, bootstrap=bootstrap,
                                       normalize=normalize,
                                       loginCss=loginCss, Sett=Sett)
    return render_template("login.html", bootstrap=bootstrap, normalize=normalize,
                           loginCss=loginCss, form=form, font=font, Sett=Sett)


@app.route('/register', methods=['POST', 'GET'])
def register():
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    registerCss = url_for('static', filename='css/register.css')
    Sett = SiDB.find_one({'_id': Setting_ID})
    form = SignUp()
    if form.validate_on_submit():
        SendWaitingRequest(form)
        flash('Waiting for approval please try to login after half hour')
        return redirect(url_for('login'))
    if form.errors:
        global errorC
        for ferror in form.errors:
            for errorM in form[ferror].errors:
                errorC = errorM
        return render_template('Register.html', errorM=errorC, form=form, font=font, bootstrap=bootstrap,
                               normalize=normalize, registerCss=registerCss, Sett=Sett)

    return render_template("register.html", bootstrap=bootstrap, normalize=normalize,
                           registerCss=registerCss, form=form, font=font, Sett=Sett)


@login_required
@app.route('/redirectto')
def redirectto():
    user = Student.find_one({'_id': current_user.id})
    if user['type'] == 'student':
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('dashboard'))


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    student = url_for('static', filename='css/student.css')
    Admin = url_for('static', filename='css/Admin.css')
    user = Student.find_one({'_id': current_user.id})
    Sett = SiDB.find_one({'_id': Setting_ID})
    return render_template("student.html", bootstrap=bootstrap, normalize=normalize,
                           student=student, font=font, Admin=Admin, Sett=Sett, user=user)


@app.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():
    user = Student.find_one({'_id': current_user.id})
    UserType = user['type']
    if UserType != 'student':
        font = url_for('static', filename='css/font-awesome.min.css')
        bootstrap = url_for('static', filename='css/bootstrap.css')
        normalize = url_for('static', filename='css/normalize.css')
        Admin = url_for('static', filename='css/Admin.css')
        WS_NUM = len(list(WS.find()))
        S_NUM = len(list(Student.find({'type': 'student'})))
        waiting = list(WS.find())
        students = list(Student.find({'type': 'student'}))
        Sett = SiDB.find_one({'_id': Setting_ID})
        return render_template("Admin.html", bootstrap=bootstrap, normalize=normalize,
                               Admin=Admin, user=user, font=font, students=students, waiting=waiting, s=S_NUM,
                               ws=WS_NUM, Sett=Sett)
    else:
        return redirect(url_for('redirectto'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/acceptstudent', methods=['POST', 'GET'])
def accept():
    sid = request.get_json()
    AddStudent(sid['id'])
    data = ReturnNewStudentNumber()
    return data


@app.route('/refusestudent', methods=['POST', 'GET'])
def refuse():
    sid = request.get_json()
    DeleteWaitingStudent(sid['id'])
    data = ReturnNewStudentNumber()
    return data


@app.route('/Students', methods=['POST', 'GET'])
def Students():
    user = Student.find_one({'_id': current_user.id})
    S_NUM = len(list(Student.find({'type': 'student'})))
    students = list(Student.find({'type': 'student'}))
    Sett = SiDB.find_one({'_id': Setting_ID})
    AdminHead = render_template('AdminHead.html')
    data = {
        'temp': render_template('Students.html', user=user, S_NUM=S_NUM, students=students, Sett=Sett),
        'AdminHead': AdminHead
    }
    return data


@app.route('/Waiting_Students', methods=['POST', 'GET'])
def Waiting_Students():
    user = Student.find_one({'_id': current_user.id})
    WS_NUM = len(list(WS.find()))
    waiting = list(WS.find())
    Sett = SiDB.find_one({'_id': Setting_ID})
    AdminHead = render_template('AdminHead.html')
    data = {
        'temp': render_template('WaitingStudent.html', user=user, WS_NUM=WS_NUM, waiting=waiting, Sett=Sett),
        'AdminHead': AdminHead
    }
    return data


@app.route('/dashboard-settings', methods=['POST', 'GET'])
def Settings():
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    Admin = url_for('static', filename='css/Admin.css')
    settings = url_for('static', filename='css/settings.css')
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    user = Student.find_one({'_id': current_user.id})
    Sett = SiDB.find_one({'_id': Setting_ID})
    return render_template('Settings.html', bootstrap=bootstrap, normalize=normalize,
                           Admin=Admin, user=user, font=font, settings=settings, Sett=Sett)


@app.route('/deletestudent', methods=['POST', 'GET'])
def deleteSt():
    sid = request.get_json()
    DeleteStudent(sid['id'])
    data = ReturnNewStudentNumber()
    return data


@app.route('/Changing', methods=['POST', 'GET'])
def Changing():
    sid = request.get_json()
    SiDB.update_one({'_id': Setting_ID}, {'$set': {
        'site_name': sid['SiteName']
    }})
    return 'Done'


@app.route('/Addition', methods=['POST', 'GET'])
def Addition():
    sid = request.get_json()
    SiDB.update({'_id': Setting_ID}, {
        '$push': {
            'Addition-Information': sid
        }
    })
    return "Your changes saved"


@app.route('/UpdateInformation', methods=['POST', 'GET'])
def UpdateInformation():
    sid = request.get_json()
    Student.update_one({'_id': current_user.id}, {'$set': {
        'Addition': sid
    }})
    return "Information Updated"


@app.route('/AddingQ', methods=['POST', 'GET'])
def AddingQ():
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    Admin = url_for('static', filename='css/Admin.css')
    settings = url_for('static', filename='css/settings.css')
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    user = Student.find_one({'_id': current_user.id})
    Sett = SiDB.find_one({'_id': Setting_ID})
    return render_template('AddQ.html', bootstrap=bootstrap, normalize=normalize,
                           Admin=Admin, user=user, font=font, settings=settings, Sett=Sett)


@app.route('/QConfiguration', methods=['POST', 'GET'])
def QConfiguration():
    sid = request.get_json()
    SiDB.update({'_id': Setting_ID}, {
        '$push': {
            'Q-Configuration': sid
        }
    })
    return "Your changes saved"


@app.route('/AddQtoDataBase', methods=['POST', 'GET'])
def AddQtoDataBase():
    sid = request.get_json()
    QDB.insert_one(sid)
    return "Your question added"


@app.route('/AddImagedQtoDataBase', methods=['POST', 'GET'])
def AddImagedQtoDataBase():
    sid = request.get_json()
    session['ImagedID'] = sid['_id']
    QDB.insert_one(sid)
    return "Question Added"


@app.route('/AddTheImage', methods=['POST', 'GET'])
def AddTheImage():
    if request.method == 'POST':
        global TitleImage
        try:
            if 'titleImage' in request.files:
                TitleImage = savepic(request.files['titleImage'], session['ImagedID'])
                QDB.update_one({'_id': session['ImagedID']}, {
                    '$set': {
                        'TitleImage': TitleImage
                    }
                })
            ChoicesImage = []
            Q = QDB.find_one({'_id': session['ImagedID']})
            ChoicesLen = len(Q['Choices'])
            for f in range(1, ChoicesLen + 1):
                if 'ChoiceImage' + str(f) in request.files:
                    PhotoName = savepic(request.files['ChoiceImage' + str(f)], session['ImagedID'])
                    ChoicesImage.append(PhotoName)

            QDB.update_one({'_id': session['ImagedID']}, {
                '$set': {
                    'ChoicesImage': ChoicesImage
                }
            })
        except werkzeug.exceptions.BadRequestKeyError:
            return 'Error Occurred'
    return "Question Added"


@app.route('/AddingAutoExam', methods=['POST', 'GET'])
def AddingAutoExam():
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    Admin = url_for('static', filename='css/Admin.css')
    settings = url_for('static', filename='css/settings.css')
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    user = Student.find_one({'_id': current_user.id})
    Sett = SiDB.find_one({'_id': Setting_ID})
    QNum = len(list(QDB.find()))
    return render_template('AddingAutoExam.html', bootstrap=bootstrap, normalize=normalize,
                           Admin=Admin, QNum=QNum, user=user, font=font, settings=settings, Sett=Sett)


@app.route('/AddAutoExam', methods=['POST', 'GET'])
def AddAutoExam():
    E_info = request.get_json()
    CreateAutoExamObject(E_info)
    return 'Exam Added'


@app.route('/exams', methods=['POST', 'GET'])
def exams():
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    Admin = url_for('static', filename='css/Admin.css')
    examCSS = url_for('static', filename='css/exam.css')
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    user = Student.find_one({'_id': current_user.id})
    Sett = SiDB.find_one({'_id': Setting_ID})
    Exams = ActiveExamsDB.find()
    return render_template('exam.html', bootstrap=bootstrap, normalize=normalize,
                           Admin=Admin, Exams=Exams, user=user, font=font, examCSS=examCSS, Sett=Sett)


@app.route('/Exam/<int:exam_id>', methods=['GET', 'POST'])
def examDash(exam_id):
    exam = ActiveExamsDB.find_one({'_id': exam_id})
    StudentInformation = exam['StudentsInformation']
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    Admin = url_for('static', filename='css/Admin.css')
    examCSS = url_for('static', filename='css/Exdash.css')
    Sett = SiDB.find_one({'_id': Setting_ID})
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    return render_template('ExamDashboard.html', bootstrap=bootstrap, normalize=normalize,
                           Admin=Admin, Sett=Sett,exam=exam ,ST=StudentInformation, font=font, examCSS=examCSS)


@app.route('/ExamQuestions/<int:exam_id>', methods=['GET', 'POST'])
def examQ(exam_id):
    exam = ActiveExamsDB.find_one({'_id': exam_id})
    Questions = exam['Questions']
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    Admin = url_for('static', filename='css/Admin.css')
    examCSS = url_for('static', filename='css/ExamPR.css')
    Sett = SiDB.find_one({'_id': Setting_ID})
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    return render_template('ExamPreview.html', bootstrap=bootstrap, normalize=normalize,
                           Admin=Admin, Sett=Sett, exam=exam ,QU=Questions, font=font, examCSS=examCSS)