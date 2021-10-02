# 10/2/2021
###########
# MySQL database for Lunar surface operations:  real-time collaboration

import pymysql

mydatabase = "logs_db"


connect = None
try:
    # connect your database and python ide
    connect = pymysql.connect(user="artemis_user", password="TeamArtemis2021!")
    # create cursor object, named cur
    with connect.cursor() as cur:
        # new datatbase
        cur.execute('CREATE DATABASE {}'.format(mydatabase))
        # new table
        cur.execute('CREATE TABLE `logs_db`.`logs` (\n'
                    '`logID` VARCHAR(20) NOT NULL UNIQUE,\n'
                    '`username` VARCHAR(30) NOT NULL,\n'
                    '`logdate` DATETIME NOT NULL,\n'
                    '`logtext` TEXT,\n'
                    '`mediaID` int UNIQUE,\n'
                    '`hardware` TEXT,\n'
                    '`otherUsername` VARCHAR(30),\n'
                    '`logEdit` DATETIME,\n'
                    ' PRIMARY KEY (`logID`));')

        cur.execute('CREATE TABLE `logs_db`.`users` (\n'
                    '`userID` int NOT NULL,\n'
                    '`username` VARCHAR(30), NOT NULL UNIQUE\n'
                    '`firstname` TEXT NOT NULL,\n'
                    '`lastname` TEXT NOT NULL,\n'
                    '`company` TEXT NOT NULL,\n'
                    '`approval` BOOLEAN NOT NULL,\n'
                    ' FOREIGN KEY (`username`) REFERENCES logs(username),\n'
                    ' PRIMARY KEY (`userID`);')

        cur.execute('CREATE TABLE `logs_db`.`media` (\n'
                    '`mediaID` int NOT NULL,\n'
                    '`imageref` TEXT,\n'
                    '`videoref` TEXT,\n'
                    '`audioref` TEXT,\n'
                    ' FOREIGN KEY (`mediaID`) REFERENCES logs(mediaID);')

except Exception as e:
    print("Exception Error")
    print(e)
finally:
    if connect:
        connect.close()