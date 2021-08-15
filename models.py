from pymongo import MongoClient
from .User import User

client = MongoClient("mongodb+srv://Users:U196S54@examistadatabase.x1hz4.mongodb.net/"
                     "ExamistaDataBase?retryWrites=true&w=majority")


UsersDB = client.get_database('Users')
Student = UsersDB.get_collection('Students')
WS = UsersDB.get_collection('WS')
SiDB = UsersDB.get_collection('Settings')
QDB = UsersDB.get_collection('Questions')
ActiveExamsDB = UsersDB.get_collection('Active_Exam')



def GetUser(id):
    user_data = Student.find_one({'_id': id})
    return User(user_data['_id'])