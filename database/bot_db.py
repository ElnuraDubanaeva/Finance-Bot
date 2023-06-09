import psycopg2
from decouple import config
from services.count import count


class DataBase:

    @classmethod
    def __create_table_info(cls):
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_info (
                id SERIAL PRIMARY KEY,
                date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fullname VARCHAR(50),
                number VARCHAR(20),
                age INTEGER,
                salary INTEGER,
                invests INTEGER,
                needs INTEGER,
                wants INTEGER,
                username VARCHAR(18)
                );
            """
        )
        db.commit()
    
    @classmethod
    def __create_table_needs(cls):
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_needs (
            id SERIAL PRIMARY KEY,
            date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INT,
            FOREIGN KEY (user_id) REFERENCES user_info(id),
            wasted INTEGER,
            info VARCHAR(20)
            );
            """
        )
        db.commit()

    @classmethod
    def __create_table_wants(cls):
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_wants (
            id SERIAL PRIMARY KEY,
            date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INT,
            FOREIGN KEY (user_id) REFERENCES user_info(id),
            wasted INTEGER,
            info VARCHAR(20)
            );
            """
            )        
        db.commit()
    
    @classmethod
    def connect_postgres(cls):
        global db, cursor
        db = psycopg2.connect(
            dbname=config("POSTGRES_DB"),
            user=config("POSTGRES_USER"),
            password=config("POSTGRES_PASSWORD"),
            host=config("POSTGRES_HOST"),
            port=config("POSTGRES_PORT"),
        )
        cursor = db.cursor()

        if cursor and db:
            print("Database successfully connected")
        cls.__create_table_info()
        cls.__create_table_needs()
        cls.__create_table_wants()

    async def insert_info(state):
        async with state.proxy() as data:
            cursor.execute( 
                "INSERT INTO user_info(fullname, number, age, salary, invests, needs, wants, username)"
                "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                tuple(data.values())
            )
        db.commit()
        
    async def insert_needs(state):
        async with state.proxy() as data:
            id_total = await DataBase.get_user_id(data["username"])
            cursor.execute(
                "INSERT INTO user_needs(user_id, wasted, info)"
                "VALUES(%s, %s, %s)",
                (id_total["id"],
                 data["amount"], 
                 data["info"])
            )
        db.commit()
            
    async def insert_wants(state):
        async with state.proxy() as data:
            id_total = await DataBase.get_user_id(data["username"])
            cursor.execute(
                "INSERT INTO user_wants(user_id, wasted, info)"
                "VALUES(%s, %s, %s)",
                (id_total["id"],
                 data["amount"], 
                 data["info"])
            )
        db.commit()

    async def get_user_id(username):
        cursor.execute(
             f"SELECT id, needs, wants, salary FROM user_info WHERE username='{username}';"
         )
        data = cursor.fetchone()
        if data is None:
            return data
        else:
            return {
                "id":data[0],
                "needs": count(data[1], data[3]),
                "wants": count(data[2], data[3])
            }
    

    async def get_user_needs(username):
        user = await DataBase.get_user_id(username)
        if user is not None:
            cursor.execute(f"SELECT * FROM user_needs WHERE user_id='{user['id']}';")
            data = cursor.fetchall()
            av = 0
            for i in data:
                av += i[-2]
            return {
                "total" : user["needs"],
                "available" : user["needs"] - av,
                "username" : username,
                "wasted": av
            }
        else:
            return user
    
    async def get_user_wants(username):
        user = await DataBase.get_user_id(username)
        if user is not None:
            cursor.execute(f"SELECT * FROM user_wants WHERE user_id='{user['id']}';")
            data = cursor.fetchall()
            av = 0
            for i in data:
                av += i[-2]
            return {
                "total" : user["wants"],
                "available" : user["wants"] - av,
                "username" : username,
                "wasted": av
            }
        else:
            return user
