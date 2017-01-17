from flask import Flask, render_template,request,flash,redirect,url_for, Markup
from collections import defaultdict
from datetime import datetime as dt
import mysql.connector as mariadb
import datetime
import random

app = Flask(__name__)


@app.route("/", methods=['GET'])
def jobs():

	curDate = datetime.date.today()
	mariadb_connection = mariadb.connect(user='stats', password='OGE1MTZkYzNhYWI', database='ninja_jobs')
	cursor = mariadb_connection.cursor(buffered=True, dictionary=True)

	#Today
	cursor.execute('''SELECT name, job FROM watchdog_jobs WHERE date = "%s"ORDER BY job;'''%(curDate))
	phonetoday = cursor.fetchall()
	phonetodayString = ''
	for nlist in phonetoday:
		phonetodayString += "<tr><td>" + str(nlist['name']) + "</td><td>" + str(nlist['job'])+ "</td></tr>"


        #Pie Charts
	## Jobs
	cursor.execute('''SELECT name, count(job) AS total FROM watchdog_jobs WHERE job = 'phones' GROUP BY name ORDER BY total DESC''')
	phonearray = cursor.fetchall()
	phoneString=''
	for plist in phonearray:
		phoneString += "{ name: '" + str(plist['name']) + "', y: " + str(plist['total']) + "},"

        cursor.execute('''SELECT name, count(job) AS total FROM watchdog_jobs WHERE job = 'tickets' GROUP BY name ORDER BY total DESC''')
        ticketarray = cursor.fetchall()
        ticketString=''
        for tlist in ticketarray:
                ticketString += "{ name: '" + str(tlist['name']) + "', y: " + str(tlist['total']) + "},"

        cursor.execute('''SELECT name, count(job) AS total FROM watchdog_jobs WHERE job = 'alerts' GROUP BY name ORDER BY total DESC''')
        alertarray = cursor.fetchall()
        alertString=''
        for alist in alertarray:
                alertString += "{ name: '" + str(alist['name']) + "', y: " + str(alist['total']) + "},"


        cursor.execute('''SELECT name, count(job) AS total FROM watchdog_jobs WHERE job = 'chats' GROUP BY name ORDER BY total DESC''')
        chatarray = cursor.fetchall()
        chatString=''
        for clist in chatarray:
                chatString += "{ name: '" + str(clist['name']) + "', y: " + str(clist['total']) + "},"



	## Individuals

	watchdogs = ['Carlos S', 'Grace T', 'Jim C', 'Joe S', 'Lee N', 'Marcos T', 'Matt V', 'Pam L', 'Tim M', 'Uwe N']
	fulljobarray = []

	for name in watchdogs:

	        cursor.execute('''SELECT job, count(job) AS total FROM watchdog_jobs WHERE name="%s" GROUP BY job order by job;'''%(name))
	        jobarray = cursor.fetchall()
		

		PieString=''
		for jlist in jobarray:
			PieString += "{ name: '" + str(jlist['job']) + "', y: " + str(jlist['total']) + "},"
		fulljobarray.append([name, PieString])


	print fulljobarray
	for array in fulljobarray:
		print array
		if array[0] == "Carlos S":
			CarlosSPie = array[1]
                elif array[0] == "Grace T":
                        GraceTPie = array[1]
                elif array[0] == "Jim C":
                        JimCPie = array[1]
                elif array[0] == "Joe S":
                        JoeSPie = array[1]
                elif array[0] == "Lee N":
                        LeeNPie = array[1]
                elif array[0] == "Marcos T":
                        MarcosTPie = array[1]
                elif array[0] == "Matt V":
                        MattVPie = array[1]
                elif array[0] == "Pam L":
                        PamLPie = array[1]
                elif array[0] == "Tim M":
                        TimMPie = array[1]
                elif array[0] == "Uwe N":
                        UweNPie = array[1]


	return render_template('jobs.html',PhoneToday = phonetodayString, PhonePie = phoneString, ChatPie = chatString, TicketPie = ticketString, AlertPie = alertString, CarlosSPie = CarlosSPie, GraceTPie = GraceTPie, JimCPie = JimCPie, JoeSPie = JoeSPie, LeeNPie = LeeNPie, MarcosTPie = MarcosTPie, MattVPie = MattVPie, PamLPie = PamLPie, TimMPie = TimMPie, UweNPie = UweNPie)


@app.route("/about", methods=['GET'])
def about():
	return render_template('about.html')


if __name__ == "__main__":
	app.run(debug=True,port=5002)
	app.run()
