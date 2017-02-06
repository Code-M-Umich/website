from flask import render_template, Blueprint, request
from database import openDBConnection, closeDBConnection, DBCommit
from util import randomCompliment

member = Blueprint('member', __name__, template_folder='views')

def get_members():
    conn,cur = openDBConnection()
    query = "SELECT * FROM users" 
    cur.execute(query)
    results = cur.fetchall()
    entries = []
    for i in results:
        entries.append( 
            {"uniqname": i[0],
             "joined": i[1],
             "admin": i[2]
            }
        )
    closeDBConnection(conn,cur)
    return entries

# returns all the peope who attended an event 
def get_event_attendance(eventID):
    cur = openDBConnection()
    query = "SELECT uniqname FROM codeM.attendance WHERE eventID=\"%d\";" % eventID
    cur.execute(query)
    entries = cur.fetchall()
    closeDBConnection()
    return entries

def add_attendence(uniqname, eventID):
    cur = openDBConnection()
    query = "INSERT INTO attendance (uniqname, event) " \
            "VALUES (\"%s\",\"%d\")" % (uniqname, eventID)
    cur.execute(query)
    DBCommit()
    closeDBConnection()

def get_points(uniqname):
    conn, cur = openDBConnection()
    query = "SELECT SUM(events.points) from events " \
    "JOIN attendance ON events.eventid = attendance.eventID " \
    "WHERE attendance.uniqname = \"%s\";" % uniqname
    cur.execute(query)
    entries = cur.fetchone()
    points = entries[0]
    if points == None:
        points = 0
    closeDBConnection(conn, cur)
    return points

# Returns true if a given user is an admin
def get_admin(uniqname):
    conn,cur = openDBConnection()
    query = "SELECT admin from users " \
            "WHERE uniqname = \"%s\" LIMIT 1" % uniqname
    cur.execute(query)
    entries = cur.fetchone()
    if len(entries):
        closeDBConnection(conn,cur)
        #check whether received true or false

        return entries[0]
    else:
        query = "INSERT INTO users (uniqname) " \
                "VALUES (\"%s\")" % (uniqname)
        cur.execute(query)
        DBCommit(conn)
        closeDBConnection(conn,cur)
        #not admin by default
        return False
    
    return True

# Checks to see if the user entered accessCode is correct for a given event
def validateAttendance(uniqname, userEnteredCode, eventID):
    cur = openDBConnection()
    query = "SELECT accessCode FROM events WHERE eventID=\"%d\" AND open=1 LIMIT 1" % (eventID)
    cur.execute(query)
    accessCode = cur.fetchone()
    closeDBConnection()
    if userEnteredCode == accessCode:
        add_attendence(uniqname, eventID)
        return True
    else:
         return False

# returns all the details about an event
def get_event(eventid):
    conn,cur = openDBConnection()
    query = "SELECT * FROM events WHERE eventID=\"%d\";" % (eventID)
    cur.execute(query)
    entry = cur.fetchone()
    closeDBConnection(conn,cur)
    return entry

# Returns all the currently open events
def get_open_events():
    entries = []
    conn,cur = openDBConnection()
    query = "SELECT eventID, name FROM events WHERE open=1"
    cur.execute(query)
    results = cur.fetchall()
    for i in results:
        entries.append( [i[0],i[1]] )
    closeDBConnection(conn,cur)
    return entries

@member.route('/member', methods=['GET', 'POST'])
def member_route():
    user = request.environ['REMOTE_USER'] #should always be valid with cosign
    #If the user is an admin, give them admin page
    if get_admin(user):
        options = {
            'users' : get_members()
        }
        return render_template("admin.html", **options)
    else:
        isAuth = False
        didSubmit = False
        
        # Handle event code submission
        if request.method == 'POST' and request.form['eventCode']:
            didSubmit = True
            f = request.form
            eventID= f['eventID']
            if validateAttendance(user, f['eventCode'], eventID):
                isAuth = True
                event = get_event(eventID)
                options['authedEventName'] = event['name']

        options = {
            'user' : user,
            'events' : get_open_events(),
            'didSubmitCode' : didSubmit,
            'isAuth' : isAuth,
            'points' : get_points(user),
            'compliment' : randomCompliment()
        } 

        return render_template("member.html", **options)
