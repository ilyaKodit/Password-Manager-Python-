from tkinter import *
from tkinter.ttk import Combobox
import sqlite3
from tkinter.tix import *

men = [['asd', 'asd'], ['Максим', '123'], ['Василий', '123']]
# men = []

line = (('1', 'yandex.ru', 'mail@yandex.ru', 'qwerty123', 'Моя почта для поиска работы', 'Сайты', '',),
        ('2', 'google.com', 'mail@gmail.com', 'qwert543', 'no comments', 'Сайты', '',),
        ('3', 'yahoo.com', 'mail@yahoo.com', 'qwerty887', '-', 'Сайты', '',))

conn = sqlite3.connect('database.db') # создаём базу данных
cursor = conn.cursor()

# Создаём таблицы в базе данных
try:
    cursor.execute("""
        CREATE TABLE line
        (id text, site text, login text, password text, discription text, category text, favorites text)
        """)
except sqlite3.OperationalError:
    pass

#вставляем данные в таблицу базы данных
cursor.executemany("INSERT INTO line VALUES (?,?,?,?,?,?,?)", line)
conn.commit()
cursor.execute("SELECT * FROM line ORDER BY login")
print(cursor.fetchall())

# cursor.execute("""DELETE FROM line""")
# conn.commit()

def registration():
    frame_auth.place_forget()
    frame_reg.place( relx=0.33, rely=0.3)
    label_reg = Label( frame_reg, text='Регистрация', font='Tahoma 45', fg='grey')
    label_reg.place( x=33, y=10)
    label_auth_name = Label( frame_reg, text='Имя:', width=10, anchor='e')
    label_auth_name.place( x=40, y=109)
    label_auth_password = Label( frame_reg, text='Пароль:', width=10, anchor='e')
    label_auth_password.place( x=40, y=137)
    entry_reg_login = Entry( frame_reg, width=30)
    entry_reg_login.place( x=123, y=110)
    entry_reg_password = Entry( frame_reg, width=30)
    entry_reg_password.place( x=123, y=138)
    button_reg = Button( frame_reg, text='Регистрация', width=20)
    button_reg.place(x=140, y=186)
    label_back_to_auth = Label( frame_reg, text='Вернуться к авторизации')
    label_back_to_auth.place( x=143, y=435)
    button_back_to_auth = Button( frame_reg, text='Авторизация', width=20, command=authorization)
    button_back_to_auth.place(x=140, y=460)

def authorization():
    frame_reg.place_forget()
    frame_auth.place(relx=0.33, rely=0.3)

def login():
    frame_mainwindow.place_forget()
    frame_listwindow.place(x=0, y=63)
    frame_header.place(x=0, y=0)
    frame_footer.place(x=0, y=685)

    label_add_site.place(x=85, y=9)
    label_add_login.place(x=270, y=9)
    label_add_password.place(x=400, y=9)
    label_add_description.place(x=610, y=9)
    label_add_category.place(x=805, y=9)
    label_mainwindow_copyrights.place(x=530, y=7)

    filter_combobox['values'] = (['Фильтр', "Избранное", "Игры", "Сайты", "Приложения"])
    filter_combobox.current(0)
    filter_combobox.place(x=15, y=7)

    checkbutton_favorites.place(x=1000, y=33)

    category_combobox['values'] = (["Игры", "Сайты", "Приложения", "Избранное"])
    category_combobox.current(0)
    category_combobox.place(x=795, y=35)

    entry_add_site.place(x=15, y=35)
    entry_add_login.place(x=230, y=35)
    entry_add_pass.place(x=365, y=35)
    entry_add_description.place(x=500, y=35)

    button_add_values.place(x=905, y=33)
    button_add_filter.place(x=115, y=5)
    button_clear_entry.place(x=1175, y=33)
    button_delete_string.place(x=1175, y=5)
    button_edit_string.place(x=1075, y=5)

