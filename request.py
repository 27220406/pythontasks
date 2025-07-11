import requests
def my_request(username):
    data = requests.get(f" https://api.github.com/users/{username}")
    if  data.status_code==200:
        mydata= data.json()

        print(mydata)
my_request("27220406")


   
    


