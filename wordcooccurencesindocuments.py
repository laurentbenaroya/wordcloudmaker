import io
import pandas as pd
import re
import matplotlib.pyplot as plt

from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

import nltk
from nltk.corpus import stopwords
from textblob import Word


def processRow(row):
    tweet = row
    tweet = tweet.lower()

    tweet = re.sub(r'(\\u[0-9a-fA-F]+)', r'', tweet)
    # tweet = re.sub(r'[^\x00-\x7f]', r'', tweet)

    tweet = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)  # ^\s
    tweet = re.sub('@[^\s]+', 'AT_USER', tweet)

    tweet = re.sub('[\s]+', ' ', tweet)
    tweet = re.sub('[\n]+', ' ', tweet)
    tweet = re.sub('[\t]+', ' ', tweet)

    tweet = re.sub(r'[^\w]', ' ', tweet)

    tweet = re.sub(r'(#[^\s]+)', r'\1', tweet)
    tweet = ' '.join([i for i in tweet.split() if not i.isdigit()])

    tweet = re.sub(r'(\.)\1+', ' ', tweet)
    # lemma
    tweet = ' '.join([Word(word).lemmatize() for word in tweet.split()])

    # trim
    tweet = tweet.strip('\'''')
    row = tweet

    return row


def get_words_from_pdf(mypdf, lang):
    """
        read pdf and get words with some cleaning
    """
    resMgr = PDFResourceManager()
    retData = io.StringIO()
    TxtConverter = TextConverter(resMgr, retData, laparams= LAParams())
    interpreter = PDFPageInterpreter(resMgr, TxtConverter)

    with open(mypdf,'rb') as fid:
        for page in PDFPage.get_pages(fid):
            interpreter.process_page(page)
    txt = retData.getvalue()
    docu = txt.split(' ')
    # set as dataframe
    df = pd.DataFrame({'line': docu})
    
    
    # get words and remove words with less than 4 characters
    my_words = []
    for line in df['line']:
        for word in processRow(line).split():
            if len(word) > 3:
                my_words.append(word)

    # remove stop words
    stopWords = stopwords.words(lang)
    my_words = [word for word in my_words if word not in stopWords]
    if True:
        # ad-hoc for Laurent E.
        my_words = [word.replace('commerciale', 'commercial') for word in my_words]
    print(f'number of words in {mypdf} : {len(my_words)}, cleaned : {len(my_words)}')
    return my_words


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="display common words in two or more pdf documents")
    parser.add_argument('--docs', '--names-list', required=True, default=[], nargs='+', help='document filenames (minimum of two)')
    parser.add_argument('--lang', type=str, required=True, help='language (english or french)')                        

    args = parser.parse_args()

    nltk.download('omw-1.4')
    docs = args.docs
    if len(docs) < 2:
        print("You need to pass at least two document filenames in --docs argument")
        import sys
        sys.exit(-1)

    # process the two first documents
    d0_words = get_words_from_pdf(docs[0], lang=args.lang)
    d1_words = get_words_from_pdf(docs[1], lang=args.lang)
    # get intersection
    co_words = list(set(d0_words).intersection(set(d1_words)))
    for doc in docs[2:]:
        # iterate over next documents
        di_words = get_words_from_pdf(doc, lang=args.lang)
        co_words = list(set(co_words).intersection(set(di_words)))
    # sort list
    co_words = sorted(co_words)

    print()
    print(f'shared words : {len(co_words)}')
    print()
    print(', '.join(sorted(co_words)))
 