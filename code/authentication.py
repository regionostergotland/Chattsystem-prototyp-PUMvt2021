# Authenticates a user
def authenticate(pid):
    return True


names = {"0": "Patienten Peter",
         "1": "Vårdpersonalen Viktor",
         "2": "Specialisten Sara"}


def getName(pid):
    if(pid in names):
        return names[pid]
    return "Sven"
