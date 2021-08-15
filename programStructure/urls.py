import werkzeug
from programStructure import app, log, Setting_ID
from flask import render_template, url_for, redirect, flash, request, session
from .models import GetUser, Student, WS, SiDB, QDB, ActiveExamsDB
from .forms import SignUp, LoginForm , LoginFormInArabic , SignUpInArabic
from .functions import SendWaitingRequest, savepic, CreateAutoExamObject, AddStudent, \
    DeleteWaitingStudent, \
    ReturnNewStudentNumber, \
    DeleteStudent, ReturnExamsStatus, CreateManualExamObject

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
    Language = request.cookies.get('Language')
    global form
    if Language == "English" or Language == "None" :
        form = LoginForm()
    elif Language == "Arabic" :
        form = LoginFormInArabic()

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
                return render_template('login.html', errorM=errorC, form=form, bootstrap=bootstrap,
                                       normalize=normalize,
                                       loginCss=loginCss,Language=Language, Sett=Sett)
    return render_template("login.html", bootstrap=bootstrap, normalize=normalize,
                           loginCss=loginCss, form=form,Language=Language, font=font, Sett=Sett)


@app.route('/register', methods=['POST', 'GET'])
def register():
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    registerCss = url_for('static', filename='css/register.css')
    Sett = SiDB.find_one({'_id': Setting_ID})
    Language = request.cookies.get('Language')
    global form
    if Language == "English" or Language == "None":
        form = SignUp()
    elif Language == "Arabic":
        form = SignUpInArabic()
    if form.validate_on_submit():
        SendWaitingRequest(form)
        if Language == 'English' or Language is None:
            flash('Waiting for approval please try to login later')
        elif Language == 'Arabic':
            flash('في انتظار الموافقة حاول مجددا لاحقا')
        return redirect(url_for('login'))
    if form.errors:
        global errorC
        for ferror in form.errors:
            for errorM in form[ferror].errors:
                errorC = errorM
        return render_template('register.html', errorM=errorC, form=form, font=font, bootstrap=bootstrap,
                               normalize=normalize, registerCss=registerCss, Sett=Sett)

    return render_template("register.html", bootstrap=bootstrap, normalize=normalize,
                           registerCss=registerCss, form=form, Language=Language ,font=font, Sett=Sett)


