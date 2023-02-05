import matplotlib.pyplot as plt
from wordcloud import WordCloud


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="generate wordcloud from CV in pdf format")
    parser.add_argument('--words', type=str,
                        required=True, help='input file with words and score')
    parser.add_argument('--img', type=str,
                        required=True, help='filename of the output wordcloud image')
    parser.add_argument('--map', type=str, default="Blues",
                        required=False, help='name of the figure colormap')

    args = parser.parse_args()

    # read text file, format = word : score
    lines = open(args.words, 'r').readlines()
    frequency_dist = dict()
    for line in lines:
        key, value = line.split(':')
        value = int(value)
        frequency_dist[key] = value

    print(f'number of words in CV : {len(frequency_dist.keys())}')
    print(frequency_dist)

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
