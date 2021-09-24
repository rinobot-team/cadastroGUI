
import pyrebase
import json

class FirebaseConnection():
    """
    Classe responsável pela conexão e manipulação do banco de dados Firebase Realtime Database
    """

    _firebaseConfig = {
        'apiKey': "AIzaSyBRyNACN7FAwDdcKuYXvTD9I6Ek2TUjfDo",
        'authDomain': "testebancodedados-56c27.firebaseapp.com",
        'databaseURL': "https://testebancodedados-56c27.firebaseio.com",
        'projectId': "testebancodedados-56c27",
        'storageBucket': "testebancodedados-56c27.appspot.com",
        'messagingSenderId': "927314771289",
        'appId': "1:927314771289:web:b6d4252a57af18c99da048",
        'measurementId': "G-86QRW9J99C"
    }

    def __init__(self, login) -> None:
        self.firebase_app = pyrebase.initialize_app(self._firebaseConfig)
        self._db = self.firebase_app.database()
        self._auth = self.firebase_app.auth()
        self._login = self.login(login['email'], login['password'])

        self.my_stream = self._db.child('testebancodedados-56c27').child('Cadastro').stream(self.listener)

    
    def listener(self,event):
        print(event.event_type)  # can be 'put' or 'patch'
        print(event.path)  # relative to the reference, it seems
        print(event.data)  # new data at /reference/event.path. None if deleted


    def signup(self,email,password,phone_number):
        try:
            user = self._auth.create_user(email = email, password = password, phone_number=phone_number)
        except:
            pass


    def login(self,email,password):
        try:
            self._login = self._auth.sign_in_with_email_and_password(email, password)
            # print(login)
            return self._login
        except Exception as e:
            print("Erro no login: ",e.args)
            return {}


    def get_data(self,id):
        if 'idToken' in self._login.keys():
            data = self._db.child('testebancodedados-56c27').child('Cadastro').child(id).get(self._login['idToken'])
            if data.val():
                data = dict(data.val())
                #print(data)
                return data
            else:
                print("ID inexistente.")
                return None
        else:
            print("Não autorizado")
            return {}


    def update_data(self,cod_att,data):
        if 'idToken' in self._login.keys():
            # data = json.dumps(dado)
            print("Updated data: ",data)
            data = self._db.child('testebancodedados-56c27').child('Cadastro').child(cod_att).update(data, self._login['idToken'])
        else:
            print("Não autorizado")
            return {}


    def get_people_keys(self):
        keys = self._db.child('testebancodedados-56c27').child('Cadastro').shallow().get(self._login['idToken'])
        keys = map(int,keys.val())
        keys = list(keys)
        return keys


    def new_user_id(self):
        keys = self.get_people_keys()
        print("Keys: ",keys)
        # ids = []
        # for key in keys:
        #     ids.append(self.get_id(key))
        
        new_id = len(keys)
        while True:
            if new_id in keys:
                new_id += 1
            else:
                break
        return new_id


    def get_id(self,user_code):
        if 'idToken' in self._login.keys():
            data = self._db.child('testebancodedados-56c27').child('Cadastro').child(user_code).child('ID').get(self._login['idToken'])
            data = data.val()
            print(data)
            return data
        else:
            print("Não autorizado")
            return {}


    def new_person(self, data):
        # data_id = str(int(data['ID'])+1)
        data_id = data['ID']
        print("Data: ",data)
        self._db.child('testebancodedados-56c27').child('Cadastro').child(data_id).set(data,self._login['idToken'])