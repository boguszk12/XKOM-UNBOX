
import mailslurp_client,time

class Client:

    def __init__(self,api_key) -> None:
        #Email Client Config
        self.api_key = api_key
        self.configuration = mailslurp_client.Configuration()
        self.configuration.api_key['x-api-key'] = self.api_key

    def CreateInbox(self):
        with mailslurp_client.ApiClient(self.configuration) as api_client:
            inbox_controller = mailslurp_client.InboxControllerApi(api_client)
            inbox = inbox_controller.create_inbox()
            return inbox.email_address,inbox.id

    def getActivationLink(self,id):
        time.sleep(5)
        with mailslurp_client.ApiClient(self.configuration) as api_client:
            waitfor_controller = mailslurp_client.WaitForControllerApi(api_client)
            email = waitfor_controller.wait_for_latest_email(inbox_id=id, timeout=20000, unread_only=True)
            #Best parsing known to human kind :)
            activation_link = email.body.split('Sprawdź')[0].split('href="')[-1].split('"')[0]

        #with open('x.html','w',encoding='utf-8') as raw: raw.write(response.text)
            
        return activation_link
