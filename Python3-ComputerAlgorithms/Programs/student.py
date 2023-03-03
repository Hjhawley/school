import re

class Student:

    def __init__(self, lastName, firstName, SSN, email, age):
        self.mLastName = lastName
        self.mFirstName = firstName
        self.mSSN = SSN
        self.mEmail = email
        self.mAge = age
    
    def __eq__(self, rhs):
        if rhs == False:
            return False
        return self.mSSN == rhs.mSSN

    def __ne__(self, rhs):
        return self.mSSN != rhs.mSSN
    
    def __lt__(self, rhs):
        return self.mSSN < rhs.mSSN

    def __gt__(self, rhs):
        return self.mSSN > rhs.mSSN

    def __le__(self, rhs):
        return self.mSSN <= rhs.mSSN

    def __ge__(self, rhs):
        return self.mSSN >= rhs.mSSN
    
    def __int__(self):
        return int(re.sub("[^0-9]", "", self.mSSN)) # Convert the SSN into an integer