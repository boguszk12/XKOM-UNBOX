import requests,time,random
from threading import Thread
import requests
from os import system
import xkom
import utils


succ = 0
errors = 0

api_key = '' #mailslurp api_key

proxy_string = '' #user:pass@ip:port


if proxy_string != '':
    if 'http' not in proxy_string:
        proxy_string = 'http://'+proxy_string



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


def Checker(u):
    try:
        handler = Handler(api_key,u[2],u[3],u[0],u[0].split('@')[0],u[1],proxy_string)
        handler.Roll()
    except Exception as exc:return exc
    return True



def Creator():
    try:
        handler = Handler(api_key,proxystring=proxy_string)
        handler.Create()
        handler.Roll()
    except Exception as exc:return exc
    return True

def Controller():
    global users_list
    global succ
    global errors
    while len(users_list) > 0:
        USER = users_list.pop(0)


        match cs:
            case 1:
                result = Creator()
            case 2:
                result = Checker(USER)

        
        if result == True:
            succ+=1
        else:
            errors+=1
            print(result)

 
def runner(): 
    global succ
    global errors
    global users_list
    total_users = len(users_list)
    while len(users_list)>0: 
        time.sleep(1) 
        log = f"Success: {succ}  Errors: {errors}  Remaining: {len(users_list)}/{total_users}"
        system("title " + log)
        
               
       
 
def main(threads):

    thread_list = []

    thread_list.append(Thread(target=runner))
    thread_list[0].start()

    for i in range(0,threads):
        thread_list.append(Thread(target=Controller))
        thread_list[-1].start()
        time.sleep(0.05)

    for x in thread_list:
        x.join()




 




cs, amount = utils.welcome()

th = int(input('Input thread amount:\n - '))



if cs == 2:
    with open('files/users.txt','r',encoding='utf-8') as raw: users_list = [t.strip().split(':') for t in raw.readlines()]
    if len(users_list) == 0:
        print('No accs found in files/users.txt')
        quit()
else:
    users_list = list(range(amount))








main(th)

print('FINISHED')
input()     
