import sqlite3


class BotDB:

    def __init__(self, db_file):
        ##ин. БД
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    #проверяем есть ли пользователь
    def user_exists(self, id):
        result = self.cursor.execute("SELECT id FROM user WHERE id = ?", (id,)).fetchone()
        if result == None:
            return False
        else:
            return True

    ##создание пользователя
    def newUser(self, id):
        self.cursor.execute("INSERT INTO 'user' ('id') VALUES (?)", (id,))
        return self.conn.commit()
    
    ##количество пользователей
    def countUser(self):
        count = self.cursor.execute("SELECT id FROM user").fetchall()
        if count is not None:
            return len(count)
        else:
            return (0)
        
    #сохранение платежа в бд
    def SavePay(self, id, bill_id, comment):
        self.cursor.execute("INSERT INTO user_checkpayment (id, bill_id, comment) VALUES (?, ?, ?)", (id, bill_id, comment))
        return self.conn.commit()
    
    #поиск платежа
    def CheckPay(self, id):
        bill_id = self.cursor.execute("SELECT bill_id FROM user_checkpayment WHERE id = ?", (id,)).fetchall()[-1]
        bill_id = list(bill_id)[0]
        comment = self.cursor.execute("SELECT comment FROM user_checkpayment WHERE bill_id = ?", (bill_id,)).fetchall()[-1]
        comment = list(comment)[0]
        return bill_id, comment
        
    #прибавление сделки
    def addBill(self, id):
        count = self.cursor.execute("SELECT count FROM user WHERE id = ?", (id,)).fetchone()[0]
        count = int(count)+1
        self.cursor.execute("UPDATE user SET count = ? WHERE id = ?", (count, id,))
        return self.conn.commit()

    #get stat
    def get_stat(self, id):
        count = self.cursor.execute("SELECT count FROM user WHERE id = ?", (id,)).fetchone()[0]
        return count
    #добавление покупок
    def add_purchases(self, id, purchases):
        purchases2 = self.cursor.execute("SELECT purchases FROM user WHERE id = ?", (id,)).fetchone()[0]
        purchases2 = str(purchases2).replace('None', '')
        purchases = f"{purchases2} | {purchases}\n"
        self.cursor.execute("UPDATE user SET purchases = ? WHERE id = ?", (purchases, id,))
        return self.conn.commit()
    def get_purchases(self, id):
        purchases = self.cursor.execute("SELECT purchases FROM user WHERE id = ?", (id,)).fetchone()[0]
        return purchases
    #добавить подписку
    def add_subscribe(self, id, count):
        self.cursor.execute("UPDATE user SET subscribe = ? WHERE id = ?", (count, id,))
        return self.conn.commit()
    #проверить подписку
    def check_subscribe(self, id):
        result = int(self.cursor.execute("SELECT subscribe FROM user WHERE id = ?", (id,)).fetchone()[0])
        if result == 0:
            return False
        else:
            return True
    #сохранение задания:
    def create_task(self, id, name, product, price, status):
        self.cursor.execute("INSERT INTO execution (id, name, product, price, status) VALUES (?, ?, ?, ?, ?)", (id, name, product, price, status))
        return self.conn.commit()
    #получение всех заданий
    def get_task(self):
        task = self.cursor.execute("SELECT * FROM execution WHERE status = ?", (0,)).fetchall()
        task = list(task)
        return task
    #получение количество всех сделок
    def get_count_purchase(self):
        task = self.cursor.execute("SELECT * FROM execution", ()).fetchall()
        return len(task)
    #задание сделано
    def task_stop(self, id, task):
        self.cursor.execute("UPDATE execution SET status = ? WHERE id = ? AND product = ?", (1, id, task))
        return self.conn.commit()
    #получение общей сумму сделок
    def get_sum_purchase_all(self):
        task = self.cursor.execute("SELECT price FROM execution", ()).fetchall()
        count = 0
        for i in list(task):
            count+=int(str(i).replace("(", '').replace(")", '').replace(",", ""))
        return f"{count} руб."
    #проверка выполняеться ли задание
    def check_task_Status(self, id):
        result = self.cursor.execute("SELECT id FROM task WHERE id = ?", (id,)).fetchone()
        if result == None:
            return False
        else:
            return True
    #добавление данных в бд когда админ принял задание
    def create_old_task(self, id, task, admin_id):
        self.cursor.execute("INSERT INTO task (id, task, admin_id, message, status) VALUES (?, ?, ?, ?, ?)", (id, task, admin_id, None, 0))
        return self.conn.commit()
    #поставить заказ на паузу
    def pause_task(self, id):
        self.cursor.execute("UPDATE task SET status = ? WHERE id = ?", (1, id,))
        return self.conn.commit()
    #проверка на паузу
    def check_pause(self, id):
        result = self.cursor.execute("SELECT status FROM task WHERE id = ?", (id,)).fetchone()
        if result != None:
            result = int(str(result).replace("(", "").replace(")", "").replace(",", ""))
        if result == 0:
            return False
        if result == None:
            return False
        else:
            return True
    #удаление сообщения
    def delete_message(self, id):
        self.cursor.execute("DELETE message FROM task WHERE id = ?", (id, ))
        return self.conn.commit()
    #сохранение сообщении в бд если стоит пауза
    def save_message(self, id, message):
        temp_message=self.cursor.execute("SELECT message FROM task WHERE id = ?", (id,)).fetchone()
        temp_message=str(temp_message).replace("(", "").replace(")", "").replace(",", "").replace("'", "")
        temp_message=str(temp_message).replace('None', "")
        print(temp_message)
        self.cursor.execute("UPDATE task SET message = ? WHERE id = ?", (f"{temp_message}/new/{message}", id,))
        return self.conn.commit()
    #получение сообщений
    def get_message(self, id):
        result = self.cursor.execute("SELECT message FROM task WHERE id = ?", (id,)).fetchone()
        return result
    # получение id админа который выполняет заказ
    def get_admin_id(self, id):
        result = str(self.cursor.execute("SELECT admin_id FROM task WHERE id = ?", (id,)).fetchone()).replace(",", "").replace("(", "").replace(")", "")
        return int(result)
    #удаление заказа из второй бд после выполнения
    def delete_old_task(self, id):
        self.cursor.execute("DELETE FROM task WHERE id = ?", (id, ))
        return self.conn.commit()
    #получение всех id
    def get_all_id(self):
        result = self.cursor.execute("SELECT id FROM user").fetchall()
        return result
    ##закрытие
    def close(self):
        self.conn.close()
