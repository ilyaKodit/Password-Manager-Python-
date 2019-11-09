from tkinter import *
from tkinter.ttk import Combobox
import sqlite3
from tkinter.tix import *
from tkinter.messagebox import *

#------------------------------- Глобальные переменные --------------------------------

user_name = ''

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users
    (login text, password text)
    """)
cursor.close()
conn.close()

#------------------------------------- ФУНКЦИИ ----------------------------------------


def registration_window():
    frame_auth.place_forget()
    frame_reg.place( relx=0.33, rely=0.3)

    label_reg = Label( frame_reg, text='Регистрация', font='Tahoma 45', fg='grey')
    label_reg.place( x=33, y=10)
    label_auth_name = Label( frame_reg, text='Имя:', width=10, anchor='e')
    label_auth_name.place( x=40, y=109)
    label_auth_password = Label( frame_reg, text='Пароль:', width=10, anchor='e')
    label_auth_password.place( x=40, y=137)
    label_reg_error.place(x=50, y=225)

    entry_reg_login.place( x=123, y=110)
    entry_reg_password.place( x=123, y=138)

    button_reg = Button( frame_reg, text='Регистрация', width=20, command=new_registration)
    button_reg.place(x=140, y=186)

    label_back_to_auth = Label( frame_reg, text='Вернуться к авторизации')
    label_back_to_auth.place( x=143, y=435)

    button_back_to_auth = Button( frame_reg, text='Авторизация', width=20, command=back_to_authorization)
    button_back_to_auth.place(x=140, y=460)


def back_to_authorization():
    frame_reg.place_forget()
    frame_auth.place(relx=0.33, rely=0.3)


def work_window():
    frame_mainwindow.place_forget()
    frame_listwindow.place(x=0, y=63)
    frame_header.place(x=0, y=0)
    frame_footer.place(x=0, y=674)

    label_add_site.place(x=85, y=9)
    label_add_login.place(x=270, y=9)
    label_add_password.place(x=400, y=9)
    label_add_description.place(x=610, y=9)
    label_add_category.place(x=805, y=9)
    label_mainwindow_copyrights.place(x=530, y=12)

    filter_combobox['values'] = (['Фильтр', "Избранное", "Игры", "Сайты", "Приложения"])
    filter_combobox.current(0)
    filter_combobox.place(x=15, y=12)

    checkbutton_favorites.place(x=1000, y=33)

    category_combobox['values'] = (["Игры", "Сайты", "Приложения"])
    category_combobox.current(0)
    category_combobox.place(x=795, y=35)

    entry_add_site.place(x=15, y=35)
    entry_add_login.place(x=230, y=35)
    entry_add_pass.place(x=365, y=35)
    entry_add_description.place(x=500, y=35)

    button_add_values.place(x=905, y=33)
    button_add_filter.place(x=115, y=10)
    button_clear_entry.place(x=1175, y=33)
    button_delete_string.place(x=1175, y=10)
    button_edit_string.place(x=1075, y=10)
    button_clear_filter.place(x=210, y=10)
    button_change_user.place(x=925, y=10)


def new_registration():
    user = []
    user.append((check_login_reg.get(), check_password_reg.get()))

    if registration_correct() == True:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.executemany("INSERT INTO users VALUES (?, ?)", (user[0],))
        conn.commit()

        cursor.close()
        conn.close()

        entry_reg_login.delete(0, END)
        entry_reg_password.delete(0, END)
        label_reg_error['text'] = ''
        back_to_authorization()
    else:
        label_reg_error['text'] = 'Такой пользователь уже существует!'


def registration_correct():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users
        (login text, password text)
        """)

    cursor.execute("SELECT * FROM users")
    query_result = cursor.fetchall()

    cursor.close()
    conn.close()
    if len(query_result) == 0:
        return True


    for i in range(len(query_result)):
        if query_result[i][0] == check_login_reg.get() and query_result[i][1] == check_password_reg.get():
            return False

    return True


