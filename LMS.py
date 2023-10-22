import mysql.connector
from mysql.connector import Error
import datetime
def connection_creator(hostname,username,password,db):
    connection = None
    try:
        connection = mysql.connector.connect(host = hostname,user = username,password=password,database=db)
        print("connection to MYSQL is successfull")
    except Error as err:
        print("The error ",{err} ," occured")
    return connection
def create_database(connection ,query):
    mycursor = connection.cursor()
    try:
        mycursor.execute(query)
        print("Database created")
    except Error as err:
        print(f"The error '{err}' occurred")

class Books:
    def __init__(self,name,author,copies):
        self.name = name
        self.author = author
        self.status = False
        self.copies = copies
        self.issuedate = None
        self.returndate = None
    def add_copies(self,n):
        self.copies+=n
    def set_status(self,status):
        self.status = status
class library:

    def __init__(self):
        self.__librarianAccount={'admin':'admin'}
        self.db = connection_creator("localhost" ,"root" ,"imranfrommoradabad231321","lmsDBMS")
        self.mycursor = self.db.cursor(buffered=True)
        self.displayTables
        self.Id = None
        # create_database_query = "CREATE DATABASE lmsDBMS"
        # create_database(self.db, create_database_query)
        # self.mycursor.execute(f"CREATE DATABASE lmsDBMS")
        # print(self.db)
        # self.createusertable()
        # self.createtransactionTable()
        
        # self.books = {}
        self.mainMenu()
    def createbooksTable(self):
        query=  """
                CREATE TABLE Books (
                    BookID INT AUTO_INCREMENT PRIMARY KEY,
                    BookName VARCHAR(100),
                    BookAuthor VARCHAR(100),
                    BookStatus BOOLEAN,
                    TotalCopies INT,
                    AvailableCopies INT
                )
                """
        self.mycursor.execute(query)
        self.db.commit()
    def createusertable(self):
        query=  """
                CREATE TABLE Users (
                    UserID INT AUTO_INCREMENT PRIMARY KEY,
                    UserName VARCHAR(100),
                    UserAddress VARCHAR(100),
                    blockStatus BOOLEAN
                )
                """
        self.mycursor.execute(query)
        self.db.commit()
    def createtransactionTable(self):
        create_table_query = """
            CREATE TABLE transactions (
                transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                userID INT,
                bookID INT,
                issue_date DATE,
                return_date DATE,
                return_status VARCHAR(20),
                FOREIGN KEY (userID) REFERENCES users(userID),
                FOREIGN KEY (bookID) REFERENCES books(bookID)
            )
        """

        # Execute the query
        self.mycursor.execute(create_table_query)

        # Commit the changes
        self.db.commit()   
    #func to identify librarian or user 
    def loginInfo(self):
        print('Who are you?\n1.Librarian   2.LMS user  3.Quit' )
        return input('Enter (1,2 or 3)\n')
    def displayTables(self):
        show_tables_query = "SHOW TABLES;"
        self.mycursor.execute(show_tables_query)
        tables = self.mycursor.fetchall()
        for table in tables:
            print(table[0])
            describetable = f"DESCRIBE {table[0]}"
            self.mycursor.execute(describetable)
            table_description = self.mycursor.fetchall()
            for column_info in table_description:
                print(column_info)
            
    def mainMenu(self):
        print('Welcome to Namal Library System')
        # self.createbooksTable()
        self.displayTables()
        self.DisplayData('books')
        while True:
            ques = self.loginInfo()
            if ques=='1':
                login = self.librarian_login()
                if login:
                    self.LibrarianMenu()
                else:
                    print('Incorrect Credentials')
            elif ques== '2':
                while self.UserPage():

                    pass
            elif ques =='3':
                break
            else:
                print('Enter correct Number please')
    #librarian login
    def librarian_login(self):
        while True:
            username = input('Enter Your username:')
            password = input('Enter Your Password:')
            if username in self.__librarianAccount and self.__librarianAccount[username]==password:
                print('Access granted')
                return True
            else:
                print('Access Denied')
                relogin= input('Want to login again?(y/n)')
                if relogin=='y':
                    continue
                else:
                    return False
    #Librarian functions ADD_book,Delete_book
    def LibrarianMenu(self):
        print('Welcome to LMS')
        print('Type followin number to perform respective actions:')
        print('1.Add Book')
        task = input()
        if task=='1':
            self.AddBook()
        elif task=='2':
            self.DeleteBook()
    def DisplayData(self,table):
        select_query = f"SELECT * FROM {table}"

        self.mycursor.execute(select_query)
        rows = self.mycursor.fetchall()
        for row in rows:
            print(row)
    def AddBook(self):
        try:
            bookname = input('Enter book Name: ')
            bookauthor = input('Enter Author  Name:')
            try:
                copies = int(input('how many copies are you adding?'))
            except ValueError:
                raise ValueError('Incorrect number of copies')
            AddBookQuery = """
            INSERT INTO books (BookName, BookAuthor, BookStatus, TotalCopies, AvailableCopies)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (bookname, bookauthor, False, copies, copies)
            self.mycursor.execute(AddBookQuery, values)
            self.db.commit()
            print('Book is Successfully added.')
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    def AreAvailableAndTotalcopiesEqual(self,bookname,bookauthor):
        select_query = """
            SELECT TotalCopies, AvailableCopies 
            FROM books 
            WHERE BookName = %s 
            AND BookAuthor = %s
        """
        values = (bookname, bookauthor)
        self.mycursor.execute(select_query, values)
        copies = self.mycursor.fetchone()
        return copies[0]==copies[1],copies[0]
    def DeleteBook(self):
        try:
            bookname = input('Enter book Name: ')
            bookauthor = input('Enter Author  Name:')
            try:
                copies = input('how many copies do you want to delete(type A to delete All copies)?')
            except ValueError:
                raise ValueError('Incorrect number of copies')
            if copies =='A':
                DeleteBookQuery = """
                DELETE FROM books 
                WHERE BookName = %s 
                AND BookAuthor = %s
                """
                values = (bookname, bookauthor)
                self.mycursor.execute(DeleteBookQuery, values)
                self.db.commit()
                print('Successfully Deleted.')
            else:
                check,Totalcopies = self.AreAvailableAndTotalcopiesEqual()
                if check():
                    updateQuery = """
                    UPDATE books 
                    SET TotalCopies = %s, AvailableCopies = %s 
                    WHERE BookName = %s 
                    AND BookAuthor = %s
                """
                    values = (Totalcopies, Totalcopies, bookname, bookauthor)
                    self.mycursor.execute(updateQuery, values)
                    self.db.commit()
                    print('Successfully Deleted.')
                else:
                    print(f'Kindly recieve all issued books from users,to modify copies of {bookname} Book')
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    def UserPage(self):
        while True:
            task = input('1.Login\t\t2.SignUp\t\t3.Quit')
            if task =='1':
                self.Userlogin()
            elif task=='2':
                self.UserSignUp()
            elif task =='3':
                break
            else:
                print('Enter Correct Number:)')
    def Userlogin(self):
            while True:
                username = input('Enter Your username:') 
                password = input('Enter Your Password:')
                self.userId=self.UserloginCheck(username,password)
                if self.userId==None:
                    print('Incorrect Credentials:)')
                    if input('Loin aain?(y/n)')=='y':
                        pass
                    else:
                        break
                else:
                    print('Login Successfull')
                    self.UserMenu()
    def AddUserInDBMS(self,username,useraddress,blockstatus,password):
        try : 
            insert_query = """
                INSERT INTO Users (UserName, UserAddress, blockStatus,Password)
                VALUES (%s, %s, %s,%s)
            """
            values = (username, useraddress, blockstatus,password)
            self.mycursor.execute(insert_query, values)
            self.db.commit()
            print('User added successfully.')

        except mysql.connector.Error as err:
            print(f"Error: {err}")
    def Usernamecheck(self,username):
        try:
            select_query = """
                SELECT COUNT(*) 
                FROM Users 
                WHERE UserName = %s
            """
            values = (username,)
            self.mycursor.execute(select_query, values)
            user_count = self.mycursor.fetchone()
            return user_count[0] > 0

        except mysql.connector.Error as err:
            print(f"Error: {err}")
        return None
    def UserSignUp(self):
        while True:
            username = input('Enter your Username:')
            if self.Usernamecheck(username):
                print('Username Already Exist!')
            else:
                break
        password = input('Enter your Password:')
        location = input('Enter your Location:')
        self.AddUserInDBMS(username,location,False,password)
    def UserloginCheck(self,username,password):
        try:
            select_query = """
                SELECT UserID
                FROM Users
                WHERE UserName = %s AND Password = %s
            """
            values = (username, password)
            self.mycursor.execute(select_query, values)
            user_id = self.mycursor.fetchone()
            return user_id[0] if user_id else None

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
    def UserMenu(self):
        while True:
            task = input('Enter following Number to perform following Tasks\n1.searc Book\n2.Return Book')
            if task =='1':
                self.SearchBook()
            elif task=='2':
                self.ReturnBook()
            else:
                print('Enter correct Number')
    def SearchBook(self):
        try:
            keyword= input("Enter Name of Book or Author:")
            search_query = """
                SELECT *
                FROM books
                WHERE BookName LIKE %s OR BookAuthor LIKE %s
            """
            keyword = f"%{keyword}%" 
            values = (keyword, keyword)

            self.mycursor.execute(search_query, values)
            books = self.mycursor.fetchall()
            if books:
                for book in books:
                    print("Name of Book :",book[1])
                    print("Name of Author :",book[2])
                    print("Available copies :",book[5])
                    issue = input("Want to issue tis book?(y/n)")
                    if issue=="y":
                        self.IssueBook(book[0])

            else:
                print('No matching books found.')

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
    def IssueBook(self,bookid):
        try:
            today = datetime.today()
            return_date = today + datetime.timedelta(days=5)

            insert_query = """
                INSERT INTO transactions (userID, bookID, issue_date, return_date, return_status)
                VALUES (%s, %s, %s, %s, %s)
            """

            values = (self.userId, bookid,today, return_date, False)
            self.mycursor.execute(insert_query, values)
            self.db.commit()

            print('Book Issue successfully.')

        except mysql.connector.Error as err:
            print(f"Error: {err}")
    def ReturnBook(self,bookid):
        try:
            select_query = """
                SELECT *
                FROM transactions
                WHERE userID = %s AND bookID = %s
            """
            values = (self.userId,bookid)
            self.mycursor.execute(select_query, values)

            transaction_details = self.mycursor.fetchone()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        if transaction_details:
            print(f'Transaction Details: {transaction_details}')
            alter_query = """
                ALTER TABLE transactions
                MODIFY COLUMN return_status BOOLEAN DEFAULT TRUE
            """
            self.mycursor.execute(alter_query)              
            self.db.commit()

            print('Book returned successfully.')

        else:
            print('No matching transaction found.')
library()