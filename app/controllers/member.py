from flask import render_template, Blueprint, request, jsonify
from database import openDBConnection, closeDBConnection, DBCommit
from app import util

member = Blueprint('member', __name__, template_folder='views')

tiers = [
    {
        "name" : "tier1",
        "rewards" : ["Free Movie Tickets", "Water Bottle"],
        "pointReq" : 20
    },
    {
        "name" : "tier2",
        "rewards" : ["Resume Book Access", "Exclusive Corporate Events", "T-shirt"],
        "pointReq" : 12
    },
    {
        "name" : "tier3",
        "rewards" : ["Drawstring Bag", "Company Swag", "Member-only Social Events"],
        "pointReq" : 6
    },
    {
        "name" : "tier4",
        "rewards" : ["Code-M Sticker", "Slack Access", "Piazza Access"],
        "pointReq" : 2
    }
]


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
             "joined": i[2],
             "disabled": i[0]==util.get_current_user() 
            }
        )
    closeDBConnection(conn,cur)
    return entries

# returns all the peope who attended an event 
def get_event_attendance(eventID):
    conn, cur = openDBConnection()
    query = "SELECT uniqname FROM codeM.attendance WHERE eventID=\"%d\";" % eventID
    cur.execute(query)
    entries = cur.fetchall()
    closeDBConnection(conn, cur)
    return entries

def add_attendence(uniqname, eventID):
    eventID = int(eventID)
    conn, cur = openDBConnection()
    query = "INSERT INTO attendance (uniqname, eventID) SELECT '%s', %d FROM DUAL \
        WHERE NOT EXISTS (SELECT * FROM attendance WHERE uniqname='%s' \
        AND eventID=%d) LIMIT 1" % (uniqname, eventID, uniqname, eventID)
    cur.execute(query)
    DBCommit(conn)
    closeDBConnection(conn, cur)

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

def get_awards(points):
    toReturn = []
    for t in tiers:
        if t['pointReq'] <= points:
            toReturn += t['rewards']
    return toReturn

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
    query = "SELECT * from users " \
            "WHERE uniqname = \"%s\" AND admin=True LIMIT 1" % uniqname
    cur.execute(query)
    entries = cur.fetchone()
    if not entries:
        isAdmin = False
        print "\n\n\n\eyterterter"
    closeDBConnection(conn,cur)
    return isAdmin

def set_admin(uniqname, admin):
    conn,cur = openDBConnection()
    query = "UPDATE users " \
            "SET admin= %s " \
            "WHERE uniqname='%s'" % (admin, uniqname) 
    cur.execute(query)
    DBCommit(conn)
    closeDBConnection(conn,cur)
    return True
    #not admin by default

def OpenCloseEvent(eventID, state):
    conn,cur = openDBConnection()
    query = "UPDATE events " \
            "SET open= %s " \
            "WHERE eventID='%s'" % (state, eventID) 
    cur.execute(query)
    DBCommit(conn)
    closeDBConnection(conn,cur)
    return True
    #not admin by default
    
# Checks to see if the user entered accessCode is correct for a given event
def validateAttendance(uniqname, userEnteredCode, eventID):
    conn,cur = openDBConnection()
    query = "SELECT accessCode FROM events WHERE eventID=\"%d\" AND open=1 LIMIT 1" % (int(eventID))
    cur.execute(query)
    accessCode = cur.fetchone()[0]
    closeDBConnection(conn,cur)
    if userEnteredCode == accessCode:
        add_attendence(uniqname, eventID)
        return True
    else:
        return False

# returns all the details about an event
def get_event(eventID):
    conn,cur = openDBConnection()
    query = "SELECT * FROM events WHERE eventID=\"%d\";" % (int(eventID))
    cur.execute(query)
    entry = cur.fetchone()
    closeDBConnection(conn,cur)
    entry = {
            "id": entry[0],
            "name": entry[1],
            "host": entry[2],
            "datetime": entry[3],
            "location": entry[4],
            "description": entry[5],
            "accessCode": entry[6],
            "open": entry[7],
            "points": entry[8],
            "semester": entry[9],
            "lastUpdates": entry[10],
    }
    return entry

# Returns all the events
# if all is False, then it just get's open events
def get_events(all):
    entries = []
    conn,cur = openDBConnection()
    if all:
        query = "SELECT eventID, name, open, accessCode FROM events"
    else:
        query = "SELECT eventID, name, open, accessCode FROM events WHERE open=1"
    cur.execute(query)
    results = cur.fetchall()
    for i in results:
        entries.append( {
            "id": i[0],
            "name": i[1],
            "open": i[2],
            "code": i[3]
        })
    closeDBConnection(conn,cur)
    return entries


@member.route('/member', methods=['GET', 'POST'])
def member_route():
    user = util.get_current_user()
    #If the user is an admin, give them admin page
    if get_admin(user):
        options = {
            'users' : get_members(),
            'events' : get_events(True)
        }
        return render_template("admin.html", **options)
    else:
        add_user(user)
        isAuth = False
        didSubmit = False

        options = {
            'user' : user,
            'events' : get_events(False),
            'didSubmitCode' : didSubmit,
            'isAuth' : isAuth,
            'points' : get_points(user),
            'compliment' : util.randomCompliment(),
            'perks' : get_awards(get_points(user))
        } 
        
        # Handle event code submission
        if request.method == 'POST' and request.form['eventCode']:
            didSubmit = True
            f = request.form
            eventID= f['eventID']
            if validateAttendance(user, f['eventCode'], eventID):
                isAuth = True
                event = get_event(eventID)
                options['authedEventName'] = event['name']

        return render_template("member.html", **options)


@member.route('/_member_update_admin', methods=['GET'])
def update_user_route():
    user = util.get_current_user()
    options = {
            "success": False
    }
    uniqname = str(request.args.get('uniqname'))
    state = str(request.args.get('state')) 
    if user != uniqname and  get_admin(user):
        options['success'] = set_admin(uniqname, state)
    return jsonify( **options )

@member.route('/_open_close_event', methods=['GET'])
def update_event_route():
    user = util.get_current_user()
    options = {
            "success": False
    }
    eventID = int(request.args.get('eventID'))
    state = str(request.args.get('state')) 
    if get_admin(user):
        options['success'] = OpenCloseEvent(eventID, state)
    return jsonify( **options )

#make users global, so that when sorting or removing or whatever, you don't
#have to reload the whole users database again.

