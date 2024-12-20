import shutil

from Translate import getTranslationAPI, getTranslationByWords, getTree
import tkinter.filedialog

from pathlib import Path
import os
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel


OUTPUT_PATH = Path(__file__).parent
IMAGES_PATH = "C://Users//nikit//OneDrive//Desktop//bsuir//eyaziis_4//images"
print(str(OUTPUT_PATH))
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\nikit\OneDrive\Desktop\bsuir\eyazis3\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def save_output():
    output = text_area.get("1.0", "end")
    with open(str(OUTPUT_PATH)+"\save.txt", "w", encoding="UTF-8") as file:
        file.write(output)
    print("Сохранено!")


def select_folder():
    global output_path
    output_path = tkinter.filedialog.askdirectory()

    for root, dirs, files in os.walk(output_path):
        for file in files:
            path = os.path.join(root, file)
            with open(f'{os.path.join(root, file)}', 'r', encoding='utf-8') as file:
                text = file.read()

            output = f"\n\nСсылка на документ: {path}\n\n"
            output += f"~~~ Содержимое ~~~\nКоличество слов: {len(text.split())}.\n"
            output += text.replace("\n", " ")
            translated_text = getTranslationAPI(text=text, langFrom='en', langTo='de')
            output += f"\n\n~~~ Перевод ~~~\nКоличество слов: {len(translated_text.split())}.\n"
            output += translated_text
            output += "\n\n~~~ Грамматическая информация ~~~\n"
            data = getTranslationByWords(text=text, langFrom='en', langTo='de')
            sorted_data = sorted(data, key=lambda x: x['frequency'], reverse=True)
            output += f"\tСлово\t\tПеревод\t\tЧастота\t\tЧасть речи\t\n"
            for item in sorted_data:
                output += f"\t{item['word']}\t\t{item['translation']}\t\t{item['frequency']}\t\t{item['tags']}\t\n"
            name = os.path.splitext(os.path.basename(path))[0]
            getTree(text=translated_text, file=name)

            output += f"\n~~~ Синтаксическая информация ~~~\n{IMAGES_PATH}//{name}_x.png"

            text_area.insert('1.0', output)

    return output_path


def select_document():
    global output_path
    output_path = tkinter.filedialog.askopenfile()

    with open(f'{output_path.name}', 'r', encoding='utf-8') as file:
        text = file.read()
    output = f"\n\nСсылка на документ: {output_path.name}\n\n"
    output += f"~~~ Содержимое ~~~\nКоличество слов: {len(text.split())}.\n"
    output += text.replace("\n", " ")
    translated_text = getTranslationAPI(text=text, langFrom='en', langTo='de')
    output += f"\n\n~~~ Перевод ~~~\nКоличество слов: {len(translated_text.split())}.\n"
    output += translated_text
    output += "\n\n~~~ Грамматическая информация ~~~\n"
    data = getTranslationByWords(text=text, langFrom='en', langTo='de')
    sorted_data = sorted(data, key=lambda x: x['frequency'], reverse=True)
    output +=  f"\tСлово\t\tПеревод\t\tЧастота\t\tЧасть речи\t\n"
    for item in sorted_data:
        output +=  f"\t{item['word']}\t\t{item['translation']}\t\t{item['frequency']}\t\t{item['tags']}\t\n"
    name = os.path.splitext(os.path.basename(output_path.name))[0]
    getTree(text=translated_text, file=name)

    output += f"\n~~~ Синтаксическая информация ~~~\n{IMAGES_PATH}//{name}_x.png"
    text_area.insert('1.0', output)
    return output_path.name


def help_window():
    help_window = Toplevel(window)
    help_window.lift()
    help_window.geometry("350x360")
    help_window.configure(bg="#379683")

    canvas = Canvas(
        help_window,
        bg="#379683",
        height=360,
        width=350,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        12.0,
        11.0,
        anchor="nw",
        text="Данное приложение поможет вам\nпроизвести перевод с английского\nна немецкий",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        12.0,
        185.0,
        anchor="nw",
        text="Кнопка “Помощь” откроет данное окно",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        12.0,
        219.0,
        anchor="nw",
        text="Кнопка “Выбрать документ” позволит вам\nвыбрать один документ и перевести его",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        13.0,
        291.0,
        anchor="nw",
        text="Кнопка “Выбрать папку” сделает перевод\nвсех документов из выбранной вами\nпапки",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        12.0,
        90.0,
        anchor="nw",
        text="Кнопка ",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        135.0,
        90.0,
        anchor="nw",
        text="сохранит весь вывод",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        12.0,
        132.0,
        anchor="nw",
        text="программы в текстовый файл с\nназванием “save.txt”",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    image_1 = canvas.create_image(
        101.0,
        99.0,
        image=image_image_1
    )
    help_window.resizable(False, False)
    help_window.mainloop()


window = Tk()

window.geometry("762x500")
window.configure(bg="#379683")

canvas = Canvas(
    window,
    bg="#379683",
    height=500,
    width=762,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
button_image_save = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_save = Button(
    image=button_image_save,
    borderwidth=0,
    highlightthickness=0,
    command=save_output,
    relief="flat"
)
button_save.place(
    x=113.0,
    y=17.0,
    width=47.600006103515625,
    height=47.600006103515625
)

button_image_help = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_help = Button(
    image=button_image_help,
    borderwidth=0,
    highlightthickness=0,
    command=help_window,
    relief="flat"
)
button_help.place(
    x=181.0,
    y=17.0,
    width=77.0,
    height=47.600006103515625
)

button_image_pick_folder = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_pick_folder = Button(
    image=button_image_pick_folder,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print(select_folder()),
    relief="flat"
)
button_pick_folder.place(
    x=474.0,
    y=17.0,
    width=176.0,
    height=47.600006103515625
)

button_image_pick_document = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_pick_document = Button(
    image=button_image_pick_document,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print(select_document()),
    relief="flat"
)
button_pick_document.place(
    x=278.0,
    y=17.0,
    width=176.0,
    height=47.600006103515625
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    381.0,
    284.0,
    image=entry_image_1
)
text_area = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
text_area.place(
    x=14.0,
    y=82.0,
    width=734.0,
    height=402.0
)

def display_popup(event):
    menu.post(event.x_root, event.y_root)

def popup_copy():
    text_area.event_generate("<<Copy>>")

def popup_cut():
    text_area.event_generate("<<Cut>>")

def popup_paste():
    text_area.event_generate("<<Paste>>")

menu = tkinter.Menu(tearoff=False)
menu.add_command(label="Copy", command=popup_copy)
menu.add_command(label="Cut", command=popup_cut)
menu.add_separator()
menu.add_command(label="Paste", command=popup_paste)
text_area.bind("<Button-3>", display_popup)

canvas.create_rectangle(
    705.0,
    39.0,
    719.0,
    118.0,
    fill="#236155",
    outline="")

canvas.create_rectangle(
    732.0,
    62.0,
    746.0,
    141.0,
    fill="#236155",
    outline="")

canvas.create_rectangle(
    678.0,
    14.0,
    692.0,
    93.0,
    fill="#236155",
    outline="")

canvas.create_rectangle(
    44.0,
    39.0,
    58.0,
    118.0,
    fill="#236155",
    outline="")

canvas.create_rectangle(
    71.0,
    14.0,
    85.0,
    93.0,
    fill="#236155",
    outline="")

canvas.create_rectangle(
    17.0,
    62.0,
    31.0,
    141.0,
    fill="#236155",
    outline="")

window.resizable(False, False)
window.mainloop()


