import hashlib
import random
import http.server 
import socketserver
import webbrowser


allUsers = {}
salt = "Test#120"

class User:
    count = 0 
    def __init__(self, name, surname, email, password):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.count=self.count+1
        
    def printinfo(self):
        return '[ '+self.name +' , '+ self.surname + ' , '+ self.email+' ]'
        
def hashpass(password):
    return hashlib.sha256(password.encode()).hexdigest()

adminUser = User("Project","Admin","xyz@reddit.com",hashpass("x123"+salt))
allUsers["Admin123"] = adminUser


def newUser():
    print("\n")
    name = str(input('Enter Your First Name : '))
    surname = str(input('Enter Your Surname : '))
    email = str(input('Enter Your Email : '))
    username = name+str(random.randint(1,100))+surname
    password = str(input('Enter Your Password : '))
    conf_password = str(input('Confirm Your Password : '))
    
    if (password == conf_password):
        allUsers[username] = User(name,surname,email, hashpass(password+salt))
        print("\nRegistered Successfully!!\n\n***Please Save Your Username For Future Use!!***\n\nUsername = "+username+"\n\n")
    else:
        print("Passwords DO NOT MATCH")
        
def getAllUsers():
    try:
        print("\n\nUsername  |  Details  [first-name, surname, email]")
        for key,value in allUsers.items():
            print(key," | ", value.printinfo())
        print("\n\n")
    except ValueError:
        print(ValueError)
        
PORT = 7000

class CustomHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        self.url = self.path.strip('/')
        self.response_headers = [('Content-type', 'text/html')]

        # Render HTML
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = self.render_html("index.html")
        self.wfile.write(html.encode())

    def render_html(self, template_path):
        with open(template_path, 'r') as f:
            html = f.read()
            return html
        
def run():
    Handler = CustomHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("serving at port", PORT)
    webbrowser.open('http://localhost:{}'.format(PORT))
    httpd.serve_forever()

    
def login():
    print("\n")
    userName = input('Username : ')
    passWord = input('Password : ')
    if userName in allUsers and hashpass(passWord+salt)==allUsers[userName].password:
        if userName == "Admin123":
            print("Press 1 : To Access Data of all the users\nPress 2 : To Load the special page\nPress 3 : Return to Main Menu")
            choice = int(input('Enter Your Choice : '))
            if choice==1:
                getAllUsers()
            elif choice==2:
                run()
            elif choice==3:
                return
            else:
                print("INVALID CHOICE ENTERED --> REDIRECTING TO MAIN MENU")
                return
        else:
            run()
    else:
        print('Incorrect Username or Password!')
        


choice = 5
cont = ''
while cont!=0 and choice!=3:
    print('\nPress 1: To Login\nPress 2: To Register\nPress 3: To Exit')
    try:
        choice = int(input("\nEnter Your Choice : "))
    except ValueError:
        print('Please Enter an Integer/Number in the input!!')
        continue
    if choice==1:
        login()
    elif choice==2:
        newUser()
    elif choice==3:
        print("Thanks for using this app!")
        break
    else:
        print("INVALID CHOICE")
    cont = int(input("\nWish to continue further (Yes=1/No=0) : "))