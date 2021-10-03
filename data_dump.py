# Data Dump / Random data to test logs database


import pymysql

connect = pymysql.connect(host='localhost', user="artemis_user", password="TeamArtemis2021!")

def send_request(request):
    # create cursor object, named cur
    with connect.cursor() as cur:
        cur.execute(request)

             # username,  password, firstname, lastname,  company,   approval
user_data = ['(`ChrisN`,`1234!`, `Christine`, `Nolan`, `Hubbal Finacial`, `true`)',
             '(`DaveB`, `1523#`, `Dave`, `Borncamp`, `Ball Corp.`, `false`)',
             '(`RuthF`, `9875$`, `Ruth`, `Fantastic`, `Student`, `false`)']

for data in user_data:
    user_string = f'INSERT INTO Users VALUES {data};'
    send_request(user_string)


   # log ID,  username, logdate,     logtext,    mediaID, hardware, updateID, hashtag, approvelog)
log_data = ['(`ChrisN`,`2020-10-09`, `temp is 15C`, `4`, `thermo`, ``, `spacetemps`, `true)',
            '(`DaveB`, `2019-12-15`, `rock is hard`, `6`, `hammer`, `321`, `spacerocks`, `true`)',
            '(`RuthF`, `2021-01-01`, `5cm soil sample`, `8`, `shovel`, ``, `spacesoil`, `false`)']

for data in log_data:
    log_string = f'INSERT INTO logs (logID, username, logdate, logtext, mediaID, hardware, otherUsername, logEdit, hashtag, approvelog) VALUES {data};'
    send_request(log_string)


    # mediaID, imageref, videoref, audioref
media_data = ['(`4`, `Im123`, ``, ``)',
              '(`6`, ``, ``, `Aud123`)',
              '(`8`, ``, `Vid123`, ``)']

for data in media_data:
    media_string = f'INSERT INTO media (mediaID, imageref, videoref, audioref) VALUES {data};'
    send_request(media_string)

