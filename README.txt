Hello, my name is Ishani. I am a CSE undergraduate from IIITD and a budding backend developer. 
This repository contains the backend framework of a Lucky Draw Gaming Service. Users can use this service to get raffle tickets and win prizes. 
I have implemented 5 APIs, which carry out the following functions respectively:
* Allows users to get raffle tickets
* Shows the date, timing and prize of the next lucky draw event
* Allows users to participate in the game only once in a single event. If the user has already registered for the event, it will show “already registered”.
* Lists all the winners of all the events over the last week.
* To compute and announce the winner of the event .
To run these APIs easily use postman. Postman can be installed using the following command:
sudo snap install postman


pip install Flask


TechStack: Flask, MySQL, Numpy, Pyodbc, sql-server
View Engine: Postman 


STEPS TO RUN AND EXECUTE THE PROGRAM-


1. Clone the repository
2. CREATE db
3. Run db_init.py to initialize the database.
4. Run server.py to run API server.
5. APIs could be accessed at http://localhost:5000
6. Postman can be used to test/run the APIs.


In db.py the database creation and updation process is taking place.
* Get winner- provides the winner list of event winners.
* For ticket_id- random hexadecimal value is assigned to the user.