def login_correct():
    repeat = False
    if len(men) == 0:
        label_login_error['text'] = 'База данных не содержит пользователей!'
    elif check_login.get() == '' or check_password.get() == '':
        label_login_error['text'] = 'Введите корректный логин и пароль!'
    else:
        for i in range(len(men)):
            if men[i][0] == check_login.get() and men[i][1] == check_password.get():
                login()
                return
            else:
                repeat = True
    if repeat == True:
        label_login_error['text'] = 'Введите корректный логин и пароль!'

def entry_login_enter(event):
    login_correct()

def clear_entry():
    entry_add_site.delete(0, END)
    entry_add_login.delete(0, END)
    entry_add_pass.delete(0, END)
    entry_add_description.delete(0, END)
    category_combobox.current(0)
    check_favorites.set(0)

def table():
    tab = HList(frame_listwindow, columns=7, width=157, height=46, font='Tahoma 11',
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

    for i in range(len(line)):
        index = '%s' % i
        tab.add(index, data="--<%s>--" % i)

        tab.item_create(index, 0, text=line[i][0])
        tab.item_create(index, 1, text=line[i][1])
        tab.item_create(index, 2, text=line[i][2])
        tab.item_create(index, 3, text=line[i][3])
        tab.item_create(index, 4, text=line[i][4])
        tab.item_create(index, 5, text=line[i][5])
        tab.item_create(index, 6, text=line[i][6])


def add_new_record():
    line.append([entry_add_site.get(), entry_add_login.get(), entry_add_pass.get(), entry_add_description.get(), category_combobox.get()])
    table()
    clear_entry()

def new_index():
    pass

root = Tk()
root.geometry('1280x720+300+150')
root.resizable(0, 0)
root.title('Password manager')


check_auth = IntVar()
check_favorites = IntVar()
check_login = StringVar()
check_password = StringVar()

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
label_mainwindow_copyrights = Label( frame_mainwindow, text='All rights reserved © MahimkO & IlyaKodit ™ 2019', font='Tahoma 8 italic')
label_mainwindow_copyrights.place(x=1020, y=695)

entry_auth_login = Entry( frame_auth, width=30, textvariable=check_login)
entry_auth_login.place( x=123, y=110)
entry_auth_password = Entry( frame_auth, width=30, textvariable=check_password)
entry_auth_password.place( x=123, y=138)
entry_auth_login.bind('<Return>', entry_login_enter) # вешаем событие при нажатии Enter на поле ввода логина
entry_auth_password.bind('<Return>', entry_login_enter) # вешаем событие при нажатии Enter на поле ввода пароля

checkbutton_auth = Checkbutton( frame_auth, text='Запомнить меня', variable=check_auth)
checkbutton_auth.place(x=148, y=159)

button_auth = Button( frame_auth, text='Войти', width=20, command=login_correct)
button_auth.place(x=140, y=186)
button_reg_user = Button( frame_auth, text='Регистрация', width=20, command=registration)
button_reg_user.place(x=140, y=460)

# Вторая страница
frame_listwindow = Frame(root, width=1280, height=622)
frame_header = Frame( root, width=1280, height=63, bg='#A1D2B8')
frame_footer = Frame( root, width=1280, height=35, bg='#A1D2B8')

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

filter_combobox = Combobox( frame_footer, width=11, state='readonly')

checkbutton_favorites = Checkbutton( frame_header, text='В избранное', bg='#A1D2B8', activebackground='#A1D2B8', variable=check_favorites)

category_combobox = Combobox( frame_header, width=13, state='readonly')

button_add_values = Button( frame_header, text='Добавить', width=11, command=add_new_record)
button_add_filter = Button( frame_footer, text='Применить', width=11)
button_clear_entry = Button( frame_header, text='Очистить', width=11, command=clear_entry)
button_delete_string = Button( frame_footer, text='Удалить', width=11)
button_edit_string = Button( frame_footer, text='Изменить', width=11)

table()

root.mainloop()
