import matplotlib.pyplot as plt
import numpy as np

from wordcloud import WordCloud


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="generate wordcloud from ordered words/group of words text file")
    parser.add_argument('--txt', type=str,
                        required=True, help='input text file')
    parser.add_argument('--img', type=str,
                        required=True, help='filename of the output wordcloud image')
    parser.add_argument('--lang', type=str, default='french',
                        required=False, help='filename of the output wordcloud image (english or french)')                                               
    parser.add_argument('--map', type=str, default='Blues',
                        required=False, help='name of the figure colormap')
    """
    'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r'
    """
    args = parser.parse_args()

    lines = open(args.txt).readlines()
    word_dict = dict()
    for count, line in enumerate(lines):
        line = line.strip()
        word_dict[line] = count+1

    T = len(word_dict)
    alpha = 0.9
    z_min = 3
    z_max = 10
    delta = z_min-z_max
    modified_word_dict = dict()
    frequency_dist = dict()
    for word, value in word_dict.items():
        if False:
            print(word)
            print(value)
        frequency_dist[word] = int(np.floor(delta*((value-1)/(T-1))+z_max))

    # generate wordcloud
    xfig = 6
    yfig = 3
    wcloud = WordCloud(colormap=args.map, prefer_horizontal=0.8, height=yfig*100, width=xfig*100).generate_from_frequencies(frequency_dist)

    # plot figure
    plt.figure(figsize=(xfig, yfig))
    plt.imshow(wcloud, interpolation='bilinear', origin='upper')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(args.img)
    plt.show()
