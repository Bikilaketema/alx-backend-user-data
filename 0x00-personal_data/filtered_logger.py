#!/usr/bin/env python3
''' Task 0: Regex-ing: filter_datum
    Task 1: Log formatter: class RedactingFormatter
    Task 2: Create logger
    Task 3: Connect to secure database
    Task 4: Read and filter data
'''

import re
from typing import List
import logging
import mysql.connector
from os import getenv


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    '''a function that returns the log message obfuscated:
        Arguments: fields : redaction: message: separator:
    '''

    for i in fields:
        message = re.sub(i + "=.*?" + separator,
                         i + "=" + redaction + separator,
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Constructor Method """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filters values in incoming log records using filter_datum """
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    ''' get_logger function that takes no arguments
                     and returns a logging.Logger object.
    '''
    log = logging.getLogger('user_data')
    log.setLevel(logging.INFO)
    log.propagate = False

    sh = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    sh.setFormatter(formatter)
    log.addHandler(sh)

    return log


def get_db() -> mysql.connector.connection.MySQLConnection:
    ''' read a data from holberton schools secured database.
    '''
    connection_db = mysql.connector.connection.MySQLConnection(
        user=getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=getenv('PERSONAL_DATA_DB_NAME'))

    return connection_db


def main():
    '''The function will obtain a database connection using get_db
    and retrieve all rows in the users table
    and display each row under a filtered format
    '''
    database = get_db()
    cursor = database.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = [i[0] for i in cursor.description]

    log = get_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, fields))
        log.info(str_row.strip())

    cursor.close()
    database.close()


if __name__ == '__main__':
    main()
