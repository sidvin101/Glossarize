from this import d
import PyPDF2 as pdf
import regex as re
import nltk
from nltk.corpus import brown
from nltk.corpus import stopwords
import requests
import yaml
import pprint
import json

def glossify(file, numWords):
    # creating a pdf file object 
    pdfFileObj = open(file, 'rb') 
    
    # creating a pdf reader object
    pdfReader = pdf.PdfFileReader(pdfFileObj) 
    
    # printing number of pages in pdf file 
    print(pdfReader.numPages) 
    
    # creating a page object 
    pageObj = pdfReader.getPage(0) 
    
    # extracting text from page 
    testText = pageObj.extractText()
    
    # closing the pdf file object 
    pdfFileObj.close() 

    # a couple of merging code in order to properly split the text into separate words
    textChar = list(testText)
    
    textWord = ''.join(textChar)

    joinChars = "".join(textChar)

    convertedWords = joinChars.split()

    #create a set for a unique set of words (will have to be called again)
    uniqueWords = set(convertedWords)
    
    #replace special characters with a space
    nonspace = []
    for word in uniqueWords:
        word = word.replace('.',' ')
        word = word.replace(',',' ')
        word = word.replace('(',' ')
        word = word.replace(')',' ')
        word = word.replace('&',' ')
        word = word.replace('©',' ')
        word = word.replace('[',' ')
        word = word.replace(']',' ')
        nonspace.append(word)
    
    #reformats the list to maintain individual words
    reformattedList = ' '.join(nonspace).split()

    #filters out short words and words containing numerical values
    unShortList = [word for word in reformattedList if len(word) >= 3 and word.isalpha()]

    #removes any non-words
    nltk.download('words')
    words = set(nltk.corpus.words.words())
    realList = [word for word in unShortList if word in words]

    #removes any articles and other stopwords
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    nonStopList = [word for word in realList if word.lower() not in stop_words]

    #reorders the words by frequency in the english language. This will be our measurement for complexity
    nltk.download('brown')
    freqs = nltk.FreqDist([w.lower() for w in brown.words()])
    # sort wordlist by word frequency
    sortList = sorted(nonStopList, key=lambda x: freqs[x.lower()])

    #remove and reorder everything again
    uniqueListTwo = set(sortList)
    sortListTwo = sorted(uniqueListTwo, key = lambda x: freqs[x.lower()])

    #removes proper nouns
    commonList = [word for word in sortListTwo if word[0].islower()]

    #get the glossaryList 
    glossList = commonList[0:numWords]

    #gets the dictionary api
    aList = []
    for word in glossList:
        req = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        jList = json.loads(req.text)
        aList.append(jList)
    
    return aList