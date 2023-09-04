

def Smtp_Cred(file_Path):
    smtp = {}
    with open(file_Path , 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                key, value = line.split('=', 1)
                smtp[key.strip()] = value.strip()
    return smtp
        