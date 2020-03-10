"""
Manage the database

--

Author : DrLarck

Last update : 10/03/20 by DrLarck
"""

import asyncio
import os


class Database:
    """
    Represents the database the game is connected to
    """

    def __init__(self):
        self.__database = os.environ["dev_dbz_db_name"]
        self.__user = os.environ["dev_dbz_db_user"]
        self.__password = os.environ["dev_dbz_db_password"]
        self.__host = os.environ["dev_dbz_db_host"]
        self.__port = os.environ["dev_dbz_db_port"]

