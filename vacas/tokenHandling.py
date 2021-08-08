class jwt:
    def __init__(self, envint, envprod):
        self.envint = envint
        self.envprod = envprod

#Read the JWT token files
def readJWT (file):
    f = open(file,"r")
    content = f.read()
    f.close()
    return content

#Write to JWT token files
def writeJWT (file, content):
    f = open(file,"w")
    f.write(content)
    f.close()