@app.route('/redirectto')
@login_required
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
    Language = request.cookies.get('Language')
    return render_template("student.html", bootstrap=bootstrap, normalize=normalize,
                           student=student,Language=Language, font=font, Admin=Admin, Sett=Sett, user=user)


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
        Language = request.cookies.get('Language')
        return render_template("Admin.html", bootstrap=bootstrap, normalize=normalize,
                               Admin=Admin, user=user, font=font, students=students, waiting=waiting, s=S_NUM,
                               ws=WS_NUM, Language=Language ,Sett=Sett)
    else:
        return redirect(url_for('redirectto'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/acceptstudent', methods=['POST', 'GET'])
@login_required
def accept():
    sid = request.get_json()
    AddStudent(sid['id'])
    data = ReturnNewStudentNumber()
    return data


@app.route('/refusestudent', methods=['POST', 'GET'])
@login_required
def refuse():
    sid = request.get_json()
    DeleteWaitingStudent(sid['id'])
    data = ReturnNewStudentNumber()
    return data


@app.route('/Students', methods=['POST', 'GET'])
@login_required
def Students():
    user = Student.find_one({'_id': current_user.id})
    S_NUM = len(list(Student.find({'type': 'student'})))
    students = list(Student.find({'type': 'student'}))
    Sett = SiDB.find_one({'_id': Setting_ID})
    AdminHead = render_template('AdminHead.html')
    Language = request.cookies.get('Language')
    data = {
        'temp': render_template('Students.html', Language=Language ,user=user, S_NUM=S_NUM, students=students, Sett=Sett),
        'AdminHead': AdminHead
    }
    return data


@app.route('/Waiting_Students', methods=['POST', 'GET'])
@login_required
def Waiting_Students():
    user = Student.find_one({'_id': current_user.id})
    WS_NUM = len(list(WS.find()))
    waiting = list(WS.find())
    Sett = SiDB.find_one({'_id': Setting_ID})
    AdminHead = render_template('AdminHead.html')
    Language = request.cookies.get('Language')
    data = {
        'temp': render_template('WaitingStudent.html', Language=Language ,user=user, WS_NUM=WS_NUM, waiting=waiting, Sett=Sett),
        'AdminHead': AdminHead
    }
    return data


@app.route('/dashboard-settings', methods=['POST', 'GET'])
@login_required
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
    Language = request.cookies.get('Language')
    return render_template('Settings.html', Language=Language ,bootstrap=bootstrap, normalize=normalize,
                           Admin=Admin, user=user, font=font, settings=settings, Sett=Sett)


@app.route('/deletestudent', methods=['POST', 'GET'])
@login_required
def deleteSt():
    sid = request.get_json()
    DeleteStudent(sid['id'])
    data = ReturnNewStudentNumber()
    return data


@app.route('/Changing', methods=['POST', 'GET'])
@login_required
def Changing():
    sid = request.get_json()
    SiDB.update_one({'_id': Setting_ID}, {'$set': {
        'site_name': sid['SiteName']
    }})
    return 'Done'


@app.route('/Addition', methods=['POST', 'GET'])
@login_required
def Addition():
    sid = request.get_json()
    SiDB.update({'_id': Setting_ID}, {
        '$push': {
            'Addition-Information': sid
        }
    })
    return "Your changes saved"


@app.route('/UpdateInformation', methods=['POST', 'GET'])
@login_required
def UpdateInformation():
    sid = request.get_json()
    Student.update_one({'_id': current_user.id}, {'$set': {
        'Addition': sid
    }})
    return "Information Updated"


@app.route('/AddingQ', methods=['POST', 'GET'])
@login_required
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
@login_required
def QConfiguration():
    sid = request.get_json()
    SiDB.update({'_id': Setting_ID}, {
        '$push': {
            'Q-Configuration': sid
        }
    })
    return "Your changes saved"


@app.route('/AddQtoDataBase', methods=['POST', 'GET'])
@login_required
def AddQtoDataBase():
    sid = request.get_json()
    QDB.insert_one(sid)
    return "Your question added"


@app.route('/AddImagedQtoDataBase', methods=['POST', 'GET'])
@login_required
def AddImagedQtoDataBase():
    sid = request.get_json()
    session['ImagedID'] = sid['_id']
    QDB.insert_one(sid)
    return "Question Added"


@app.route('/AddTheImage', methods=['POST', 'GET'])
@login_required
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
@login_required
def AddingAutoExam():
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    Admin = url_for('static', filename='css/Admin.css')
    settings = url_for('static', filename='css/settings.css')
    Language = request.cookies.get('Language')
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    user = Student.find_one({'_id': current_user.id})
    Sett = SiDB.find_one({'_id': Setting_ID})
    QNum = len(list(QDB.find()))
    return render_template('AddingAutoExam.html', bootstrap=bootstrap, normalize=normalize,
                           Admin=Admin, QNum=QNum, Language=Language ,user=user, font=font, settings=settings, Sett=Sett)


@app.route('/AddAutoExam', methods=['POST', 'GET'])
@login_required
def AddAutoExam():
    E_info = request.get_json()
    CreateAutoExamObject(E_info)
    Language = request.cookies.get('Language')
    if Language == 'English' or Language is None:
        return 'Exam Added'
    elif Language == 'Arabic' :
        return 'تمت اضافة الامتحان'

@app.route('/exams', methods=['POST', 'GET'])
@login_required
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
    Exams = list(ActiveExamsDB.find())
    Language = request.cookies.get('Language')
    return render_template('exam.html', bootstrap=bootstrap, normalize=normalize,
                           Admin=Admin, Language=Language ,Exams=Exams, user=user, font=font, examCSS=examCSS, Sett=Sett)


@app.route('/returnExams', methods=['POST', 'GET'])
@login_required
def returnExams():
    Exams = list(ActiveExamsDB.find())
    Language = request.cookies.get('Language')
    temp1 = render_template('ActiveExams.html', Language=Language ,Exams=Exams)
    temp2 = render_template('PublishedExam.html', Language=Language ,Exams=Exams)
    temp3 = render_template('SubmittedExam.html',Language=Language , Exams=Exams)

    data = {
        'temp': temp1,
        'temp2': temp2,
        'temp3': temp3
    }
    return data


@app.route('/Exam/<int:exam_id>', methods=['GET', 'POST'])
@login_required
def examDash(exam_id):
    try:
        exam = ActiveExamsDB.find_one({'_id': exam_id})
        StudentInformation = exam['StudentsInformation']
    except TypeError:
        return redirect(url_for('exams'))
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    Admin = url_for('static', filename='css/Admin.css')
    examCSS = url_for('static', filename='css/Exdash.css')
    Sett = SiDB.find_one({'_id': Setting_ID})
    Language = request.cookies.get('Language')
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    return render_template('ExamDashboard.html', bootstrap=bootstrap, normalize=normalize,
                           Admin=Admin, Language=Language ,Sett=Sett, exam=exam, ST=StudentInformation, font=font, examCSS=examCSS)


@app.route('/ExamQuestions/<int:exam_id>', methods=['GET', 'POST'])
@login_required
def examQ(exam_id):
    exam = ActiveExamsDB.find_one({'_id': exam_id})
    Questions = exam['Questions']
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    Admin = url_for('static', filename='css/Admin.css')
    examCSS = url_for('static', filename='css/ExamPR.css')
    Language = request.cookies.get('Language')
    Sett = SiDB.find_one({'_id': Setting_ID})
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    return render_template('ExamPreview.html', bootstrap=bootstrap, normalize=normalize,
                           Admin=Admin, Language=Language ,Sett=Sett, exam=exam ,QU=Questions, font=font, examCSS=examCSS)


@app.route('/ExamPublish/<int:exam_id>', methods=['GET', 'POST'])
@login_required
def ExamPublish(exam_id):
    exam = ActiveExamsDB.find_one({'_id': exam_id})
    for s in exam['StudentsInformation']['Absent']:
        Student.update_one(s, {
            '$push': {
                'Messages': exam
            }
        })
    ActiveExamsDB.update_one(exam, {
        '$set': {
            'ExamInformation.Status': 'Published'
        }
    })
    Language = request.cookies.get('Language')
    if Language == 'English' or Language is None:
        flash('Your exam published')
    elif Language == 'Arabic' :
        flash('تم نشر امتحانك')

    return redirect(url_for('exams'))


@app.route('/ExamDelete/<int:exam_id>', methods=['GET', 'POST'])
@login_required
def ExamDelete(exam_id):
    exam = ActiveExamsDB.find_one({'_id': exam_id})
    for s in exam['StudentsInformation']['Absent']:
        if s:
            Student.update_one(s, {
                '$pull': {
                    'Messages': exam
                }
            })
    ActiveExamsDB.update_one(exam, {
        '$set': {
            'ExamInformation.Status': 'Submitted'
        }
    })
    Language = request.cookies.get('Language')
    if Language == 'English' or Language is None:
        flash('Your exam deleted from students')
    elif Language == 'Arabic' :
        flash('تم حذف الامتحان من عند الطلاب')

    return redirect(url_for('exams'))


@app.route('/Messages', methods=['GET', 'POST'])
@login_required
def Messages():
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    Admin = url_for('static', filename='css/Admin.css')
    message = url_for('static', filename='css/message.css')
    student = url_for('static', filename='css/student.css')
    Sett = SiDB.find_one({'_id': Setting_ID})
    user = Student.find_one({'_id': current_user.id})
    Language = request.cookies.get('Language')
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    return render_template('Message.html', bootstrap=bootstrap, normalize=normalize,
                           Admin=Admin, Language=Language ,student=student, Sett=Sett, user=user, font=font, message=message)


@app.route('/DeleteMSG', methods=['POST', 'GET'])
@login_required
def DeleteMSG():
    E_info = request.get_json()
    user = Student.find_one({'_id': current_user.id})
    for m in user['Messages']:
        if m['_id'] == E_info['id']:
            Student.update(user,
                           {'$pull': {
                               'Messages': {
                                   '_id': E_info['id']
                               }
                           }})

    return 'Deleted'


@app.route('/GoToExam', methods=['POST', 'GET'])
@login_required
def GoToExam():
    E_info = request.get_json()
    exam = ActiveExamsDB.find_one({'_id': E_info['id']})
    user = Student.find_one({'_id': current_user.id})
    ActiveExamsDB.update(exam,
                         {'$pull': {
                             'StudentsInformation.Absent': {
                                 '_id': user['_id']
                             }
                         }})

    if user not in exam['StudentsInformation']['Attended']:
        ActiveExamsDB.update({'_id': exam['_id']}, {
            '$push': {
                'StudentsInformation.Attended': user
            }
        })

    for m in user['Messages']:
        if m['_id'] == E_info['id']:
            Student.update(user,
                           {'$pull': {
                               'Messages': {
                                   '_id': E_info['id']
                               }
                           }})

    return 'OKAY'


@app.route('/StudentExam/<int:exam_id>', methods=['POST', 'GET'])
@login_required
def StudentExam(exam_id):
    exam = ActiveExamsDB.find_one({'_id': exam_id})
    Questions = exam['Questions']
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    Admin = url_for('static', filename='css/Admin.css')
    examCSS = url_for('static', filename='css/ExamPR.css')
    user = Student.find_one({'_id' : current_user.id})
    Sett = SiDB.find_one({'_id': Setting_ID})
    Language = request.cookies.get('Language')
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    if user in exam['StudentsInformation']['Attended']:
        if Language == 'English' or Language is None:
            flash('You attended before')
            return redirect(url_for('Messages'))
        elif Language == 'Arabic':
            flash('لقد حضرت من قبل')
            return redirect(url_for('Messages'))
    return render_template('StudentExam.html', bootstrap=bootstrap, normalize=normalize,
                           Admin=Admin, Sett=Sett, exam=exam, QU=Questions, font=font, examCSS=examCSS)


@app.route('/SendingSubmitting', methods=['POST', 'GET'])
@login_required
def SendingSubmitting():
    E_info = request.get_json()
    exam = ActiveExamsDB.find_one({'_id': E_info['id']})
    user = Student.find_one({'_id': current_user.id})
    Submitting = {
        '_id': current_user.id,
        'firstName': user['first_name'],
        'lastName': user['last_name'],
        'score': E_info['score']
    }
    ActiveExamsDB.update_one(exam, {
        '$push': {
            'StudentsInformation.Submitted': Submitting
        }
    })

    return 'OKAY'


@app.route('/SendingResult/<int:exam_id>', methods=['POST', 'GET'])
@login_required
def SendingResult(exam_id):
    exam = ActiveExamsDB.find_one({'_id': exam_id})

    for Submit in exam['StudentsInformation']['Submitted']:
        user = Student.find_one({'_id': Submit['_id']})
        Student.update_one(user, {
            '$push': {
                'Results': {
                    'ExamId': exam['_id'],
                    'ExamQ': exam['QuestionInformation'],
                    'Mark': Submit['score'],
                    'status': 'Unseen'
                }
            }
        })

    Language = request.cookies.get('Language')
    if Language == 'English' or Language is None:
        flash('The results sent')
    elif Language == 'Arabic' :
        flash('تم ارسال الدرجات')
    return redirect(url_for('exams'))


@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    Admin = url_for('static', filename='css/Admin.css')
    message = url_for('static', filename='css/message.css')
    student = url_for('static', filename='css/student.css')
    Sett = SiDB.find_one({'_id': Setting_ID})
    user = Student.find_one({'_id': current_user.id})
    Language = request.cookies.get('Language')
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    try:
        for i, r in enumerate(list(user['Results'])):
            if r['status'] == 'Unseen':
                Student.update_one({'_id': current_user.id}, {
                    '$set': {
                        'Results.' + str(i) + '.status': 'seen'
                    }
                })
    except KeyError:
        if Language == 'English' or Language is None:
            flash('No Results yet')
        elif Language == 'Arabic':
            flash('لا يوجد درجات بعد')
        return redirect(url_for('profile'))
    return render_template('Result.html', bootstrap=bootstrap, normalize=normalize,
                           Admin=Admin, Language=Language ,student=student, Sett=Sett, user=user, font=font, message=message)

@app.route('/AddingManExam', methods=['POST', 'GET'])
@login_required
def AddingManExam():
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
    Language = request.cookies.get('Language')
    return render_template('AddManualExam.html', bootstrap=bootstrap, normalize=normalize,
                           Admin=Admin, Language=Language ,QNum=QNum, user=user, font=font, settings=settings, Sett=Sett)


@app.route('/AddManualExam', methods=['POST', 'GET'])
@login_required
def AddManualExam():
    E_info = request.get_json()
    data = CreateManualExamObject(E_info)
    return data


@app.route('/GetQuestions', methods=['POST', 'GET'])
@login_required
def GetQuestions():
    E_info = request.get_json()
    questions = E_info['list']
    Language = request.cookies.get('Language')
    return render_template('QuestionChoose.html', Language=Language,question=questions)


@app.route('/UpQOfManToMongo', methods=['POST', 'GET'])
@login_required
def UpQOfManToMongo():
    E_info = request.get_json()
    E_Q = []
    FullMark = 0
    for q in E_info['list']:
        Q = QDB.find_one({'_id': int(q)})
        E_Q.append(Q)

    exam = ActiveExamsDB.find_one({'_id': E_info['id']})

    for Question in E_Q:
        Score = list(Question['score'])
        for score in Score:
            FullMark += int(score)

    ActiveExamsDB.update_one(exam, {
        '$set': {
            'ExamInformation.FullMark': FullMark,
            'QuestionInformation.QNO': len(E_Q),
            'Questions': E_Q
        }
    })
    Language = request.cookies.get('Language')
    if Language == 'English' or Language is None:
        return 'Exam Added'
    elif Language == 'Arabic':
        return 'تمت اضافة الامتحان'
