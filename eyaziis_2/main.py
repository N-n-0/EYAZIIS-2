import os
from tkinter import *

from AlphabetMethod import AlphabetMethod
from GramsMethod import GramsMethod
from NeuralMethod import NeuralMethod

root = Tk()
root.configure(bg='gray')
root.title("lr2")
root.geometry("1300x800")
entry_path = Entry(width=100)
label_1 = Label(text="Введите в поле ввода путь к файлу, содержимое которого хотите проверить. ", bg='gray', fg="black", justify='left')
label_2 = Label(text="", bg='gray', fg="black", justify='left')


grams_method = GramsMethod(r"C:\Users\nikit\OneDrive\Desktop\bsuir\eyaziis_2\dataset\russian.html", r"C:\Users\nikit\OneDrive\Desktop\bsuir\eyaziis_2\dataset\german.html")
alphabet_method = AlphabetMethod(r"C:\Users\nikit\OneDrive\Desktop\bsuir\eyaziis_2\dataset\russian.html", r"C:\Users\nikit\OneDrive\Desktop\bsuir\eyaziis_2\dataset\german.html")
neural_method = NeuralMethod(r"C:\Users\nikit\OneDrive\Desktop\bsuir\eyaziis_2\dataset\russian.html", r"C:\Users\nikit\OneDrive\Desktop\bsuir\eyaziis_2\dataset\german.html")

def exit_button_handler():
    quit()


def grams_method_button():
    file_path = entry_path.get()
    abs_path = os.path.abspath(file_path)
    import pathlib
    uri = pathlib.Path(abs_path).as_uri()
    import time
    start_time = time.time()
    lang, rus_measure, ger_measure = grams_method.get_language(file_path)
    content = uri + ' -- ' + lang
    label_2['text'] = content + "\n--- %s seconds ---" % (time.time() - start_time)
    path = r'C:\Users\nikit\OneDrive\Desktop\bsuir\eyaziis_2\dataset\out' + '\\' + str(
        len(os.listdir(r'C:\Users\nikit\OneDrive\Desktop\bsuir\eyaziis_2\dataset\out'))) + ".txt"
    with open(path, 'a', encoding='utf-8') as file:
        file.write(content)
        file.write("\nGrams method:\n")
        file.write("Russian:" + str(rus_measure))
        file.write("\nGerman:" + str(ger_measure))
        abs_path = os.path.abspath(path)
        import pathlib
        uri = pathlib.Path(abs_path).as_uri()
        label_1['text'] = 'Saved -- ' + uri


def alphabet_method_button():
    file_path = entry_path.get()
    abs_path = os.path.abspath(file_path)
    import pathlib
    uri = pathlib.Path(abs_path).as_uri()
    import time
    start_time = time.time()
    lang, rus_measure, ger_measure = alphabet_method.get_language(file_path)
    content = uri + ' -- ' + lang
    label_2['text'] = content + "\n--- %s seconds ---" % (time.time() - start_time)
    path = r'C:\Users\nikit\OneDrive\Desktop\bsuir\eyaziis_2\dataset\out' + '\\' + str(
        len(os.listdir(r'C:\Users\nikit\OneDrive\Desktop\bsuir\eyaziis_2\dataset\out'))) + ".txt"
    with open(path, 'a', encoding='utf-8') as file:
        file.write(content)
        file.write("\nAlphabet method:\n")
        file.write("Russian:" + str(rus_measure) + "%\n")
        file.write("German:" + str(ger_measure) + "%")
        abs_path = os.path.abspath(path)
        import pathlib
        uri = pathlib.Path(abs_path).as_uri()
        label_1['text'] = 'Saved -- ' + uri


def neural_method_button():
    file_path = entry_path.get()
    abs_path = os.path.abspath(file_path)
    import pathlib
    uri = pathlib.Path(abs_path).as_uri()
    import time
    start_time = time.time()
    content = uri + ' -- ' + neural_method.get_language(file_path)
    label_2['text'] = content + "\n--- %s seconds ---" % (time.time() - start_time)
    path = r'C:\Users\nikit\OneDrive\Desktop\bsuir\eyaziis_2\dataset\out' + '\\' + str(len(os.listdir(r'C:\Users\nikit\OneDrive\Desktop\bsuir\eyaziis_2\dataset\out'))) + ".txt"
    with open(path, 'a', encoding='utf-8') as file:
        file.write(content)
        abs_path = os.path.abspath(path)
        import pathlib
        uri = pathlib.Path(abs_path).as_uri()
        label_1['text'] = 'Saved -- ' + uri


def help_button():
    if label_1['text'] == "Введите в поле ввода путь к файлу, содержимое которого хотите проверить. ":
        label_1['text'] = '* Вы используете систему для определения языка текста. \n' \
                      '* Для того, чтобы воспользоваться одним из методов определения языка текста нажмите на кнопку с соответствующим методом. \n' \
                      '* Чтобы каждый раз не стирать путь к файлу вручную, нажмите на кнопку "Очистить строку ввода" \n' \
                      '* Все проведенные анализы сохраняются автоматически, вы можете посмотреть предыдущие анализы в папке \\out. \n' \
                      '* Каждому анализу соответствует папка с датой и временем проверки. \n* Выйти из программы вы можете нажав на кнопку "Завершить программу" либо нажав на крестик в верхнем правом углу экрана.'
    else:
        label_1['text'] = "Введите в поле ввода путь к файлу, содержимое которого хотите проверить. "

    label_2['text'] = ''


def clear_button():
    entry_path.delete(0, 'end')


alphabet_method_button = Button(text="Алфавитный метод", command=alphabet_method_button, bg="black", fg="white", height=2, width=20)
grams_method_button = Button(text="Метод N-грамм ", command=grams_method_button, bg="black", fg="white", height=2, width=20)
neural_method_button = Button(text="Нейронный метод ", command=neural_method_button, bg="black", fg="white", height=2, width=20)
exit_button_handler = Button(text="Завершить программу", command=exit_button_handler, bg="black", fg="white", height=2, width=20)
help_btn = Button(text="Помощь", command=help_button, bg="black", fg="white", height=2, width=20)
clear_button = Button(text="Очистить строку ввода", command=clear_button, bg="black", fg="white", height=2, width=20)

alphabet_method_button.pack()
grams_method_button.pack()
neural_method_button.pack()
exit_button_handler.pack()
clear_button.pack()
help_btn.pack()

entry_path.pack(padx=8, pady=8)
label_1.pack(padx=10, pady=10)
label_2.pack()

root.mainloop()