def login_correct():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    query_result = cursor.fetchall()

    cursor.close()
    conn.close()

    if check_login_auth.get() == '' or check_password_auth.get() == '':
        label_login_error['text'] = 'Введите корректный логин и пароль!'
        return

    for i in range(len(query_result)):
        if check_login_auth.get() == query_result[i][0] and check_password_auth.get() == query_result[i][1]:
            entry_auth_login.delete(0, END)
            entry_auth_password.delete(0, END)
            label_login_error['text'] = ''

            global user_name
            user_name = query_result[i][0] + query_result[i][1]

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS {0}
                    (id text, site text, login text, password text, discription text, category text, favorites text)
                    """.format(user_name))
            cursor.close()
            conn.close()

            work_window()
            load_table()
            return
    else:
        label_login_error['text'] = 'Такой пользователь не найден!'


def entry_login_enter(event):
    login_correct()


def clear_entry():
    entry_add_site.delete(0, END)
    entry_add_login.delete(0, END)
    entry_add_pass.delete(0, END)
    entry_add_description.delete(0, END)
    category_combobox.current(0)
    check_favorites.set(0)


def create_id():
    # Получаем все id из базы данных
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM {0}".format(user_name))
    query_result = cursor.fetchall()

    cursor.close()
    conn.close()

    # узнаём какой id последний и увеличиваем на 1 чтобы вернуть как результат функции
    if len(query_result) == 0:
        return 1
    result = 0
    for i in range(len(query_result)):
        result = query_result[i]
    result = result[0]
    result = int(result)
    result += 1
    return result


def load_table():
    # Получаем из базы всё что в ней хранится и заполняем таблицу
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM {0}".format(user_name))
    tbl = cursor.fetchall()

    cursor.close()
    conn.close()

    tab = HList(frame_listwindow, columns=9, width=157, height=32, font='Tahoma 11',
        padx=15, pady=5, selectbackground='#C8ECBE', selectforeground='black', header=True)
    tab.grid(row=0, column=0)

    scroll = Scrollbar(frame_listwindow, width=20, command=tab.yview)
    tab['yscrollcommand'] = scroll.set
    scroll.grid(row=0, column=1, sticky='nswe')

    tab.header_create(0, text="№")
    tab.header_create(1, text="Название")
    tab.header_create(2, text="Логин")
    tab.header_create(3, text="Пароль")
    tab.header_create(4, text="Описание")
    tab.header_create(5, text="Категория")
    tab.header_create(6, text="Избранное")
    tab.header_create(7, text="Изменить")
    tab.header_create(8, text="Удалить")
    counter = 1


    for i in range(len(tbl)):
        index = '%s' % i
        tab.add(index, data=tbl[i][0])

        tab.item_create(index, 0, text=counter)
        tab.item_create(index, 1, text=tbl[i][1])
        tab.item_create(index, 2, text=tbl[i][2])
        tab.item_create(index, 3, text=tbl[i][3])
        tab.item_create(index, 4, text=tbl[i][4])
        tab.item_create(index, 5, text=tbl[i][5])
        tab.item_create(index, 6, text=tbl[i][6])

        def transorm(index):
            def f():
                check_sub_site = StringVar()
                check_sub_login = StringVar()
                check_sub_password = StringVar()
                check_sub_description = StringVar()

                def apply():
                    s = check_sub_site.get()
                    l = check_sub_login.get()
                    p = check_sub_password.get()
                    d = check_sub_description.get()
                    c = category_sub_combobox.get()
                    f = favorites_sub_combobox.get()

                    conn = sqlite3.connect('database.db')
                    cursor = conn.cursor()

                    cursor.execute("SELECT * FROM {0} WHERE id = {1}".format(user_name, tab.info_data(index)))
                    result = cursor.fetchall()
                    result = result[0]

                    if s == '':
                        s = result[1]
                    if l == '':
                        l = result[2]
                    if p == '':
                        p = result[3]
                    if d == '':
                        d = result[4]
                    if c == '':
                        c = result[5]

                    if f == '':
                        f = result[6]
                    elif f == 'В избранное':
                        f = '★'
                    else:
                        f = ''

                    list = []
                    list.append((tab.info_data(index), s, l, p, d, c, f))

                    cursor.execute("""
                        UPDATE {0} SET site = '{1}' WHERE id = '{2}'
                        """.format(user_name, list[0][1], tab.info_data(index)))
                    conn.commit()

                    cursor.execute("""
                        UPDATE {0} SET login = '{1}' WHERE id = '{2}'
                        """.format(user_name, list[0][2], tab.info_data(index)))
                    conn.commit()

                    cursor.execute("""
                        UPDATE {0} SET password = '{1}' WHERE id = '{2}'
                        """.format(user_name, list[0][3], tab.info_data(index)))
                    conn.commit()

                    cursor.execute("""
                        UPDATE {0} SET discription = '{1}' WHERE id = '{2}'
                        """.format(user_name, list[0][4], tab.info_data(index)))
                    conn.commit()

                    cursor.execute("""
                        UPDATE {0} SET category = '{1}' WHERE id = '{2}'
                        """.format(user_name, list[0][5], tab.info_data(index)))
                    conn.commit()

                    cursor.execute("""
                        UPDATE {0} SET favorites = '{1}' WHERE id = '{2}'
                        """.format(user_name, list[0][6], tab.info_data(index)))
                    conn.commit()

                    cursor.close()
                    conn.close()

                    load_table()
                    sub.destroy()
                    # print(s, l, p, d, c, f)

                sub = Toplevel(root, bg='#A1D2B8')
                sub.geometry('400x270+150+100')
                sub.resizable(0, 0)

                label_sub = Label(sub, text='''Введите данные, которые хотите изменить!''', font='Tahoma 14', bg='#A1D2B8')
                label_sub.place(x=4, y=15)

                label_sub_site = Label(sub, text='Название', font='Tahoma 11', bg='#A1D2B8')
                label_sub_site.place(x=10, y=50)
                entry_sub_site = Entry(sub, width=25, font='Tahoma 11', textvariable=check_sub_site)
                entry_sub_site.place(x=100, y=50)

                label_sub_login = Label(sub, text='Логин', font='Tahoma 11', bg='#A1D2B8')
                label_sub_login.place(x=10, y=75)
                entry_sub_login = Entry(sub, width=25, font='Tahoma 11', textvariable=check_sub_login)
                entry_sub_login.place(x=100, y=75)

                label_sub_password = Label(sub, text='Пароль', font='Tahoma 11', bg='#A1D2B8')
                label_sub_password.place(x=10, y=100)
                entry_sub_password = Entry(sub, width=25, font='Tahoma 11', textvariable=check_sub_password)
                entry_sub_password.place(x=100, y=100)

                label_sub_description = Label(sub, text='Описание', font='Tahoma 11', bg='#A1D2B8')
                label_sub_description.place(x=10, y=125)
                entry_sub_description = Entry(sub, width=25, font='Tahoma 11', textvariable=check_sub_description)
                entry_sub_description.place(x=100, y=125)

                label_sub_category = Label(sub, text='Категория', font='Tahoma 11', bg='#A1D2B8')
                label_sub_category.place(x=10, y=150)
                category_sub_combobox = Combobox(sub, width=19, state='readonly')
                category_sub_combobox['values'] = (["", "Игры", "Сайты", "Приложения"])
                category_sub_combobox.current(0)
                category_sub_combobox.place(x=100, y=150)

                label_sub_favorites = Label(sub, text='Избранное', font='Tahoma 11', bg='#A1D2B8')
                label_sub_favorites.place(x=10, y=175)
                favorites_sub_combobox = Combobox(sub, width=19, state='readonly')
                favorites_sub_combobox['values'] = (["", "В избранное", "Убрать из избранного"])
                favorites_sub_combobox.current(0)
                favorites_sub_combobox.place(x=100, y=175)

                button_sub = Button(sub, text='Применить', command=apply)
                button_sub.place(x=160, y=220)
            return f

        def delete(index):
            def f():
                answer = askokcancel('Удаление строки', 'Удалить строку?')
                if answer == 1:
                    print(tab.info_data(index))

                    conn = sqlite3.connect('database.db')
                    cursor = conn.cursor()

                    cursor.execute("DELETE FROM {0} WHERE id = {1}".format(user_name, tab.info_data(index)))
                    conn.commit()

                    cursor.close()
                    conn.close()

                    load_table()
            return f

        button_transform = Button(tab, text="↻", width=3, command=transorm(index))
        tab.item_create(index, 7, itemtype=WINDOW, window=button_transform)

        button_del = Button(tab, text="✖", width=3, command=delete(index))
        tab.item_create(index, 8, itemtype=WINDOW, window=button_del)

        counter += 1

        # print(tab.info_data(index))



def add_new_record():
    i = 0 + create_id()
    s = entry_add_site.get()
    l = entry_add_login.get()
    p = entry_add_pass.get()
    d = entry_add_description.get()
    c = category_combobox.get()
    f = ''

    if check_favorites.get() == 1:
        f = '★'

    # заполняем список полученными данными
    list = []
    list.append((i, s, l, p, d, c, f))
    clear_entry()

    # вставляем данные в таблицу базы данных
    conn = sqlite3.connect('database.db') # создаём базу данных
    cursor = conn.cursor()

    cursor.executemany("INSERT INTO {0} VALUES (?,?,?,?,?,?,?)".format(user_name), (list[0],))
    conn.commit()

    cursor.close()
    conn.close()

    load_table()


def use_filter(filter_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM {0}".format(user_name))
    tbl = cursor.fetchall()

    cursor.close()
    conn.close()

    tab = HList(frame_listwindow, columns=9, width=157, height=32, font='Tahoma 11',
        padx=15, pady=5, selectbackground='#C8ECBE', selectforeground='black', header=True)
    tab.grid(row=0, column=0)

    scroll = Scrollbar(frame_listwindow, width=20, command=tab.yview)
    tab['yscrollcommand'] = scroll.set
    scroll.grid(row=0, column=1, sticky='nswe')

    tab.header_create(0, text="№")
    tab.header_create(1, text="Название")
    tab.header_create(2, text="Логин")
    tab.header_create(3, text="Пароль")
    tab.header_create(4, text="Описание")
    tab.header_create(5, text="Категория")
    tab.header_create(6, text="Избранное")
    tab.header_create(7, text="Удалить")
    tab.header_create(8, text="Изменить")

    counter = 1

    for i in range(len(tbl)):
        if tbl[i][5] == filter_name:
            index = '%s' % i
            tab.add(index, data=tbl[i][0])

            tab.item_create(index, 0, text=counter)
            tab.item_create(index, 1, text=tbl[i][1])
            tab.item_create(index, 2, text=tbl[i][2])
            tab.item_create(index, 3, text=tbl[i][3])
            tab.item_create(index, 4, text=tbl[i][4])
            tab.item_create(index, 5, text=tbl[i][5])
            tab.item_create(index, 6, text=tbl[i][6])

            def transorm(index):
                def f():
                    check_sub_site = StringVar()
                    check_sub_login = StringVar()
                    check_sub_password = StringVar()
                    check_sub_description = StringVar()

                    def apply():
                        s = check_sub_site.get()
                        l = check_sub_login.get()
                        p = check_sub_password.get()
                        d = check_sub_description.get()
                        c = category_sub_combobox.get()
                        f = favorites_sub_combobox.get()

                        conn = sqlite3.connect('database.db')
                        cursor = conn.cursor()

                        cursor.execute("SELECT * FROM {0} WHERE id = {1}".format(user_name, tab.info_data(index)))
                        result = cursor.fetchall()
                        result = result[0]

                        if s == '':
                            s = result[1]
                        if l == '':
                            l = result[2]
                        if p == '':
                            p = result[3]
                        if d == '':
                            d = result[4]
                        if c == '':
                            c = result[5]

                        if f == '':
                            f = result[6]
                        elif f == 'В избранное':
                            f = '★'
                        else:
                            f = ''

                        list = []
                        list.append((tab.info_data(index), s, l, p, d, c, f))

                        cursor.execute("""
                            UPDATE {0} SET site = '{1}' WHERE id = '{2}'
                            """.format(user_name, list[0][1], tab.info_data(index)))
                        conn.commit()

                        cursor.execute("""
                            UPDATE {0} SET login = '{1}' WHERE id = '{2}'
                            """.format(user_name, list[0][2], tab.info_data(index)))
                        conn.commit()

                        cursor.execute("""
                            UPDATE {0} SET password = '{1}' WHERE id = '{2}'
                            """.format(user_name, list[0][3], tab.info_data(index)))
                        conn.commit()

                        cursor.execute("""
                            UPDATE {0} SET discription = '{1}' WHERE id = '{2}'
                            """.format(user_name, list[0][4], tab.info_data(index)))
                        conn.commit()

                        cursor.execute("""
                            UPDATE {0} SET category = '{1}' WHERE id = '{2}'
                            """.format(user_name, list[0][5], tab.info_data(index)))
                        conn.commit()

                        cursor.execute("""
                            UPDATE {0} SET favorites = '{1}' WHERE id = '{2}'
                            """.format(user_name, list[0][6], tab.info_data(index)))
                        conn.commit()

                        cursor.close()
                        conn.close()

                        load_table()
                        sub.destroy()
                        # print(s, l, p, d, c, f)

                    sub = Toplevel(root, bg='#A1D2B8')
                    sub.geometry('400x270+150+100')
                    sub.resizable(0, 0)

                    label_sub = Label(sub, text='''Введите данные, которые хотите изменить!''', font='Tahoma 14', bg='#A1D2B8')
                    label_sub.place(x=4, y=15)

                    label_sub_site = Label(sub, text='Название', font='Tahoma 11', bg='#A1D2B8')
                    label_sub_site.place(x=10, y=50)
                    entry_sub_site = Entry(sub, width=25, font='Tahoma 11', textvariable=check_sub_site)
                    entry_sub_site.place(x=100, y=50)

                    label_sub_login = Label(sub, text='Логин', font='Tahoma 11', bg='#A1D2B8')
                    label_sub_login.place(x=10, y=75)
                    entry_sub_login = Entry(sub, width=25, font='Tahoma 11', textvariable=check_sub_login)
                    entry_sub_login.place(x=100, y=75)

                    label_sub_password = Label(sub, text='Пароль', font='Tahoma 11', bg='#A1D2B8')
                    label_sub_password.place(x=10, y=100)
                    entry_sub_password = Entry(sub, width=25, font='Tahoma 11', textvariable=check_sub_password)
                    entry_sub_password.place(x=100, y=100)

                    label_sub_description = Label(sub, text='Описание', font='Tahoma 11', bg='#A1D2B8')
                    label_sub_description.place(x=10, y=125)
                    entry_sub_description = Entry(sub, width=25, font='Tahoma 11', textvariable=check_sub_description)
                    entry_sub_description.place(x=100, y=125)

                    label_sub_category = Label(sub, text='Категория', font='Tahoma 11', bg='#A1D2B8')
                    label_sub_category.place(x=10, y=150)
                    category_sub_combobox = Combobox(sub, width=19, state='readonly')
                    category_sub_combobox['values'] = (["", "Игры", "Сайты", "Приложения"])
                    category_sub_combobox.current(0)
                    category_sub_combobox.place(x=100, y=150)

                    label_sub_favorites = Label(sub, text='Избранное', font='Tahoma 11', bg='#A1D2B8')
                    label_sub_favorites.place(x=10, y=175)
                    favorites_sub_combobox = Combobox(sub, width=19, state='readonly')
                    favorites_sub_combobox['values'] = (["", "В избранное", "Убрать из избранного"])
                    favorites_sub_combobox.current(0)
                    favorites_sub_combobox.place(x=100, y=175)

                    button_sub = Button(sub, text='Применить', command=apply)
                    button_sub.place(x=160, y=220)
                return f

            def delete(index):
                def f():
                    answer = askokcancel('Удаление строки', 'Удалить строку?')
                    if answer == 1:
                        print(tab.info_data(index))

                        conn = sqlite3.connect('database.db')
                        cursor = conn.cursor()

                        cursor.execute("DELETE FROM {0} WHERE id = {1}".format(user_name, tab.info_data(index)))
                        conn.commit()

                        cursor.close()
                        conn.close()

                        filters()
                return f

            button_transform = Button(tab, text="↻", width=3, command=transorm(index))
            tab.item_create(index, 7, itemtype=WINDOW, window=button_transform)

            button_del = Button(tab, text="✖", width=3, command=delete(index))
            tab.item_create(index, 8, itemtype=WINDOW, window=button_del)

            counter += 1
            # print(tab.info_data(index))

        if tbl[i][6] == filter_name:
            index = '%s' % i
            tab.add(index, data=tbl[i][0])

            tab.item_create(index, 0, text=counter)
            tab.item_create(index, 1, text=tbl[i][1])
            tab.item_create(index, 2, text=tbl[i][2])
            tab.item_create(index, 3, text=tbl[i][3])
            tab.item_create(index, 4, text=tbl[i][4])
            tab.item_create(index, 5, text=tbl[i][5])
            tab.item_create(index, 6, text=tbl[i][6])

            def transorm(index):
                def f():
                    check_sub_site = StringVar()
                    check_sub_login = StringVar()
                    check_sub_password = StringVar()
                    check_sub_description = StringVar()

                    def apply():
                        s = check_sub_site.get()
                        l = check_sub_login.get()
                        p = check_sub_password.get()
                        d = check_sub_description.get()
                        c = category_sub_combobox.get()
                        f = favorites_sub_combobox.get()

                        conn = sqlite3.connect('database.db')
                        cursor = conn.cursor()

                        cursor.execute("SELECT * FROM {0} WHERE id = {1}".format(user_name, tab.info_data(index)))
                        result = cursor.fetchall()
                        result = result[0]

                        if s == '':
                            s = result[1]
                        if l == '':
                            l = result[2]
                        if p == '':
                            p = result[3]
                        if d == '':
                            d = result[4]
                        if c == '':
                            c = result[5]

                        if f == '':
                            f = result[6]
                        elif f == 'В избранное':
                            f = '★'
                        else:
                            f = ''

                        list = []
                        list.append((tab.info_data(index), s, l, p, d, c, f))

                        cursor.execute("""
                            UPDATE {0} SET site = '{1}' WHERE id = '{2}'
                            """.format(user_name, list[0][1], tab.info_data(index)))
                        conn.commit()

                        cursor.execute("""
                            UPDATE {0} SET login = '{1}' WHERE id = '{2}'
                            """.format(user_name, list[0][2], tab.info_data(index)))
                        conn.commit()

                        cursor.execute("""
                            UPDATE {0} SET password = '{1}' WHERE id = '{2}'
                            """.format(user_name, list[0][3], tab.info_data(index)))
                        conn.commit()

                        cursor.execute("""
                            UPDATE {0} SET discription = '{1}' WHERE id = '{2}'
                            """.format(user_name, list[0][4], tab.info_data(index)))
                        conn.commit()

                        cursor.execute("""
                            UPDATE {0} SET category = '{1}' WHERE id = '{2}'
                            """.format(user_name, list[0][5], tab.info_data(index)))
                        conn.commit()

                        cursor.execute("""
                            UPDATE {0} SET favorites = '{1}' WHERE id = '{2}'
                            """.format(user_name, list[0][6], tab.info_data(index)))
                        conn.commit()

                        cursor.close()
                        conn.close()

                        load_table()
                        sub.destroy()
                        # print(s, l, p, d, c, f)

                    sub = Toplevel(root, bg='#A1D2B8')
                    sub.geometry('400x270+150+100')
                    sub.resizable(0, 0)

                    label_sub = Label(sub, text='''Введите данные, которые хотите изменить!''', font='Tahoma 14', bg='#A1D2B8')
                    label_sub.place(x=4, y=15)

                    label_sub_site = Label(sub, text='Название', font='Tahoma 11', bg='#A1D2B8')
                    label_sub_site.place(x=10, y=50)
                    entry_sub_site = Entry(sub, width=25, font='Tahoma 11', textvariable=check_sub_site)
                    entry_sub_site.place(x=100, y=50)

                    label_sub_login = Label(sub, text='Логин', font='Tahoma 11', bg='#A1D2B8')
                    label_sub_login.place(x=10, y=75)
                    entry_sub_login = Entry(sub, width=25, font='Tahoma 11', textvariable=check_sub_login)
                    entry_sub_login.place(x=100, y=75)

                    label_sub_password = Label(sub, text='Пароль', font='Tahoma 11', bg='#A1D2B8')
                    label_sub_password.place(x=10, y=100)
                    entry_sub_password = Entry(sub, width=25, font='Tahoma 11', textvariable=check_sub_password)
                    entry_sub_password.place(x=100, y=100)

                    label_sub_description = Label(sub, text='Описание', font='Tahoma 11', bg='#A1D2B8')
                    label_sub_description.place(x=10, y=125)
                    entry_sub_description = Entry(sub, width=25, font='Tahoma 11', textvariable=check_sub_description)
                    entry_sub_description.place(x=100, y=125)

                    label_sub_category = Label(sub, text='Категория', font='Tahoma 11', bg='#A1D2B8')
                    label_sub_category.place(x=10, y=150)
                    category_sub_combobox = Combobox(sub, width=19, state='readonly')
                    category_sub_combobox['values'] = (["", "Игры", "Сайты", "Приложения"])
                    category_sub_combobox.current(0)
                    category_sub_combobox.place(x=100, y=150)

                    label_sub_favorites = Label(sub, text='Избранное', font='Tahoma 11', bg='#A1D2B8')
                    label_sub_favorites.place(x=10, y=175)
                    favorites_sub_combobox = Combobox(sub, width=19, state='readonly')
                    favorites_sub_combobox['values'] = (["", "В избранное", "Убрать из избранного"])
                    favorites_sub_combobox.current(0)
                    favorites_sub_combobox.place(x=100, y=175)

                    button_sub = Button(sub, text='Применить', command=apply)
                    button_sub.place(x=160, y=220)
                return f

            def delete(index):
                def f():
                    answer = askokcancel('Удаление строки', 'Удалить строку?')
                    if answer == 1:
                        print(tab.info_data(index))

                        conn = sqlite3.connect('database.db')
                        cursor = conn.cursor()

                        cursor.execute("DELETE FROM {0} WHERE id = {1}".format(user_name, tab.info_data(index)))
                        conn.commit()

                        cursor.close()
                        conn.close()

                        filters()
                return f

            button_transform = Button(tab, text="↻", width=3, command=transorm(index))
            tab.item_create(index, 7, itemtype=WINDOW, window=button_transform)

            button_del = Button(tab, text="✖", width=3, command=delete(index))
            tab.item_create(index, 8, itemtype=WINDOW, window=button_del)

            counter += 1
            # print(tab.info_data(index))


def filters():
    if check_filter.get() == 'Игры':
        use_filter('Игры')

    if check_filter.get() == 'Сайты':
        use_filter('Сайты')

    if check_filter.get() == 'Приложения':
        use_filter('Приложения')

    if check_filter.get() == 'Избранное':
        use_filter('★')

def clear_filter():
    filter_combobox.current(0)
    load_table()

def change_user():
    frame_listwindow.place_forget()
    frame_header.place_forget()
    frame_footer.place_forget()
    frame_mainwindow.place(x=0, y=0)

def want_to_change_user():
    answer = askokcancel('Сменить пользователя', 'Сменить пользователя?')
    if answer == 1:
        change_user()



#----------------------------------------------- TKINTER -----------------------------------------------


root = Tk()
root.geometry('1280x720+100+50')
root.resizable(0, 0)
root.title('Password manager')


check_remember_me = IntVar()
check_favorites = IntVar()
check_login_auth = StringVar()
check_password_auth = StringVar()
check_login_reg = StringVar()
check_password_reg = StringVar()

frame_mainwindow = Frame( root, width=1280, height=720)
frame_mainwindow.place(x=0, y=0)
frame_auth = Frame( frame_mainwindow, width=426, height=500)
frame_auth.place( relx=0.33, rely=0.3)
frame_reg = Frame( frame_mainwindow, width=426, height=500)

label_title = Label( frame_mainwindow, text='Password manager', font='Tahoma 45', fg='#A1D2B8')
label_title.place( relx=0.3, rely=0.1)
label_auth = Label( frame_auth, text='Авторизация', font='Tahoma 45', fg='grey')
label_auth.place( x=33, y=10)
label_auth_name = Label( frame_auth, text='Имя:', width=10, anchor='e')
label_auth_name.place( x=40, y=109)
label_auth_password = Label( frame_auth, text='Пароль:', width=10, anchor='e')
label_auth_password.place( x=40, y=137)
label_reg_button = Label( frame_auth, text='Если у Вас нет учетной записи, то Вы можете зарегистрироваться')
label_reg_button.place( x=30, y=436)
label_login_error = Label( frame_auth, width=37, font='Tahoma 13 italic', fg='#F7444D')
label_login_error.place(x=50, y=225)
label_reg_error = Label( frame_reg, width=37, font='Tahoma 13 italic', fg='#F7444D')
label_mainwindow_copyrights = Label( frame_mainwindow, text='All rights reserved © MahimkO & IlyaKodit ™ 2019', font='Tahoma 8 italic')
label_mainwindow_copyrights.place(x=1020, y=695)

entry_auth_login = Entry( frame_auth, width=30, textvariable=check_login_auth)
entry_auth_login.place( x=123, y=110)
entry_auth_password = Entry( frame_auth, width=30, textvariable=check_password_auth)
entry_auth_password.place( x=123, y=138)
entry_auth_login.bind('<Return>', entry_login_enter) # вешаем событие при нажатии Enter на поле ввода логина
entry_auth_password.bind('<Return>', entry_login_enter) # вешаем событие при нажатии Enter на поле ввода пароля

entry_reg_login = Entry( frame_reg, width=30, textvariable=check_login_reg)
entry_reg_password = Entry( frame_reg, width=30, textvariable=check_password_reg)

checkbutton_auth = Checkbutton( frame_auth, text='Запомнить меня', variable=check_remember_me)
checkbutton_auth.place(x=148, y=159)

button_auth = Button( frame_auth, text='Войти', width=20, command=login_correct)
button_auth.place(x=140, y=186)
button_reg_user = Button( frame_auth, text='Регистрация', width=20, command=registration_window)
button_reg_user.place(x=140, y=460)

# --------------------------------- ВТОРАЯ СТРАНИЦА ---------------------------------

check_filter = StringVar()

frame_listwindow = Frame(root, width=1280, height=622)
frame_header = Frame( root, width=1280, height=63, bg='#A1D2B8')
frame_footer = Frame( root, width=1280, height=46, bg='#A1D2B8')

entry_add_site = Entry( frame_header, width=25, font='Tahoma 11')
entry_add_login = Entry( frame_header, width=15, font='Tahoma 11')
entry_add_pass = Entry( frame_header, width=15, font='Tahoma 11')
entry_add_description = Entry( frame_header, width=35, font='Tahoma 11')

label_add_site = Label( frame_header, bg='#A1D2B8', font='Tahoma 11 italic', text='Название')
label_add_login = Label( frame_header, bg='#A1D2B8', font='Tahoma 11 italic', text='Логин')
label_add_password = Label( frame_header, bg='#A1D2B8', font='Tahoma 11 italic', text='Пароль')
label_add_description = Label( frame_header, bg='#A1D2B8', font='Tahoma 11 italic', text='Описание')
label_add_category = Label( frame_header, bg='#A1D2B8', font='Tahoma 11 italic', text='Категория')
label_mainwindow_copyrights = Label( frame_footer, text='All rights reserved © MahimkO & IlyaKodit ™ 2019',
    font='Tahoma 8 italic', bg='#A1D2B8')

filter_combobox = Combobox( frame_footer, width=11, state='readonly', textvariable=check_filter)

checkbutton_favorites = Checkbutton( frame_header, text='В избранное', bg='#A1D2B8', activebackground='#A1D2B8', variable=check_favorites)

category_combobox = Combobox( frame_header, width=13, state='readonly')

button_add_values = Button( frame_header, text='Добавить', width=11, command=add_new_record)
button_add_filter = Button( frame_footer, text='Применить', width=11, command=filters)
button_clear_entry = Button( frame_header, text='Очистить', width=11, command=clear_entry)
button_delete_string = Button( frame_footer, text='Удалить', width=11)
button_edit_string = Button( frame_footer, text='Изменить', width=11)
button_clear_filter = Button( frame_footer, text='Сбросить фильтр', width=15, command=clear_filter)
button_change_user = Button ( frame_footer, text='Сменить пользователя', width=19, command=want_to_change_user)
root.mainloop()


#------------------------------------------ Справочная информация ------------------------------------


# Если нужно удалить таблицу
# cursor.execute("DROP TABLE users")

# Если нужно очистить таблицу
# cursor.execute("DELETE FROM line")
# conn.commit()

