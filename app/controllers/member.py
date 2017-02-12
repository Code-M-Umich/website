from flask import render_template, Blueprint, request
from database import openDBConnection, closeDBConnection, DBCommit
from app import util

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
             "admin": i[1],
             "joined": i[2]
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


# adds user to database if they don't exist
def add_user(uniqname):
    conn,cur = openDBConnection()
    query = "INSERT IGNORE INTO users (uniqname) " \
                    "VALUES (\"%s\")" % (uniqname)
    cur.execute(query)
    DBCommit(conn)
    closeDBConnection(conn,cur)


# Returns true if a given user is an admin, false if not
def get_admin(uniqname):
    isAdmin = True
    conn,cur = openDBConnection()
    query = "SELECT admin from users " \
            "WHERE uniqname = \"%s\" LIMIT 1" % uniqname
    cur.execute(query)
    entries = cur.fetchone()
    if not entries:
        isAdmin = False
    closeDBConnection(conn,cur)
    return isAdmin


def set_admin(uniqname, admin):
    conn,cur = openDBConnection()
    query = "UPDATE users" \
            "SET admin= %d" \
            "WHERE uniqname='%s'" % (admin, uniqname) 
    cur.execute(query)
    DBCommit(conn)
    closeDBConnection(conn,cur)
    return True
    #not admin by default
    

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
    user = util.get_current_user()
    #If the user is an admin, give them admin page
    if get_admin(user):
        options = {
            'users' : get_members()
        }
        return render_template("admin.html", **options)
    else:
        add_user(user)
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
            'compliment' : util.randomCompliment()
        } 

        return render_template("member.html", **options)


@member.route('/_member_update_admin', methods=['POST'])
def update_user_route():
    user = util.get_current_user()
    if get_admin(user):
        uniqname = str(request.args.get('uniqname'))
        state = str(request.args.get('state'))
        return set_admin(uniqname, state)

#make users global, so that when sorting or removing or whatever, you don't
#have to reload the whole users database again.
