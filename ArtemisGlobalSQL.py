# 10/2/2021
###########
# MySQL database for Lunar surface operations:  real-time collaboration

import pymysql

mydatabase = "logs_db"


connect = None
try:
    # connect your database and python ide
    connect = pymysql.connect(host='localhost', user="artemis_user", password="TeamArtemis2021!")
    # create cursor object, named cur
    with connect.cursor() as cur:
        # new datatbase
        cur.execute('CREATE DATABASE {}'.format(mydatabase))
        # new table
        # 'users' table should be main table that's created first (user creates account first then can create log with media added to that log input)
        cur.execute('CREATE TABLE `logs_db`.`users` (\n'
                    '`username` VARCHAR(30) NOT NULL UNIQUE,\n'
                    '`password` VARCHAR(50) NOT NULL,\n'
                    '`firstname` VARCHAR(30) NOT NULL,\n'
                    '`lastname` VARCHAR(30) NOT NULL,\n'
                    '`company` VARCHAR(30) NOT NULL,\n'
                    '`approval` BOOLEAN NOT NULL,\n'
                    ' PRIMARY KEY (`username`));')

        cur.execute('CREATE TABLE `logs_db`.`media` (\n'
                    '`mediaID` int NOT NULL AUTO_INCREMENT,\n'
                    '`imageref` VARCHAR(256),\n'
                    '`videoref` VARCHAR(256),\n'
                    '`audioref` VARCHAR(256),\n'
                    ' PRIMARY KEY (`mediaID`));')

        cur.execute('CREATE TABLE `logs_db`.`logs` (\n'
                    '`logID` int AUTO_INCREMENT NOT NULL UNIQUE,\n'
                    '`username` VARCHAR(30) NOT NULL,\n'
                    '`logdate` DATETIME NOT NULL,\n'
                    '`logtext` TEXT,\n'
                    '`mediaID` int,\n'
                    '`hardware` TEXT,\n'
                    '`updateID` VARCHAR(30) DEFAULT NULL,\n'
                    '`hashtag` VARCHAR(30),\n'
                    '`approvelog` BOOLEAN DEFAULT FALSE,\n'
                    ' FOREIGN KEY (`username`) REFERENCES `users` (`username`),\n'
                    ' FOREIGN KEY (`mediaID`) REFERENCES `media` (`mediaID`),\n'
                    ' PRIMARY KEY (`logID`));')

        cur.execute(
            'CREATE INDEX idx_username ON `logs_db`.`users` (`username`);'
        )

        cur.execute(
            'CREATE INDEX idx_media ON `logs_db`.`media` (`mediaID`);'
        )

except Exception as e:
    print("Exception Error")
    print(e)
finally:
    if connect:
        connect.close()