
class SQL_DB_Handler():
    def __init__(self, strDias, strHoras) -> None:
        self.connection = self.retornar_conexao_sql()
        if self.connection:
            self.cursor = self.connection.cursor()

        self.strDias = strDias
        self.strHoras = strHoras

    
    def retornar_conexao_sql(self):
        try:
            server = "DESKTOP-K9EP3PF\SQLEXPRESS"
            database_name = "Membros"
            string_conexao = 'Driver={SQL Server Native Client 11.0};Server='+server+';Database='+database_name+';Trusted_Connection=yes;'
            return pyodbc.connect(string_conexao)
        except:
            pass
    
    def get_data(self,id):
        comando = "SELECT * FROM Cadastro WHERE ID = " + id
        self.cursor.execute(comando)
        dados = self.cursor.fetchone()
        return dados

    def get_schedule(self, day, id):
        comando = "SELECT * FROM " + day + " WHERE ID =  " + id

        self.cursor.execute(comando)
        data = self.cursor.fetchone()
        return data

    def new_person(self, data, boolMtxHorarios):
        comando = "SELECT ID FROM Cadastro"
        self.cursor.execute(comando)
        dados = self.cursor.fetchall()
        ids = list()

        for linha in dados:
            ids.append([x for x in linha][0])

        ids = tuple(ids)
        novaID = max(ids)+1

        comando = "INSERT INTO Cadastro(ID,Nome,DataNascimento,EMail,Cargo) VALUES ("+str(novaID)+", '"+data['Nome']+"','"+data['DataNascimento']+"','"+data['EMail']+"','"+data['Cargo']+"')"
        self.cursor.execute(comando)
        self.connection.commit()
        for j in range(len(self.strDias)):
            comando = "INSERT INTO "+self.strDias[j]+"(ID) VALUES ("+str(novaID)+")"
            self.cursor.execute(comando)
            self.connection.commit()
            for i in range(len(self.strHoras)):
                #comando = "UPDATE Cadastro SET DataNascimento = '1998-02-18' WHERE ID = 1"
                comando = "UPDATE " + self.strDias[j] + " SET "
                comando = comando + "Disp" + self.strHoras[i] + " = " + str(int(boolMtxHorarios[i][j])) + " WHERE ID = " + novaID
                self.cursor.execute(comando)
                self.connection.commit()
        
        return novaID

    def update_data(self, data, boolMtxHorarios):
        comando = "UPDATE Cadastro SET Nome = '"+data['Nome']+"' WHERE ID = "+data['ID']
        self.cursor.execute(comando)

        comando = "UPDATE Cadastro SET DataNascimento = '"+data['DataNascimento']+"' WHERE ID = "+data['ID']
        self.cursor.execute(comando)

        comando = "UPDATE Cadastro SET EMail = '"+data['EMail']+"' WHERE ID = "+data['ID']
        self.cursor.execute(comando)

        comando = "UPDATE Cadastro SET Cargo = '"+data['Cargo']+"' WHERE ID = "+data['ID']
        self.cursor.execute(comando)
        self.connection.commit()

        for j in range(len(self.strDias)):
            for i in range(len(self.strHoras)):
                #comando = "UPDATE Cadastro SET DataNascimento = '1998-02-18' WHERE ID = 1"
                comando = "UPDATE "+self.strDias[j]+" SET "
                comando = comando +"Disp"+self.strHoras[i]+" = "+str(int(boolMtxHorarios[i][j]))+" WHERE ID = "+data['ID']
                print(comando)
                self.cursor.execute(comando)
                self.connection.commit()

    def create_tables(self):
        for i in range(len(self.strDias)):
            comando = "CREATE TABLE "+self.strDias[i]+" (ID INT FOREIGN KEY REFERENCES Cadastro(ID))"
            self.cursor.execute(comando)
            self.connection.commit()
            for j in range(len(self.strHoras)):
                comando = "ALTER TABLE "+self.strDias[i]+" ADD Disp"+self.strHoras[j]+" BIT DEFAULT 1"
                self.cursor.execute(comando)
                self.connection.commit()