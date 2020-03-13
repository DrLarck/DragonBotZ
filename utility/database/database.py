"""
Manage the database

--

Author : DrLarck

Last update : 13/03/20 by DrLarck
"""

import asyncio
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

    async def __close(self):
        """
        Close the connection to the database

        --

        :return: `None`
        """

        # Release the connection if there is an existing one
        if self.__connection is not None:
            await self.__pool.release(self.__connection)

        return

    # Public method
    async def init(self):
        """
        Init the database object

        --

        :return: `None`
        """

        await self.__get_connection()

        return

    async def execute(self, query, parameters=None):
        """
        Execute an SQL query

        :param query: (`str`)

        :param parameters: (`list`)

        --

        :return: `None`
        """

        if parameters is None:
            parameters = []

        await self.__get_connection()

        # Execute the query with the passed parameters
        try:
            await self.__connection.execute(query, *parameters)

        # Ignore the UniqueViolationError
        except asyncpg.UniqueViolationError:
            pass

        # Gracefully close the connection
        finally:
            await self.__close()

        return

    async def fetch_value(self, query):
        """
        Fetch a single value from the database

        :param query: (`str`)

        --

        :return: Fetched value or `None` if not found
        """

        await self.__get_connection()

        # Execute the query
        fetched = await self.__connection.fetchval(query)

        # Gracefully close the connection
        await self.__close()

        return fetched

    async def fetch_row(self, query):
        """
        Fetch rows from the database

        :param query: (`str`)

        --

        :return: `list` of rows or `None` if not found
        """

        await self.__get_connection()

        # Fetch the row(s)
        row = await self.__connection.fetch(query)

        # Gracefully close the connection
        await self.__close()

        return row

    async def create_game_tables(self):
        """
        Create the game tables.

        --

        :return: `None`
        """

        table_queries = [
            # Logs
            """
            CREATE TABLE IF NOT EXISTS command_log(
                command TEXT,
                parameter TEXT,
                date TEXT,
                time BIGINT,
                caller_id BIGINT,
                caller_name TEXT,
                message TEXT
            );
            """,
            # player_info table
            """
            CREATE SEQUENCE IF NOT EXISTS player_info_reference_seq;
            CREATE TABLE IF NOT EXISTS player_info(
                reference BIGINT PRIMARY KEY DEFAULT nextval('player_info_reference_seq') NOT NULL,
                player_name TEXT,
                player_id BIGINT,
                player_register_date TEXT,
                player_language TEXT DEFAULT 'EN'
            );
            CREATE UNIQUE INDEX IF NOT EXISTS player_info_reference_index ON player_info(reference);
            """
        ]

        # Create the tables
        for query in table_queries:
            await asyncio.sleep(0)

            await self.execute(query)

        return
