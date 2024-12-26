import pyttsx3
import speech_recognition

import parser
from phrases import phrases


def speech_synthesis(engine: pyttsx3.Engine, text_: str) -> None:
    engine.say(text_)
    engine.runAndWait()


def voice_recognition(recognizer, microphone, lang='ru'):
    if lang == 'en':
        lang = 'en-US'
    with microphone:
        recognized_data = ""
        recognizer.adjust_for_ambient_noise(microphone, duration=2)
        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 5, 5)

        except speech_recognition.WaitTimeoutError:
            print("Can you check if your microphone is on, please?")
            return
        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language=lang).lower()

        except speech_recognition.UnknownValueError:
            pass

        except speech_recognition.RequestError:
            print("Check your Internet Connection, please")

        return recognized_data


def get_poem(lang):
    if lang == 'ru':
        main_page = parser.get_src(parser.url_ru)
        poem_url = parser.get_random_poem_ru(main_page)
        poem_page = parser.get_src(poem_url)
        return parser.get_text(poem_page)
    elif lang == 'en':
        page = parser.get_src(parser.url_en)
        return parser.get_random_poem_en(page)



def change_lang(eng, lang):
    if lang == 'en':
        gender = input('Choose speaker: z - ZIRA, d - DAVID: ')
        if gender == 'z':
            eng.setProperty('voice', eng.getProperty('voices')[1].id)
            return True
        elif gender == 'd':
            eng.setProperty('voice', eng.getProperty('voices')[2].id)
            return True
        else:
            print("Incorrect input")
            return change_lang(eng, lang)
    elif lang == 'ru':
        eng.setProperty('voice', eng.getProperty('voices')[0].id)
        return True


def main():
    eng = pyttsx3.init()
    volume = 0.5
    eng.setProperty('volume', volume)  # Максимальная громкость
    rate = 150
    eng.setProperty('rate', rate)  # Установка скорости на 150 WPM
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    language = input('Choose language: en - English, ru - Russian: ')
    print('You choose: ' + language)
    if change_lang(eng, language):
        while True:
            result = voice_recognition(recognizer, microphone, language)
            text = ''
            if not result:
                continue
            print(result + '\n')
            if result == phrases['command1'][language]:
                text = get_poem(language)
                print(text)
            elif result == phrases['stop'][language]:
                text = phrases['off'][language]
            elif result == phrases['volume_up'][language]:
                volume += 0.1
                eng.setProperty('volume', volume)  # Максимальная громкость
                print(result)
            elif result == phrases['volume_down'][language]:
                volume -= 0.1
                eng.setProperty('volume', volume)  # Максимальная громкость
                print(result)
            elif result == phrases['rate_up'][language]:
                rate += 20
                eng.setProperty('rate', rate)  # Установка скорости на 150 WPM
                print(result)
            elif result == phrases['rate_down'][language]:
                rate -= 10
                eng.setProperty('rate', rate)  # Установка скорости на 150 WPM
                print(result)
            else:
                text = phrases['unknown_command'][language]
                print(text)
            if text:
                speech_synthesis(eng, text)
            if result == phrases['stop'][language]:
                break


if __name__ == '__main__':
    main()
