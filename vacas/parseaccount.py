#understand if a vehicle is mapped to something or not
def checkIfMapped (account):
    if account[0:3] == 'BIP':
        return 'Not Mapped'
    else:
        return account

#paint the talbe box according to the account
def getColor (account):
    if account == 'No account':
        return '#ffebe5' #red
    elif account == 'Not Mapped':
        return '#fffae5' #yellow
    else:
        return '#e3fcef' #green