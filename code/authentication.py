# Authenticates a user
def authenticate(pid):
    return True



names = {   "0":"Ludwig", 
            "1":"Casper", 
            "2":"Taha", 
            "3":"Kevin", 
            "4":"Hannes", 
            "5":"Filip", 
            "6":"Lucy", 
            "7":"Felicia"}

def getName(pid):
    if(pid in names):
        return names[pid]
    return "Sven"
