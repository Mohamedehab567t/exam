import werkzeug
from programStructure import app, log, Setting_ID
from flask import render_template, url_for, redirect, flash, request, session
from .models import GetUser, Student, WS, SiDB, QDB, ActiveExamsDB
from .forms import SignUp, LoginForm, LoginFormInArabic, SignUpInArabic
from .functions import SendWaitingRequest, savepic, CreateAutoExamObject, AddStudent, \
    DeleteWaitingStudent, \
    ReturnNewStudentNumber, \
    DeleteStudent, DoRank, CreateManualExamObject, \
    GetExamDetailsFromMessagesId, GetKeysFromQ_Configuration \
    , GetFilteredListOnDeleteQ, GetFilteredListOnSearchQ, \
    ReturnNewStudentNumberVersionOfSearch, GetFilteredListOnSearchS, GetFilteredListOnDeleteS, \
    ReturnStudentOfSearchInRankedAdmin, ReturnSToAddInActiveExam, GetAbsentFromPublished

from flask_login import login_user, current_user, logout_user, login_required
from .User import User


@log.user_loader
def load_user(id):
    return GetUser(id)


@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('redirectto'))
    except TypeError:
        session.clear()
        return redirect(url_for('login'))
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    loginCss = url_for('static', filename='css/login.css')
    Sett = SiDB.find_one({'_id': Setting_ID})
    Language = request.cookies.get('Language')
    global form
    if Language == "English" or Language is None:
        form = LoginForm()
    elif Language == "Arabic":
        form = LoginFormInArabic()

    if form.validate_on_submit():
        user = Student.find_one({'phone_number': form.email.data})
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
                                       loginCss=loginCss, Language=Language, Sett=Sett)
    return render_template("login.html", bootstrap=bootstrap, normalize=normalize,
                           loginCss=loginCss, form=form, Language=Language, font=font, Sett=Sett)


@app.route('/register', methods=['POST', 'GET'])
def register():
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    registerCss = url_for('static', filename='css/register.css')
    Sett = SiDB.find_one({'_id': Setting_ID})
    Language = request.cookies.get('Language')
    global form
    if Language == "English" or Language is None:
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
                               normalize=normalize, Language=Language, registerCss=registerCss, Sett=Sett)

    return render_template("register.html", bootstrap=bootstrap, normalize=normalize,
                           registerCss=registerCss, form=form, Language=Language, font=font, Sett=Sett)


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
    ConfigS = Sett['Addition-Information']
    Language = request.cookies.get('Language')
    global Ranked
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    try:
        Ranked = Student.find({'type': 'student'}).sort([("Rank.rank", -1), ("Rank.FullMark", -1)])
    except KeyError:
        pass
    return render_template("student.html", bootstrap=bootstrap, normalize=normalize,
                           student=student, ConfigS=ConfigS, Language=Language, Ranked=Ranked, font=font, Admin=Admin,
                           Sett=Sett,
                           user=user)


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
        Bank = url_for('static', filename='css/Bank.css')
        WS_NUM = len(list(WS.find()))
        S_NUM = len(list(Student.find({'type': 'student'})))
        waiting = list(WS.find())
        students = list(Student.find({'type': 'student'}))
        Sett = SiDB.find_one({'_id': Setting_ID})
        Language = request.cookies.get('Language')
        Q = list(QDB.find())
        return render_template("Admin.html", bootstrap=bootstrap, normalize=normalize,
                               Admin=Admin, user=user, font=font, students=students, waiting=waiting, s=S_NUM,
                               ws=WS_NUM, Language=Language, Bank=Bank, Sett=Sett)
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
    ConfigS = Sett['Addition-Information']
    AdminHead = render_template('AdminHead.html')
    Language = request.cookies.get('Language')
    data = {
        'temp': render_template('Students.html', Language=Language, user=user, S_NUM=S_NUM, students=students,
                                Sett=Sett, ConfigS=ConfigS),
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
        'temp': render_template('WaitingStudent.html', Language=Language, user=user, WS_NUM=WS_NUM, waiting=waiting,
                                Sett=Sett),
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
    return render_template('Settings.html', Language=Language, bootstrap=bootstrap, normalize=normalize,
                           Admin=Admin, user=user, font=font, settings=settings, Sett=Sett)


@app.route('/deletestudent', methods=['POST', 'GET'])
@login_required
def deleteSt():
    sid = request.get_json()
    DeleteStudent(sid['id'])
    StudentsAfterDelete = GetFilteredListOnDeleteS(sid)
    data = ReturnNewStudentNumberVersionOfSearch(StudentsAfterDelete, 'StudentsPart')
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
        'first_name': sid['f'],
        'last_name': sid['l'],
        'phone_number': sid['p'],
        'gender': sid['g'],
        'Addition': sid['i']
    }})
    Language = request.cookies.get('Language')
    if Language == 'English' or Language is None:
        return "Information Updated"
    else:
        return "تم التعديل"


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
    Language = request.cookies.get('Language')
    return render_template('AddQ.html', bootstrap=bootstrap, normalize=normalize,
                           Admin=Admin, user=user, font=font, Language=Language, settings=settings, Sett=Sett)


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
                           Admin=Admin, QNum=QNum, Language=Language, user=user, font=font, settings=settings,
                           Sett=Sett)


