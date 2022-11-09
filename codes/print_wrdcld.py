import os
import matplotlib.pyplot as plt
import numpy as np
import argparse
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image


def load_lyrics(path):
    """ Load lyrics from files exist in path"""
    text = ''   
    files = os.listdir(f'{path}/')

    for file in files:
        if os.path.isfile(f'{path}/{file}'):    
            lyric = open(file=f'{path}/{file}',mode='r').read()
            text = text + ' ' + lyric
        else:
            continue            
    return text

def transform_png(file):
    '''Build mask for word-cloud based on png-file'''
    mask = np.array(Image.open(file))
    mask_rs = mask.reshape(-1,1)
    mask_rs_tf = np.array([transform_val(val) for val in mask_rs], np.uint8)
    mask_tf = mask_rs_tf.reshape(mask.shape)
    return mask_tf

# Required to define white pixels in mask as '255' (assumes currently = 0, to be changed accordingly)
def transform_val(val):
    if val == 0:
        return 255
    else: 
        return val

def create_wordcloud(artist, txt, msk=None, font_color='black'):
    
    cloud = WordCloud(background_color="white",
                    max_words=200,
                    min_font_size=1,
                    width=400, height=400,
                    mask=msk,
                    contour_width=0, contour_color='black',
                    collocations=False,  # calculates frequencies
                     ).generate(txt)
                    # stop words are removed!
    
    plt.figure(figsize = (12,12))
    plt.imshow(cloud.recolor(color_func=lambda *args, **kwargs: font_color), interpolation='bilinear')
    plt.axis("off")
    plt.savefig(f'{output}.png')
    plt.show()

# Build parser with ArgumentParser: parse the command line
parser = argparse.ArgumentParser(description="""This script create a fancy word cloud from lyrics""")

# Create arguments that the user can pass to the script
parser.add_argument("--path", help="path of lyrics file")
parser.add_argument("--mask", default='None', help="path of mask file. defualt=None")
parser.add_argument("--color", default='black',help="color of word cloud. defualt=black")
parser.add_argument("--output", help="output file")

# map the user input values  with the possible arguments
arguments = parser.parse_args()

# extract the argument
path = str(arguments.path)
mask_file = str(arguments.mask)
color = str(arguments.color)
output = str(arguments.output)


corpus =load_lyrics(path)
try:
    mask = transform_png(mask_file)
except:
    mask= None

create_wordcloud(output, corpus, msk=mask, font_color=color)