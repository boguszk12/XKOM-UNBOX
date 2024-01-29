import requests
import emailManager
from faker import Faker


def savePrize(roll,Email,Password):
    with open('files/rolls.txt','a+',encoding='utf-8') as raw: raw.write(f'{Email}:{Password}:{roll["Item"]["Name"]}:{roll["Item"]["CatalogPrice"]}:{roll["BoxPrice"]}:{roll["BoxRarity"]["Id"].upper()}\n')
    print(f'{roll["BoxRarity"]["Id"].upper()}:{roll["Item"]["Name"]}:{roll["Item"]["CatalogPrice"]}:{roll["BoxPrice"]}')


class Identity:
    def __init__(self,fn,ln,email,emailid,passw,proxystring,api_key) -> None:
        self.api_key = api_key
        self.client = emailManager.Client(api_key)
        if email == None:
            fn,ln,email,emailid,passw = self.genData()
        self.FirstName,self.LastName = fn,ln
        self.Email,self.EmailId = email,emailid
        self.Password = passw
        self.sess = requests.Session()
        if proxystring != None:
            proxies = {'http': proxystring,'https': proxystring}
            self.sess.proxies.update(proxies)
        
    def genData(self):
        fake = Faker('pl_PL') 
        password = 'standardPass%2235!'
        email,emailid = self.client.CreateInbox()
        return fake.first_name(),fake.last_name(),email,emailid,password

    def ProxyTest(self):
        response = self.sess.get('https://api.ipify.org')
        return response.text
        

    def login(self):

        payload = {
            "grant_type": "password",
            "username": self.Email,
            "password": self.Password
        }
        headers = {
            "x-api-key": "bekorcfmGwGMw9Nh",
            "clientversion": "1.89.1",
            "time-zone": "UTC",
            "user-agent": "xkom_prod/1.89.1",
            "content-type": "application/x-www-form-urlencoded",
            "host": "mobileapi.x-kom.pl",
            "connection": "Keep-Alive",
            "accept-encoding": "gzip"
        }

        response = self.sess.post("https://mobileapi.x-kom.pl/api/v1/xkom/Token", data=payload, headers=headers)
        token_data = response.json()

        self.access_token = token_data['access_token']

    def createAccount(self):
        
        headers = {
            'clientversion': '1.89.1',
            'connection': 'Keep-Alive',
            'content-type': 'application/json; charset=UTF-8',
            'host': 'mobileapi.x-kom.pl',
            'time-zone': 'UTC',
            'user-agent': 'xkom_prod/1.89.1',
            'x-api-key': 'bekorcfmGwGMw9Nh',
        }

        json_data = {
            'AccountIdentity': {
                'FirstName': self.FirstName,
                'LastName': self.LastName,
                'Email': self.Email,
            },
            'AccountAuthData': {
                'Username': self.Email,
                'Password': self.Password,
            },
            'Consents': [
                {
                    'Code': 'regulations',
                    'IsSelected': True,
                    'IsRequested': False,
                },
            ],
            'ConsentOrigin': 'nw_xkom_registration',
        }

        response = self.sess.post('https://mobileapi.x-kom.pl/api/v1/xkom/Account', headers=headers, json=json_data)


        headers = {
            "x-api-key": "bekorcfmGwGMw9Nh",
            "clientversion": "1.89.1",
            "time-zone": "UTC",
            "user-agent": "xkom_prod/1.89.1",
            "content-type": "application/x-www-form-urlencoded",
            "host": "mobileapi.x-kom.pl",
            "connection": "Keep-Alive",
            "accept-encoding": "gzip"
        }

        payload = {
            "grant_type": "password",
            "username": self.Email,
            "password": self.Password
        }

        response = self.sess.post('https://mobileapi.x-kom.pl/api/v1/xkom/Token', headers=headers, data=payload)



        token_data = response.json()

        access_token = token_data['access_token']
        refresh_token = token_data['refresh_token']

        headers = {
            'authorization': f'Bearer {access_token}',
            'clientversion': '1.89.1',
            'connection': 'Keep-Alive',
            'host': 'mobileapi.x-kom.pl',
            'time-zone': 'UTC',
            'user-agent': 'xkom_prod/1.89.1',
            'x-api-key': 'bekorcfmGwGMw9Nh',
            "accept-encoding": "gzip"
        }

        response = self.sess.get('https://mobileapi.x-kom.pl/api/v2/xkom/Account', headers=headers)

        self.tracking_id = response.json()["Identity"]["TrackingId"]

        with open('files/users.txt','a+',encoding='utf-8') as raw: raw.write(f"{self.Email}:{self.Password}:{self.FirstName}:{self.LastName}:{access_token}:{refresh_token}\n")

        self.access_token = access_token



    def activateNewsletter(self):        

        headers = {

            'authorization': f'Bearer {self.access_token}',
            'clientversion': '1.89.1',
            'connection': 'Keep-Alive',
            'content-type': 'application/json; charset=UTF-8',
            'host': 'mobileapi.x-kom.pl',
            'time-zone': 'UTC',
            'user-agent': 'xkom_prod/1.89.1',
            'x-api-key': 'bekorcfmGwGMw9Nh',
        }

        json_data = {
            'ConsentOrigin': 'nw_xkom_unbox',
            'ConsentValues': [
                {
                    'Code': 'email_contact',
                    'IsSelected': True,
                    'IsRequested': False,
                },
            ],
        }

        response = self.sess.put('https://mobileapi.x-kom.pl/api/v1/xkom/Account/Consents', headers=headers, json=json_data)

        activation_link = self.client.getActivationLink(self.EmailId)

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,pl-PL;q=0.8,pl;q=0.7,de;q=0.6',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }



        self.sess.get(activation_link,headers=headers)


    def Consent(self):
        headers = {

            'authorization': f'Bearer {self.access_token}',
            'clientversion': '1.89.1',
            'connection': 'Keep-Alive',
            'content-type': 'application/json; charset=UTF-8',
            'host': 'mobileapi.x-kom.pl',
            'time-zone': 'UTC',
            'user-agent': 'xkom_prod/1.89.1',
            'x-api-key': 'bekorcfmGwGMw9Nh',
        }

        payload = "{\"ConsentOrigin\":\"nw_xkom_unbox\",\"ConsentValues\":[{\"Code\":\"offer_adaptin\",\"IsSelected\":true,\"IsRequested\":false}]}"


        try:response = self.sess.put("https://mobileapi.x-kom.pl/api/v1/xkom/Account/Consents", data=payload, headers=headers)
        except:return False

    def roll(self,rollNumber):
        headers = {
            'authorization': f'Bearer {self.access_token}',
            'clientversion': '1.89.1',
            'connection': 'Keep-Alive',
            'host': 'mobileapi.x-kom.pl',
            'time-zone': 'UTC',
            'user-agent': 'xkom_prod/1.89.1',
            'x-api-key': 'bekorcfmGwGMw9Nh',
        }
        response = self.sess.post(f'https://mobileapi.x-kom.pl/api/v1/xkom/Box/{rollNumber}/Roll', headers=headers)
        roll = response.json()
        try:savePrize(roll,self.Email,self.Password)
        except:print(self.Email,'-',roll['Message'])

