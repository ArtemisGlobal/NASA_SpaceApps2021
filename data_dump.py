# Data Dump / Random data to test logs database


import pymysql


def send_request(request, values):
    connect = pymysql.connect(host='localhost', user="artemis_user", password="TeamArtemis2021!")

    # create cursor object, named cur
    print(request)
    with connect.cursor() as cur:
        cur.execute(request, values)
        connect.commit()
    connect.close()

             # username,  password, firstname, lastname,  company,   approval
user_data = [("ChrisN", '1234!', 'Christine', 'Nolan', 'Hubbal Finacial', True),
             ('DaveB', '1523#', 'Dave', 'Borncamp', 'Ball Corp.', False),
             ('RuthF', '9875$', 'Ruth', 'Fantastic', 'Student', False)]

for data in user_data:
    user_string = "INSERT INTO `logs_db`.`users` (username, password, firstname, lastname, company, approval) VALUES (%s, %s, %s, %s, %s, %s);"
    send_request(user_string, data)


             # username, logdate,     logtext,     hardware, updateID, hashtag, approvelog)
log_data = [('ChrisN', '2020-10-09', 'temp is 15C', 'thermo', None, '#spacetemps', True),
            ('DaveB', '2019-12-15', 'rock is hard', 'hammer', 1, '#spacerocks', True),
            ('RuthF', '2021-01-01', '5cm soil sample', 'shovel', None, '#spacesoil', False)]

for data in log_data:
    log_string = "INSERT INTO `logs_db`.`logs` (username, logdate, logtext, hardware, UpdateID, hashtag, approvelog) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    send_request(log_string, data)


    # imageref, videoref, audioref
media_data = [('Im123', '', ''),
              ('', '', 'Aud123'),
              ('', 'Vid123', '')]

for data in media_data:
    media_string = "INSERT INTO `logs_db`.`media` (imageref, videoref, audioref) VALUES (%s, %s, %s);"
    send_request(media_string, data)

