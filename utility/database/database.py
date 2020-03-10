"""
Manage the database

--

Author : DrLarck

Last update : 10/03/20 by DrLarck
"""

import asyncpg
import os


class Database:
    """
    Represents the database the game is connected to
    """

    def __init__(self):
        # Private
        # Database information
        self.__host = os.environ["dev_dbz_db_host"]
        self.__database = os.environ["dev_dbz_db_name"]
        self.__user = os.environ["dev_dbz_db_user"]
        self.__password = os.environ["dev_dbz_db_password"]
        self.__port = "5432"

        # Connection
        self.__pool = None
        self.__connection = None

    # Private method
    async def __get_connection(self):
        """
        Get the connection pool and set the connection.
        --

        :return: `asyncpg.connection.Connection` or `None`
        """

        # If the pool has not been set yet
        if self.__pool is None:
            self.__pool = await asyncpg.create_pool(host=self.__host, database=self.__database,
                                                    user=self.__user, password=self.__password,
                                                    port=self.__port)

        # If the connection pool exists : defines the connection
        if self.__pool is not None:
            self.__connection = await self.__pool.acquire()

        return self.__connection

