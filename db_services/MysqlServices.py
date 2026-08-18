import discord
from discord.ext import commands
import mysql.connector
from discord.ext.commands import CommandError


# noinspection PyGlobalUndefined
async def check_connection(host: str = commands.Parameter(name="host",
                                                          description="The host (server hostname) of the server you would like to connect to",
                                                          kind=commands.Parameter.KEYWORD_ONLY),
                           user: str = commands.Parameter(name="user",
                                                          description="The username of the login authentication for MySQL",
                                                          kind=commands.Parameter.KEYWORD_ONLY),
                           password: str = commands.Parameter(name="password",
                                                              description="The password of the login authentication for MySQL",
                                                              kind=commands.Parameter.KEYWORD_ONLY),
                           database: str = commands.Parameter(name="database",
                                                              description="The name of the database you would like to connect to",
                                                              kind=commands.Parameter.KEYWORD_ONLY)):
    """
        Gets all words from the 'banned_words' DB and returns them in a list.
        :param host: Server hostname of MySql Database
        :param user: Username for server authentication
        :param password: Password for server authentication
        :param database: Database to connect to
        :return:
        """

    if host is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('host', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The host (server hostname) of the server you would like to connect to."))

    if user is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('user', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The username of the login authentication for MySQL."))

    if password is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('password', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The password of the login authentication for MySQL."))

    if database is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('database', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The name of the database you would like to connect to."))
    mydb = None
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        await create_default_tables(host=host, user=user, password=password, database=database)

        return True
    except ConnectionError as e:
        print(e.strerror)
    finally:
        if mydb:
            mydb.close()


# noinspection PyGlobalUndefined
async def get_banned_words_from_db(host: str = commands.Parameter(name="host",
                                                                  description="The host (server hostname) of the server you would like to connect to",
                                                                  kind=commands.Parameter.KEYWORD_ONLY),
                                   user: str = commands.Parameter(name="user",
                                                                  description="The username of the login authentication for MySQL",
                                                                  kind=commands.Parameter.KEYWORD_ONLY),
                                   password: str = commands.Parameter(name="password",
                                                                      description="The password of the login authentication for MySQL",
                                                                      kind=commands.Parameter.KEYWORD_ONLY),
                                   database: str = commands.Parameter(name="database",
                                                                      description="The name of the database you would like to connect to",
                                                                      kind=commands.Parameter.KEYWORD_ONLY)):
    """
        Gets all words from the 'banned_words' DB and returns them in a list.
        :param host: Server hostname of MySql Database
        :param user: Username for server authentication
        :param password: Password for server authentication
        :param database: Database to connect to
        :return:
        """

    if host is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('host', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The host (server hostname) of the server you would like to connect to."))

    if user is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('user', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The username of the login authentication for MySQL."))

    if password is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('password', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The password of the login authentication for MySQL."))

    if database is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('database', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The name of the database you would like to connect to."))

    mydb = None
    mycursor = None
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        words = []
        mycursor = mydb.cursor()
        mycursor.execute("SELECT banned_word FROM banned_words")
        results = mycursor.fetchall()

        for x in results:
            words.append(str(x[0]))

        return results
    except Exception as e:
        raise CriticalError.DatabaseError(f"There has been an error getting the banned words from the database file. {e}")
    finally:
        mycursor.close()
        mydb.close()


# noinspection PyGlobalUndefined
async def add_banned_word_to_db(host: str = commands.Parameter(name="host",
                                                               description="The host (server hostname) of the server you would like to connect to",
                                                               kind=commands.Parameter.KEYWORD_ONLY),
                                user: str = commands.Parameter(name="user",
                                                               description="The username of the login authentication for MySQL",
                                                               kind=commands.Parameter.KEYWORD_ONLY),
                                password: str = commands.Parameter(name="password",
                                                                   description="The password of the login authentication for MySQL",
                                                                   kind=commands.Parameter.KEYWORD_ONLY),
                                database: str = commands.Parameter(name="database",
                                                                   description="The name of the database you would like to connect to",
                                                                   kind=commands.Parameter.KEYWORD_ONLY),
                                banned_word: str = commands.Parameter(name="banned_word",
                                                                      description="The word you would like banned from the server. Will be added to MySQL DB for storage",
                                                                      kind=commands.Parameter.KEYWORD_ONLY)):
    """
        Adds given word to the 'banned_words' DB.
        :param host: Server hostname of MySql Database
        :param user: Username for server authentication
        :param password: Password for server authentication
        :param database: Database to connect to
        :param banned_word: Word the initiating user would like to add to the 'banned_words' DB
        :return:
        """

    if host is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('host', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The host (server hostname) of the server you would like to connect to."))

    if user is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('user', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The username of the login authentication for MySQL."))

    if password is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('password', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The password of the login authentication for MySQL."))

    if database is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('database', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The name of the database you would like to connect to."))

    if banned_word is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('banned_word', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The word you would like banned from the server. Will be added to MySQL DB for storage."))

    mydb = None
    mycursor = None
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        mycursor = mydb.cursor()
        mycursor.execute("INSERT INTO banned_words (banned_word) VALUES (%s)", (banned_word,))
        mydb.commit()

        return True
    except Exception as e:
        raise CriticalError.DatabaseError(f"There has been an error adding the banned word to the database file. {e}")
    finally:
        mycursor.close()
        mydb.close()


# noinspection PyGlobalUndefined
async def delete_banned_word_from_db(host: str = commands.Parameter(name="host",
                                                                    description="The host (server hostname) of the server you would like to connect to",
                                                                    kind=commands.Parameter.KEYWORD_ONLY),
                                     user: str = commands.Parameter(name="user",
                                                                    description="The username of the login authentication for MySQL",
                                                                    kind=commands.Parameter.KEYWORD_ONLY),
                                     password: str = commands.Parameter(name="password",
                                                                        description="The password of the login authentication for MySQL",
                                                                        kind=commands.Parameter.KEYWORD_ONLY),
                                     database: str = commands.Parameter(name="database",
                                                                        description="The name of the database you would like to connect to",
                                                                        kind=commands.Parameter.KEYWORD_ONLY),
                                     banned_word: str = commands.Parameter(name="banned_word",
                                                                           description="The word you would like banned from the server. Will be added to MySQL DB for storage",
                                                                           kind=commands.Parameter.KEYWORD_ONLY)):
    """
        Deletes the given word from the 'banned_words' DB.
        :param host: Server hostname of MySql Database
        :param user: Username for server authentication
        :param password: Password for server authentication
        :param database: Database to connect to
        :param banned_word: Word the initiating user would like to remove from the 'banned_words' DB
        :return:
        """

    if host is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('host', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The host (server hostname) of the server you would like to connect to."))

    if user is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('user', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The username of the login authentication for MySQL."))

    if password is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('password', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The password of the login authentication for MySQL."))

    if database is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('database', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The name of the database you would like to connect to."))

    if banned_word is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('banned_word', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The word you would like banned from the server. Will be added to MySQL DB for storage."))

    mydb = None
    mycursor = None
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT banned_word FROM banned_words WHERE banned_word = %s", (banned_word,))
        result = mycursor.fetchone()

        if result is not None:
            mycursor.execute("DELETE FROM banned_words WHERE banned_word = %s", (banned_word,))
            mydb.commit()
            return True
    except Exception as e:
        raise CriticalError.DatabaseError(f"There has been an error deleting the banned word from the database file. {e}")
    finally:
        mycursor.close()
        mydb.close()


# noinspection PyGlobalUndefined
async def create_default_tables(host: str = commands.Parameter(name="host",
                                                               description="The host (server hostname) of the server you would like to connect to",
                                                               kind=commands.Parameter.KEYWORD_ONLY),
                                user: str = commands.Parameter(name="user",
                                                               description="The username of the login authentication for MySQL",
                                                               kind=commands.Parameter.KEYWORD_ONLY),
                                password: str = commands.Parameter(name="password",
                                                                   description="The password of the login authentication for MySQL",
                                                                   kind=commands.Parameter.KEYWORD_ONLY),
                                database: str = commands.Parameter(name="database",
                                                                   description="The name of the database you would like to connect to",
                                                                   kind=commands.Parameter.KEYWORD_ONLY)):
    """
        Creates the default tables needed to run the bot's functions in its entirety.
        :param host: Server hostname of MySql Database
        :param user: Username for server authentication
        :param password: Password for server authentication
        :param database: Database to connect to
        :return:
        """

    if host is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('host', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The host (server hostname) of the server you would like to connect to."))

    if user is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('user', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The username of the login authentication for MySQL."))

    if password is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('password', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The password of the login authentication for MySQL."))

    if database is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('database', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The name of the database you would like to connect to."))

    mydb = None
    mycursor = None
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        mycursor = mydb.cursor()
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, user_id TEXT, name TEXT)")
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS banned_words (id INT AUTO_INCREMENT PRIMARY KEY, banned_word TEXT)")
        mydb.commit()

        return True
    except Exception as e:
        raise CriticalError.DatabaseError(f"There has been an error creating the default tables in the database file. {e}")
    finally:
        mycursor.close()
        mydb.close()


# noinspection PyGlobalUndefined
async def check_if_user_exists_in_db(user_id: str = commands.Parameter(name="user_id",
                                                                       description="The ID of the user within the DB. Used for parsing the DB for user information",
                                                                       kind=commands.Parameter.KEYWORD_ONLY),
                                     host: str = commands.Parameter(name="host",
                                                                    description="The host (server hostname) of the server you would like to connect to",
                                                                    kind=commands.Parameter.KEYWORD_ONLY),
                                     user: str = commands.Parameter(name="user",
                                                                    description="The username of the login authentication for MySQL",
                                                                    kind=commands.Parameter.KEYWORD_ONLY),
                                     password: str = commands.Parameter(name="password",
                                                                        description="The password of the login authentication for MySQL",
                                                                        kind=commands.Parameter.KEYWORD_ONLY),
                                     database: str = commands.Parameter(name="database",
                                                                        description="The name of the database you would like to connect to",
                                                                        kind=commands.Parameter.KEYWORD_ONLY)):
    """
        Checks if a user exists in the 'users' DB with information given.
        :param user_id: ID of the message author is user ID in 'users' DB
        :param host: Server hostname of MySql Database
        :param user: Username for server authentication
        :param password: Password for server authentication
        :param database: Database to connect to
        :return:
        """

    if user_id is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('user_id', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The ID of the user within the DB. Used for parsing the DB for user information."))

    if host is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('host', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The host (server hostname) of the server you would like to connect to."))

    if user is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('user', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The username of the login authentication for MySQL."))

    if password is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('password', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The password of the login authentication for MySQL."))

    if database is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('database', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The name of the database you would like to connect to."))

    mydb = None
    mycursor = None
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        results = mycursor.fetchone()
        mydb.commit()

        if results is None:
            return True
        else:
            return False
    except Exception as e:
        raise CriticalError.DatabaseError(f"There has been an error checking the database file for the user. {e}")
    finally:
        mycursor.close()
        mydb.close()


# noinspection PyGlobalUndefined
async def add_user_to_db(user_id: str = commands.Parameter(name="user_id",
                                                           description="The ID of the user within the DB. Used for parsing the DB for user information",
                                                           kind=commands.Parameter.KEYWORD_ONLY),
                         name: str = commands.Parameter(name="name",
                                                        description="The name of the user to add to the DB. Used for parsing the DB for user information",
                                                        kind=commands.Parameter.KEYWORD_ONLY),
                         host: str = commands.Parameter(name="host",
                                                        description="The host (server hostname) of the server you would like to connect to",
                                                        kind=commands.Parameter.KEYWORD_ONLY),
                         user: str = commands.Parameter(name="user",
                                                        description="The username of the login authentication for MySQL",
                                                        kind=commands.Parameter.KEYWORD_ONLY),
                         password: str = commands.Parameter(name="password",
                                                            description="The password of the login authentication for MySQL",
                                                            kind=commands.Parameter.KEYWORD_ONLY),
                         database: str = commands.Parameter(name="database",
                                                            description="The name of the database you would like to connect to",
                                                            kind=commands.Parameter.KEYWORD_ONLY)):
    """
        Adds user to the 'users' DB with the information given.
        :param user_id: ID of the message author is user ID in 'users' DB
        :param name: Name of the user to add o the database.
        :param host: Server hostname of MySql Database
        :param user: Username for server authentication
        :param password: Password for server authentication
        :param database: Database to connect to
        :return:
        """

    if name is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('name', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The name of the user to add to the DB. Used for parsing the DB for user information. "))

    if user_id is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('user_id', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The ID of the user to add to the DB. Used for parsing the DB for user information."))

    if host is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('host', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The host (server hostname) of the server you would like to connect to."))

    if user is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('user', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The username of the login authentication for MySQL."))

    if password is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('password', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The password of the login authentication for MySQL."))

    if database is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('database', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The name of the database you would like to connect to."))

    mydb = None
    mycursor = None
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        mycursor = mydb.cursor()
        mycursor.execute("INSERT INTO users (user_id, name) VALUES (%s,%s)", (user_id, name))
        mydb.commit()

        return True
    except Exception as e:
        raise CriticalError.DatabaseError(f"There has been an error adding the user to the database. {e}")
    finally:
        mycursor.close()
        mydb.close()


# noinspection PyGlobalUndefined
async def get_tables_in_db(host: str = commands.Parameter(name="host",
                                                          description="The host (server hostname) of the server you would like to connect to",
                                                          kind=commands.Parameter.KEYWORD_ONLY),
                           user: str = commands.Parameter(name="user",
                                                          description="The username of the login authentication for MySQL",
                                                          kind=commands.Parameter.KEYWORD_ONLY),
                           password: str = commands.Parameter(name="password",
                                                              description="The password of the login authentication for MySQL",
                                                              kind=commands.Parameter.KEYWORD_ONLY),
                           database: str = commands.Parameter(name="database",
                                                              description="The name of the database you would like to connect to",
                                                              kind=commands.Parameter.KEYWORD_ONLY)):
    """
        Gets all tables in given database.
        :param host: Server hostname of MySql Database
        :param user: Username for server authentication
        :param password: Password for server authentication
        :param database: Database to connect to
        :return:
        """

    if host is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('host', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The host (server hostname) of the server you would like to connect to."))

    if user is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('user', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The username of the login authentication for MySQL."))

    if password is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('password', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The password of the login authentication for MySQL."))

    if database is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('database', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The name of the database you would like to connect to."))

    mydb = None
    mycursor = None
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        tables = []

        mycursor = mydb.cursor()
        mycursor.execute("SHOW TABLES")
        results = mycursor.fetchall()
        mydb.commit()

        for x in results:
            tables.append(x[0])

        return tables
    except Exception as e:
        raise CriticalError.DatabaseError(f"There has been an error getting the tables from the database. {e}")
    finally:
        mycursor.close()
        mydb.close()


# noinspection PyGlobalUndefined
async def get_databases(host: str = commands.Parameter(name="host",
                                                       description="The host (server hostname) of the server you would like to connect to",
                                                       kind=commands.Parameter.KEYWORD_ONLY),
                        user: str = commands.Parameter(name="user",
                                                       description="The username of the login authentication for MySQL",
                                                       kind=commands.Parameter.KEYWORD_ONLY),
                        password: str = commands.Parameter(name="password",
                                                           description="The password of the login authentication for MySQL",
                                                           kind=commands.Parameter.KEYWORD_ONLY)):
    """
        Gets all databases in MySql Server Connection.
        :param host: Server hostname of MySql Database
        :param user: Username for server authentication
        :param password: Password for server authentication
        :return:
        """

    if host is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('host', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The host (server hostname) of the server you would like to connect to."))

    if user is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('user', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The username of the login authentication for MySQL."))

    if password is None:
        raise commands.MissingRequiredArgument(param=commands.Parameter('password', commands.Parameter.KEYWORD_ONLY,
                                                                        description="The password of the login authentication for MySQL."))

    mydb = None
    mycursor = None
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        dbs = []

        mycursor = mydb.cursor()
        mycursor.execute("SHOW DATABASES")
        results = mycursor.fetchall()
        mydb.commit()

        for x in results:
            if not str(x[0]) in ['information_schema', 'performance_schema', 'mysql', 'phpmyadmin']:
                dbs.append(str(x[0]))
                return dbs
    except Exception as e:
        raise CriticalError.DatabaseError(f"There has been an error getting all databases. {e}")
    finally:
        mycursor.close()
        mydb.close()
