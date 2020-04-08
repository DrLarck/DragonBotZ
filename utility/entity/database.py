"""
Manage the database

--

Author : DrLarck

Last update : 08/04/20 by DrLarck
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

    async def fetch_value(self, query, parameters=None):
        """
        Fetch a single value from the database

        :param query: (`str`)

        :param parameters: (`list`)

        --

        :return: Fetched value or `None` if not found
        """

        # Init
        await self.__get_connection()

        if parameters is None:
            parameters = []
            
        # Execute the query
        fetched = await self.__connection.fetchval(query, *parameters)

        # Gracefully close the connection
        await self.__close()

        return fetched

    async def fetch_row(self, query, parameters=None):
        """
        Fetch rows from the database

        :param query: (`str`)

        :param parameters: (`list`)

        --

        :return: `list` of rows or `None` if not found
        """

        # Init
        await self.__get_connection()

        if parameters is None:
            parameters = []

        # Fetch the row(s)
        row = await self.__connection.fetch(query, *parameters)

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
            # command_log table
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
                player_id BIGINT,                
                player_name TEXT,
                player_register_date TEXT,
                player_language TEXT DEFAULT 'EN'
            );
            CREATE UNIQUE INDEX IF NOT EXISTS player_info_reference_index ON player_info(reference);
            CREATE UNIQUE INDEX IF NOT EXISTS player_info_id_index ON player_info(player_id);
            """,

            # player_experience table
            """
            CREATE SEQUENCE IF NOT EXISTS player_experience_reference_seq;
            CREATE TABLE IF NOT EXISTS player_experience(
                reference BIGINT PRIMARY KEY DEFAULT nextval('player_info_reference_seq') NOT NULL,
                player_id BIGINT,
                player_name TEXT,
                player_level BIGINT DEFAULT 1,
                player_experience BIGINT DEFAULT 0
            );
            CREATE UNIQUE INDEX IF NOT EXISTS player_experience_reference_index ON player_experience(reference);
            """,

            # player_resource table
            """
            CREATE SEQUENCE IF NOT EXISTS player_resource_reference_seq;
            CREATE TABLE IF NOT EXISTS player_resource(
                reference BIGINT PRIMARY KEY DEFAULT nextval('player_resource_reference_seq') NOT NULL,
                player_id BIGINT,
                player_name TEXT,
                player_dragonstone BIGINT DEFAULT 0,
                player_zeni BIGINT DEFAULT 0
            );
            CREATE UNIQUE INDEX IF NOT EXISTS player_resource_reference_index ON player_resource(reference);
            """,

            # player_time table
            """
            CREATE TABLE IF NOT EXISTS player_time(
                player_id BIGINT,
                player_name TEXT,
                player_hourly_time BIGINT DEFAULT 0,
                player_daily_time BIGINT DEFAULT 0,
                player_hourly_combo BIGINT DEFAULT 0,
                player_daily_combo BIGINT DEFAULT 0
            );
            CREATE UNIQUE INDEX IF NOT EXISTS player_time_index ON player_time(player_id);
            """,

            # character_reference table
            """
            CREATE SEQUENCE IF NOT EXISTS character_reference_reference_seq;
            CREATE TABLE IF NOT EXISTS character_reference(
                reference BIGINT PRIMARY KEY DEFAULT nextval('character_reference_reference_seq') NOT NULL,
                character_name TEXT,
                character_type INTEGER,
                character_rarity INTEGER,
                character_card TEXT,
                character_health BIGINT,
                character_damage BIGINT,
                character_attack1_name TEXT,
                character_attack1_damage BIGINT,
                character_attack2_name TEXT,
                character_attack2_damage BIGINT,
                character_attack3_name TEXT,
                character_attack3_damage BIGINT,
                character_attack4_name TEXT,
                character_attack4_damage BIGINT
            );
            CREATE UNIQUE INDEX IF NOT EXISTS character_reference_reference_index ON character_reference(reference);
            """,

            # character_unique table
            """
            CREATE SEQUENCE IF NOT EXISTS character_unique_reference_seq;
            CREATE TABLE IF NOT EXISTS character_unique(
                reference BIGINT PRIMARY KEY DEFAULT nextval('character_unique_reference_seq') NOT NULL,
                character_reference BIGINT,
                character_unique_id TEXT DEFAULT 'NONE',
                character_owner_id BIGINT,
                character_owner_name TEXT,
                character_rarity INTEGER,
                character_level INTEGER DEFAULT 1,
                character_experience BIGINT DEFAULT 0,
                character_dokkan_rate INTEGER DEFAULT 0,
                character_star INTEGER DEFAULT 0,
                character_training_armor INTEGER DEFAULT 0,
                character_training_spirit INTEGER DEFAULT 0,
                character_training_physical INTEGER DEFAULT 0,
                character_training_ki INTEGER DEFAULT 0
            );
            CREATE UNIQUE INDEX IF NOT EXISTS character_unique_index ON character_unique(reference);
            """,

            # banner table
            """
            CREATE SEQUENCE IF NOT EXISTS banner_reference_seq;
            CREATE TABLE IF NOT EXISTS banner(
                reference BIGINT PRIMARY KEY DEFAULT nextval('banner_reference_seq') NOT NULL,
                banner_name TEXT,
                banner_image TEXT,
                banner_content TEXT
            );
            CREATE UNIQUE INDEX IF NOT EXISTS banner_reference_index ON banner(reference);
            """
        ]

        # Create the tables
        for query in table_queries:
            await asyncio.sleep(0)

            await self.execute(query)

        return
