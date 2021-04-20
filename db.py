import pyodbc 
import datetime
import json

server = 'localhost' 
database = 'IshaniDB' 
username = 'admin' 
password = 'admin' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password, autocommit=True)

cursor = cnxn.cursor()

#For serialization of datetime object in json
def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

def addTicket(ticket_number):
  cursor.execute('''  INSERT INTO Tickets(TicketNumber) VALUES(?) ''',ticket_number)
  id =  cursor.execute('''SELECT @@IDENTITY''').fetchone()[0]
  return id

def addUser_Ticket(userid,ticketid):
  cursor.execute('''  INSERT INTO User_Tickets(UserID,TicketID,PurchaseDatetime) VALUES(?,?,?) ''',userid,ticketid,datetime.datetime.now())
  id =  cursor.execute('''SELECT @@IDENTITY''').fetchone()[0]
  return id


def getNextEventJson():
  cursor.execute('''SELECT TOP 1 * FROM Events WHERE ?<EventDatetime ORDER BY EventDatetime''',datetime.datetime.now())
  
  row_headers=[x[0] for x in cursor.description] #this will extract row headers
  rv = cursor.fetchall()
  json_data=[]
  for result in rv:
      json_data.append(dict(zip(row_headers,result)))
  return json.dumps(json_data, default=datetime_handler)


def getTicketIDByValue(ticket):
  cursor.execute('''SELECT TicketID FROM Tickets WHERE TicketNumber=?''',ticket)
  res=cursor.fetchone()
  if(res==None):
    return None
  return res[0]

def isEventValid(eventid):
  cursor.execute('''SELECT * FROM Events WHERE EventID=? and EventDatetime>?''',eventid,datetime.datetime.now())
  res=cursor.fetchone()
  if(res==None):
    return False
  return True

def isAlreadyParticipated(userid,eventid):
  cursor.execute('''SELECT * FROM Participants INNER JOIN User_Tickets ON Participants.User_TicketID=User_Tickets.User_TicketID WHERE UserID=? AND EventID=?''',userid,eventid)
  res=cursor.fetchone()
  if(res==None):
    return False
  return True

def getUserTicket(userid,ticket_id):
  cursor.execute('''SELECT * FROM User_Tickets WHERE UserID=? AND TicketID=?''',userid,ticket_id)
  res=cursor.fetchone()
  if(res==None):
    return None
  return res[0]


def participateUser(user_ticket_id,eventid):
  cursor.execute('''  INSERT INTO Participants(User_TicketID,EventID,ParticipationDatetime) VALUES(?,?,?) ''',user_ticket_id,eventid,datetime.datetime.now())
  id =  cursor.execute('''SELECT @@IDENTITY''').fetchone()[0]
  return id

def isWinnerAlreadyDeclared(eventid):
  cursor.execute('''SELECT * FROM Winners WHERE EventID=?''',eventid)
  res=cursor.fetchone()
  if(res==None):
    return False
  return True

def getWinner(eventid):
  #Random Winnder SQL logic - https://stackoverflow.com/questions/19412/how-to-request-a-random-row-in-sql
  cursor.execute('''SELECT TOP 1 ParticipantID FROM Participants WHERE EventID=? ORDER BY NEWID() ''',eventid)
  res =  cursor.fetchone()
  if(res==None):
    return None
  return res[0]

def getDetailsByParticipantId(participantId):
  cursor.execute('''
    SELECT Name,TicketNumber,Reward
    FROM (Participants INNER JOIN User_Tickets ON Participants.User_TicketID = User_Tickets.User_TicketID
    INNER JOIN Events ON Participants.EventID= Events.EventID )
    INNER JOIN Users ON Users.UserID=User_Tickets.UserID
    INNER JOIN Tickets ON Tickets.TicketID=User_Tickets.TicketID

    WHERE ParticipantID=?
  ''',participantId)

  row_headers=[x[0] for x in cursor.description] #this will extract row headers
  rv = cursor.fetchall()
  json_data=[]
  for result in rv:
      json_data=(dict(zip(row_headers,result)))
  return json_data

def addWinnderDetails(participantId,eventid):
  cursor.execute('''  INSERT INTO Winners(ParticipantID,EventID,WinnerDatetime) VALUES(?,?,?) ''',participantId,eventid,datetime.datetime.now())
  id =  cursor.execute('''SELECT @@IDENTITY''').fetchone()[0]
  return id

def getLastWeekWinners():
  
  cursor.execute(''' Select ParticipantID FROM Winners WHERE WinnerDatetime>= CAST(CONVERT(VARCHAR(20), GETDATE()-7, 112) AS DATETIME) ''')
  winnerParticipantIDs = cursor.fetchall()
  json_data=[]
  for winnerParticipantID in winnerParticipantIDs:
      json_data.append (getDetailsByParticipantId(winnerParticipantID[0]))

  return json.dumps(json_data, default=datetime_handler)
