from twilio.rest import Client


def send_sms(mobile,order):
 
    account_sid = "AC020410301a648c679de11ebbef4e5427"            #company details
    auth_token = "81ee7f7b5ed7a74f5d9b4423ef11b5a8"
    client =Client(account_sid, auth_token)
    user_mobile = mobile
    message = client.messages.create(
        to="+91"+user_mobile,
        #to="+918130135866",
        from_="+12016361376", #Aftab

        # from_="+18555728559",
        # from_="+17042702788", #--office
        body=" Your Order has been Placed.. Track Your Order in E-Kart App. your Order No is: "+str(order))


