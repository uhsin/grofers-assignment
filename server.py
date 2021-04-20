from flask import Flask, jsonify,request
import numpy
import json
import random
import db

app = Flask(__name__)

#Error Messages
INPUT_ERROR="Input Error"

@app.route('/', methods = ['GET', 'POST'])
def home():
  return jsonify("Home")

@app.route('/GetRaffleTicket', methods = ['GET'])
def GetRaffleTicket():
  userid= request.args.get('userid')
  if(userid==None):
    return json.dumps({"status":False,"Reason":INPUT_ERROR})

  #Generate Raffle Ticket Value - 12 digit random hexadecimal code
  ticket_number = '%012x' % random.randrange(16**12)
  ticket_id= db.addTicket(ticket_number)
  user_ticket_id= db.addUser_Ticket(userid, ticket_id)
  
  return json.dumps({"ticket_number":ticket_number})

@app.route('/GetNextEvent', methods = ['GET'])
def GetNextEvent():
  
  next_event_json= db.getNextEventJson()
  
  return next_event_json


@app.route('/ParticipateEvent', methods = ['POST'])
def ParticipateEvent():

  userid= request.args.get('userid')
  if(userid==None):
    return json.dumps({"status":False,"Reason":INPUT_ERROR})
  ticket= request.args.get('ticket')
  if(ticket==None):
    return json.dumps({"status":False,"Reason":INPUT_ERROR})
  eventid= request.args.get('eventid')
  if(eventid==None):
    return json.dumps({"status":False,"Reason":INPUT_ERROR})

  ticket_id= db.getTicketIDByValue(ticket)
  if(ticket_id==None):
    return json.dumps({"status":False,"Reason":"Ticket Not Valid"})

  eventValid= db.isEventValid(eventid)
  if(eventValid==False):
    return json.dumps({"status":False,"Reason":"Event Not Valid"})

  user_ticket_id= db.getUserTicket(userid,ticket_id)
  if(user_ticket_id==None):
    return json.dumps({"status":False,"Reason":"User Did Not Purchase Ticket"})

  isAlreadyParticipated= db.isAlreadyParticipated(userid,eventid)
  if(isAlreadyParticipated==True):
    return json.dumps({"status":False,"Reason":"Already Participated"})

  db.participateUser(user_ticket_id,eventid)
  return json.dumps({"status":True,"Reason":"Participated"})

@app.route('/GetEventWinner', methods = ['GET'])
def GetEventWinner():


  eventid= request.args.get('eventid')
  if(eventid==None):
    return json.dumps({"status":False,"Reason":INPUT_ERROR})

  if(db.isWinnerAlreadyDeclared(eventid)):
    return json.dumps({"status":False,"Reason":"Winner Already Declared"})

  participantId= db.getWinner(eventid)
  if(participantId==None):
    return json.dumps({"status":False,"Reason":"No Participants"})

  db.addWinnderDetails(participantId,eventid)

  return db.getDetailsByParticipantId(participantId)


@app.route('/GetLastWeekWinners', methods = ['GET'])
def GetLastWeekWinners():
  return db.getLastWeekWinners()

app.run( debug=True)