@app.route('/AddAutoExam', methods=['POST', 'GET'])
@login_required
def AddAutoExam():
    E_info = request.get_json()
    CreateAutoExamObject(E_info)
    Language = request.cookies.get('Language')
    if Language == 'English' or Language is None:
        return 'Exam Added'
    elif Language == 'Arabic':
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
    try:
        ActiveExamsDB.delete_many({'ExamInformation.Status': 'Without'})
    except TypeError:
        print('Error')

    return render_template('exam.html', bootstrap=bootstrap, normalize=normalize,
                           Admin=Admin, Language=Language, Exams=Exams, user=user, font=font, examCSS=examCSS,
                           Sett=Sett)


@app.route('/returnExams', methods=['POST', 'GET'])
@login_required
def returnExams():
    Exams = list(ActiveExamsDB.find())
    Language = request.cookies.get('Language')
    temp1 = render_template('ActiveExams.html', Language=Language, Exams=Exams)
    temp2 = render_template('PublishedExam.html', Language=Language, Exams=Exams)
    temp3 = render_template('SubmittedExam.html', Language=Language, Exams=Exams)

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
        NotHereStudent = ReturnSToAddInActiveExam(exam)
        NotHereStudentPublished = GetAbsentFromPublished(exam_id)
        ST = exam['StudentsInformation']
    except ValueError:
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
                           Admin=Admin, Language=Language, Sett=Sett, exam=exam, ST=ST, font=font,
                           examCSS=examCSS, NotHereStudent=NotHereStudent,
                           NotHereStudentPublished=NotHereStudentPublished)


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
                           Admin=Admin, Language=Language, Sett=Sett, exam=exam, QU=Questions, font=font,
                           examCSS=examCSS)


