import xkom
import utils

class Handler:
    def __init__(self,api_key,fn=None,ln=None,email=None,emailid=None,passw=None,proxystring=None) -> None:
        self.User = xkom.Identity(fn,ln,email,emailid,passw,proxystring,api_key)


    def Create(self):
        #User.ProxyTest()
        self.User.createAccount()
        print(f"Creating account for {self.User.Email}")
        self.User.activateNewsletter()
        print(f"Activating for {self.User.Email}")
        self.User.Consent()
        print(f"Consent made for {self.User.Email}")


    def Roll(self):
        try:self.access_token
        except:self.User.login()
        for i in range(1,4):
            try:self.User.roll(i)
            except Exception as exc:
                print(exc)

api_key = 'X' #mailslurp api_key

cs, amount = utils.welcome()

if cs == 2:
    with open('files/users.txt','r',encoding='utf-8') as raw: users = [t.strip().split(':') for t in raw.readlines()]
    if len(users) == 0:print('No accs found in files/users.txt')
    for u in users:
        handler = Handler(api_key,u[2],u[3],u[0],u[0].split('@')[0],u[1])
        handler.Roll()

if cs == 1:
    for i in range(0,amount):
        handler = Handler(api_key)
        handler.Create()
        handler.Roll()

        
