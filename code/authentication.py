# Authenticates a user
def authenticate(pid):
    return True



names = {   "0":"Ludwig", 
            "1":"Lucy", 
            "2":"Casper", 
            "3":"Taha", 
            "4":"Kevin", 
            "5":"Hannes", 
            "6":"Filip", 
            "7":"Felicia"}

def getName(pid):
    if(pid in names):
        return names[pid]
    return "Sven"
