import nltk
import spacy
from nltk import ParentedTree
from spacy import displacy
import cairosvg
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

from google_trans_new import google_translator

from pymorphy2 import MorphAnalyzer

nlpDe = spacy.load("de_core_news_sm")
nlpEn = spacy.load("en_core_web_sm")


def get_word_tags(word:str):
    morph = MorphAnalyzer()
    le = morph.parse(word)[0]
    tags = le.tag.cyr_repr
    return tags

def getTranslationAPI(langFrom, langTo, text):
  translator = google_translator()
  return translator.translate(text, lang_src=langFrom, lang_tgt=langTo)

def getTranslationByWords(langFrom, langTo, text):
  result = []
  words = wordize(text)

  nlproc = nlpEn

    
  for word in words:
    in_result = False
    for item in result:
        if word == item['word']:
            in_result = True
            item['frequency'] += 1
    if not in_result:
      resultItem = ({
        'word': word, 
        'translation': getTranslationAPI(
          langFrom=langFrom,
          langTo=langTo,
          text=word
        ),
        'frequency': 1,
        'tags':nlproc(word)[0].pos_
      })
      result.append(resultItem)
    
  return result


def wordize(text):
  words = []
  for sent in nltk.sent_tokenize(text.lower()):
      for word in nltk.word_tokenize(sent):
          if word != '.' and word != ',' and word != '?' and word != '!' and word != '-':
              words.append(word)
              
  return words


def getTree(text, file):
  sentences = sent_tokenize(text)
  print(sentences)
  print(file)
  # Создаем главное окно
  # Обработка каждого предложения
  for i, sentence in enumerate(sentences):
    doc = nlpDe(sentence.strip())
    svg = displacy.render(doc, style='dep', options={'compact': True})

    # Конвертация SVG в PNG
    png_filename = f"C://Users//nikit//OneDrive//Desktop//bsuir//eyaziis_4//images//{file}_{i}.png"
    cairosvg.svg2png(bytestring=svg, write_to=png_filename, scale=1, background_color='white')