import pyodbc 
import datetime
import json

server = 'localhost' 
database = 'IshaniDB' 
username = 'admin' 
password = 'admin' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password, autocommit=True)

cursor = cnxn.cursor()

#Initiallise Database Tables
def initialliseTables():

  #Drop Foreign Keys
  cursor.execute('''EXEC sp_msforeachtable "ALTER TABLE ? NOCHECK CONSTRAINT all"''')

  #Drop all tables
  cursor.execute('''EXEC sp_MSforeachtable @command1 = "DROP TABLE ?"''')

  #Insert Tables
  cursor.execute('''
    CREATE TABLE Users (
        UserID int NOT NULL IDENTITY(1,1),
        Name varchar(255) NOT NULL,
        PRIMARY KEY (UserID)
    );
    ''')
  
  cursor.execute('''
      INSERT INTO Users(Name) VALUES('Dashmesh');
      INSERT INTO Users(Name) VALUES('Ishani');
      INSERT INTO Users(Name) VALUES('Chinmay');
    ''')
    
  cursor.execute('''
    CREATE TABLE Tickets (
        TicketID int NOT NULL IDENTITY(1,1),
        TicketNumber varchar(255) NOT NULL,
        PRIMARY KEY (TicketID)
    );
    ''')

  cursor.execute('''
    CREATE TABLE Events (
        EventID int NOT NULL IDENTITY(1,1),
        Reward varchar(255) NOT NULL,
        EventDatetime datetime NOT NULL,
        PRIMARY KEY (EventID)
    );
    ''')

  cursor.execute('''
    INSERT INTO Events(Reward,EventDatetime) VALUES('Bike',CAST(CONVERT(VARCHAR(20), GETDATE()-1, 112) + ' 08:00:00' AS DATETIME));
    INSERT INTO Events(Reward,EventDatetime) VALUES('Car',CAST(CONVERT(VARCHAR(20), GETDATE(), 112) + ' 08:00:00' AS DATETIME));
    INSERT INTO Events(Reward,EventDatetime) VALUES('Fan',CAST(CONVERT(VARCHAR(20), GETDATE()+1, 112) + ' 08:00:00' AS DATETIME));
    INSERT INTO Events(Reward,EventDatetime) VALUES('Phone',CAST(CONVERT(VARCHAR(20), GETDATE()+2, 112) + ' 08:00:00' AS DATETIME));
    INSERT INTO Events(Reward,EventDatetime) VALUES('Computer',CAST(CONVERT(VARCHAR(20), GETDATE()+3, 112) + ' 08:00:00' AS DATETIME));

  ''')

  cursor.execute('''
    CREATE TABLE User_Tickets (
        User_TicketID int NOT NULL IDENTITY(1,1),
        UserID int NOT NULL ,
        TicketID int NOT NULL ,
        PurchaseDatetime datetime NOT NULL,
        PRIMARY KEY (User_TicketID)
    );
    ''')

  cursor.execute('''
    CREATE TABLE Participants (
        ParticipantID int NOT NULL IDENTITY(1,1),
        User_TicketID int NOT NULL ,
        EventID int NOT NULL ,
        ParticipationDatetime datetime NOT NULL,
        PRIMARY KEY (ParticipantID)
    );
    ''')

  cursor.execute('''
    CREATE TABLE Winners (
        WinnerID int NOT NULL IDENTITY(1,1),
        ParticipantID int NOT NULL ,
        EventID int NOT NULL ,
        WinnerDatetime datetime NOT NULL,
        PRIMARY KEY (WinnerID)
    );
    ''')

initialliseTables()
