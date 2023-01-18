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
from wordcloud import WordCloud


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


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="generate wordcloud from CV in pdf format")
    parser.add_argument('--cv', type=str,
                        required=True, help='input CV in pdf format')
    parser.add_argument('--img', type=str,
                        required=True, help='filename of the output wordcloud image')
    parser.add_argument('--lang', type=str,
                        required=True, help='filename of the output wordcloud image (english or french)')                        
    parser.add_argument('--com', type=int, default=10,
                        required=False, help='number of most common words (they are not taken into account)')                        
    parser.add_argument('--map', type=str, default=None,
                        required=False, help='name of the figure colormap')

    args = parser.parse_args()

    # read pdf
    resMgr = PDFResourceManager()
    retData = io.StringIO()
    TxtConverter = TextConverter(resMgr, retData, laparams= LAParams())
    interpreter = PDFPageInterpreter(resMgr, TxtConverter)

    with open(args.cv,'rb') as fid:
        for page in PDFPage.get_pages(fid):
            interpreter.process_page(page)
    txt = retData.getvalue()
    docu = txt.split(' ')
    # set as dataframe
    df = pd.DataFrame({'line': docu})
    nltk.download('omw-1.4')
    
    # get words and remove words with less than 4 characters
    cv_words = []
    for line in df['line']:
        for word in processRow(line).split():
            if len(word) > 3:
                cv_words.append(word)

    print(f'number of words in CV : {len(cv_words)}')
    # remove stop words
    stopWords = stopwords.words(args.lang)
    cv_words2 = [word for word in cv_words if word not in stopWords]
    # compute word frequency
    frequency_dist = nltk.FreqDist(cv_words2)

    print('fréquence des xx premiers mots les plus utilisés')
    print(frequency_dist.most_common(args.com))

    # generate wordcloud
    wcloud = WordCloud(colormap=args.map).generate_from_frequencies(frequency_dist)
    # wcloud = WordCloud(colormap="coolwarm").generate_from_frequencies(frequency_dist)

    # plot figure
    plt.figure(figsize=(15, 10))
    plt.imshow(wcloud, interpolation='bilinear', origin='upper')
    plt.axis('off')
    plt.margins(x=0, y=0)
    plt.savefig(args.img)
    plt.show()