@app.route('/ExamPublish/<int:exam_id>', methods=['GET', 'POST'])
@login_required
def ExamPublish(exam_id):
    exam = ActiveExamsDB.find_one({'_id': exam_id})
    for s in exam['StudentsInformation']['Absent']:
        Student.update_one({'_id': s['_id']}, {
            '$push': {
                'Messages': {'_id': exam['_id']}
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
    elif Language == 'Arabic':
        flash('تم نشر امتحانك')

    return redirect(url_for('exams'))


@app.route('/ExamDelete/<int:exam_id>', methods=['GET', 'POST'])
@login_required
def ExamDelete(exam_id):
    exam = ActiveExamsDB.find_one({'_id': exam_id})

    for s in exam['StudentsInformation']['Absent']:
        Student.update_one({'_id': s['_id']}, {
            '$pull': {
                'Messages': {
                    '_id': exam['_id']
                }
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
    elif Language == 'Arabic':
        flash('تم حذف الامتحان من عند الطلاب')

    return redirect(url_for('exams'))


@app.route('/Messages', methods=['GET', 'POST'])
@login_required
def Messages():
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    Admin = url_for('static', filename='css/Admin.css')
    student = url_for('static', filename='css/student.css')
    message = url_for('static', filename='css/message.css')
    Sett = SiDB.find_one({'_id': Setting_ID})
    user = Student.find_one({'_id': current_user.id})
    ExamsMessages = GetExamDetailsFromMessagesId(user)
    Language = request.cookies.get('Language')
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    return render_template('Message.html', bootstrap=bootstrap, normalize=normalize,
                           Admin=Admin, Language=Language, student=student, Sett=Sett, user=user, font=font,
                           message=message, ExamsMessages=ExamsMessages)


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
    exam = ActiveExamsDB.find_one({'_id': int(E_info['id'])})
    user = Student.find_one({'_id': current_user.id})
    ActiveExamsDB.update(exam,
                         {'$pull': {
                             'StudentsInformation.Absent': {
                                 '_id': user['_id']
                             }
                         }})
    Language = request.cookies.get('Language')
    if user in exam['StudentsInformation']['Attended']:
        if Language == 'English' or Language is None:
            flash('You attended before')
            return redirect(url_for('Messages'))
        elif Language == 'Arabic':
            flash('لقد حضرت من قبل')
            return redirect(url_for('Messages'))
    elif user not in exam['StudentsInformation']['Attended']:
        ActiveExamsDB.update({'_id': exam['_id']}, {
            '$push': {
                'StudentsInformation.Attended': user
            }
        })
        for m in user['Messages']:
            if m['_id'] == exam['_id']:
                Student.update(user,
                               {'$pull': {
                                   'Messages': {
                                       '_id': exam['_id']
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
    user = Student.find_one({'_id': current_user.id})
    Sett = SiDB.find_one({'_id': Setting_ID})
    if current_user.is_anonymous:
        return redirect(url_for('login'))
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
        'score': E_info['score'],
        'QuestionScore': E_info['QuestionScore']
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
        DoRank(user, exam, Submit)
    ActiveExamsDB.update_one({'_id': exam_id}, {
        '$set': {
            'r': 'true'
        }
    })

    Language = request.cookies.get('Language')
    if Language == 'English' or Language is None:
        flash('The results sent')
    elif Language == 'Arabic':
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
                           Admin=Admin, Language=Language, student=student, Sett=Sett, user=user, font=font,
                           message=message)


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
                           Admin=Admin, Language=Language, QNum=QNum, user=user, font=font, settings=settings,
                           Sett=Sett)


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
    return render_template('QuestionChoose.html', Language=Language, question=questions)


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
        if Question['kind'] == 'Q':
            Score = list(Question['score'])
            for score in Score:
                FullMark += int(score)
        elif Question['kind'] == 'P':
            qs = Question['P-Questions']
            Score = []
            for s in qs:
                Score.append(s['score'])
            for score in Score:
                for s in score:
                    FullMark += int(s)

    ActiveExamsDB.update_one(exam, {
        '$set': {
            'ExamInformation.FullMark': FullMark,
            'ExamInformation.Status': 'Active',
            'QuestionInformation.QNO': len(E_Q),
            'Questions': E_Q
        }
    })
    Language = request.cookies.get('Language')
    if Language == 'English' or Language is None:
        return 'Exam Added'
    elif Language == 'Arabic':
        return 'تمت اضافة الامتحان'


@app.route('/RankingAdmin')
def RankingA():
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    user = Student.find_one({'_id': current_user.id})
    A = url_for('static', filename='css/Admin.css')
    Sett = SiDB.find_one({'_id': Setting_ID})
    ConfigS = Sett['Addition-Information']
    global Ranked
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    try:
        Ranked = Student.find({'type': 'student'}).sort([("Rank.rank", -1), ("Rank.FullMark", -1)])
    except KeyError:
        pass
    return render_template('RankingInAdmin.html', ConfigS=ConfigS, font=font, Sett=Sett, user=user, Ranked=Ranked,
                           bootstrap=bootstrap,
                           normalize=normalize, A=A)


@app.route('/CheckSettings', methods=['POST', 'GET'])
@login_required
def CheckSettings():
    E_info = request.get_json()
    SiDB.update_one({'_id': Setting_ID}, {
        '$set': {
            'ShowPiece': E_info['ShowPiece']
        }
    })
    return 'Done'


@app.route('/StudentInformation/<int:id>', methods=['POST', 'GET'])
@login_required
def StudentInformation(id):
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    user = Student.find_one({'_id': id})
    A = url_for('static', filename='css/Admin.css')
    student = url_for('static', filename='css/student.css')
    Sett = SiDB.find_one({'_id': Setting_ID})
    return render_template('StudentInformation.html', font=font, Sett=Sett, user=user, bootstrap=bootstrap,
                           normalize=normalize, student=student, A=A)


@app.route('/BankOfQuestion', methods=['POST', 'GET'])
@login_required
def BankOfQuestion():
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    A = url_for('static', filename='css/Admin.css')
    Bank = url_for('static', filename='css/Bank.css')
    user = Student.find_one({'_id': current_user.id})
    Sett = SiDB.find_one({'_id': Setting_ID})
    Q = list(QDB.find())
    ConfigQ = GetKeysFromQ_Configuration()
    return render_template('BankOfQuestion.html', font=font, Sett=Sett, user=user, bootstrap=bootstrap,
                           normalize=normalize, A=A, Bank=Bank, Q=Q, ConfigQ=ConfigQ)


@app.route('/UpdateQuestionFromBank/<int:id>', methods=['POST', 'GET'])
@login_required
def UpdateQuestionFromBank(id):
    E_info = request.get_json()
    QDB.update_one({'_id': id}, {
        '$set': {
            'Q-title': E_info['title'],
            'Choices': E_info['Choices'],
            'score': E_info['score']
        }
    })
    q = QDB.find_one({'_id': id})

    return render_template('ReturnOneQuestionAfetrUpdate.html', q=q)


@app.route('/GetFilteredQuestion', methods=['POST', 'GET'])
@login_required
def GetFilteredQuestion():
    val = request.get_json()
    Questions = GetFilteredListOnSearchQ(val, QDB)
    return render_template('ReturnOneQuestionAfterFiltered.html', Questions=Questions)


@app.route('/DeleteBankQ', methods=['POST', 'GET'])
@login_required
def DeleteBankQ():
    val = request.get_json()
    QuestionsToGet = GetFilteredListOnDeleteQ(val)
    return render_template('ReturnOneQuestionAfterFiltered.html', Questions=QuestionsToGet)


@app.route('/GetFilteredStudent', methods=['POST', 'GET'])
@login_required
def GetFilteredStudent():
    val = request.get_json()
    FS = GetFilteredListOnSearchS(val, Student)
    return ReturnNewStudentNumberVersionOfSearch(FS, 'StudentsPart')


@app.route('/GetFilteredStudentRankedAdmin', methods=['POST', 'GET'])
@login_required
def GetFilteredStudentRankedAdmin():
    val = request.get_json()
    return ReturnStudentOfSearchInRankedAdmin(val, Student, 'GetFilteredRanked')


@app.route('/GetFilteredStudentRankedStudent', methods=['POST', 'GET'])
@login_required
def GetFilteredStudentRankedStudent():
    val = request.get_json()
    return ReturnStudentOfSearchInRankedAdmin(val, Student, 'GetFilteredRankedInStudent')


@app.route('/ShowStudentAnswer', methods=['POST', 'GET'])
@login_required
def ShowStudentAnswer():
    global val
    if request.method == 'POST':
        val = request.get_json()
    QU = []
    font = url_for('static', filename='css/font-awesome.min.css')
    bootstrap = url_for('static', filename='css/bootstrap.css')
    normalize = url_for('static', filename='css/normalize.css')
    Admin = url_for('static', filename='css/Admin.css')
    examCSS = url_for('static', filename='css/ExamPR.css')
    Sett = SiDB.find_one({'_id': Setting_ID})
    try :
        for key in val:
            Q = QDB.find_one({'_id': int(key)})
            QU.append(Q)
    except NameError:
        redirect(url_for('ShowStudentAnswer'))
    return render_template('StudentAnswers.html', font=font, bootstrap=bootstrap
                           , normalize=normalize, Admin=Admin
                           , examCSS=examCSS, Sett=Sett, val=val, QU=QU)


@app.route('/showDirectAccess/<int:id>', methods=['POST', 'GET'])
@login_required
def showDirectAccess(id):
    ActiveExamsDB.update_one({'_id': id}, {
        '$set': {
            'showDirectAccess': 'show'
        }
    })
    flash('تم الاظهار')
    return redirect(url_for('examDash', exam_id=id))


@app.route('/AddStudentToExam', methods=['POST', 'GET'])
@login_required
def AddStudentToExam():
    INFO = request.get_json()
    exam = ActiveExamsDB.find_one({'_id': INFO['Eid']})
    student = Student.find_one({'_id': INFO['Sid']})
    if INFO['status'] == 'Active':
        ActiveExamsDB.update_one(exam, {
            '$push': {
                'StudentsInformation.Absent': student
            }
        })
    elif INFO['status'] == 'Published':
        ActiveExamsDB.update_one(exam, {
            '$push': {
                'StudentsInformation.Absent': student
            }
        })
        Student.update_one(student, {
            '$push': {
                'Messages': {'_id': exam['_id']}
            }
        })
    return 'Done'


@app.route('/AddingP', methods=['POST', 'GET'])
@login_required
def AddingP():
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
    return render_template('AddP.html', bootstrap=bootstrap, normalize=normalize,
                           Admin=Admin, user=user, font=font, Language=Language, settings=settings, Sett=Sett)


@app.route('/AddPtoDataBase', methods=['POST', 'GET'])
@login_required
def AddPtoDataBase():
    sid = request.get_json()
    QDB.insert_one(sid)
    return "Your Passage added"
