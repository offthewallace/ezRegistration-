import re, mechanize, time 
from mechanize import Browser
import getpass

br = Browser()
registerTime = 1522580400 #Wednesday, April 16th, 2014, 7:00 am

# Ignore robots.txt
br.set_handle_robots( False )
# Google demands a user-agent that isn't a robot
br.addheaders = [('User-agent', 'Chrome')]

# Navigates to BannerWeb HomePage
br.open( "https://auth.richmond.edu/cas/login?service=https%3A%2F%2Fsso.richmond.edu%3A443%2Fssomanager%2Fc%2FSSB" )

print "Current time: " + time.ctime()
print "Registration time: " + time.ctime(registerTime)
print "****Welcome to regapp by WH****"

#Gets all user information needed for registration
print "User ID: "
ID = raw_input()
PIN = getpass.getpass(prompt = 'PIN: ')
print "Number of CRN's registering: "
numCrn = int(raw_input())
slot = 0
CRNs = []
while numCrn != 0:
    print "CRN #" + str(slot + 1) + ":"
    CRNs.append(raw_input())
    numCrn -= 1
    slot += 1

#sleeps till 6:55 am before longing in
print "Sleeping until registration..."
time.sleep(registerTime - 300 - time.time())

# Selects and fills in login form
br.select_form( 'loginform' )
br.form[ 'sid' ] = ID
#print "PIN: "
br.form [ 'PIN' ] = PIN

# Submits form
br.submit()

#Links that lead to registration page
link1 = 'https://ssb.middlebury.edu/PNTR/twbkwbis.P_GenMenu?name=bmenu.P_StuMainMnu'
link2 = 'https://ssb.middlebury.edu/PNTR/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu'
link3 = 'https://ssb.middlebury.edu/PNTR/bwskfreg.P_AltPin'

#Navigates through links above
br.open(link1)
br.open(link2)
br.open(link3)

#Chooses registration period 
br.select_form(nr = 1)
br.form ['term_in'] = ["201490",]
br.submit()

#Sleeps untill 7:00 am
time.sleep(1397646000 - time.time())

#Opens Alternate PIN page if not there already
def altID():
    if br.geturl() != link3:
        br.open(link3)
        br.select_form(nr = 1)
        br.form ['pin'] = altID
        br.submit()
        print br.geturl()
        altIDCheck()
    else:
        altIDCheck()
#checks success
def altIDCheck():
    if br.geturl() == 'https://ssb.middlebury.edu/PNTR/bwskfreg.P_CheckAltPin':
        print "Incorrect PIN. Enter again: "
        altID()
    else:
        br.select_form(nr = 1)

        index = 0
        for control in br.form.controls:
            if control.type == "text":
                if index < len(CRNs):
                    control.value = CRNs[index]
                    index += 1
        
        resp = br.submit()
        
        # Print success of registration
        content = resp.get_data()
        print "Your classes have been succesfully registered"
        print time.ctime()
        
altID()
        
