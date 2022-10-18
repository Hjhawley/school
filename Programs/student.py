class Student:

    def __init__(self, lastName, firstName, SSN, email, age):
        self.mLastName = lastName
        self.mFirstName = firstName
        self.mSSN = SSN
        self.mEmail = email
        self.mAge = age
    
    def __eq__(self, rhs):
        if self.mSSN == rhs.mSSN:
            return True
        else:
            return False