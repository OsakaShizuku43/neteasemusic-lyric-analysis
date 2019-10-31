import re
import requests

from wordcloud import WordCloud
import MeCab
import matplotlib.pyplot as plt

from settings import *


## Login to NeteaseMusic
s = requests.session()
user_info = s.get(API_URL + '/login?email={}&password={}'.format(NETEASE_EMAIL, NETEASE_PASSWORD)).json()
uid = user_info.get('account').get('id')
print('User id:', uid)

## Get favourite song list
playlist = s.get(API_URL + '/likelist?uid={}'.format(uid)).json()
fav_song_ids = playlist.get('ids')
print('Fav song list retrieved')
if fav_song_ids is None:
    print(playlist)
    exit()

## Get lyrics for each song
lyrics = []
for song_id in fav_song_ids:
    lyric_info = s.get(API_URL + '/lyric?id={}'.format(song_id)).json()
    if 'lrc' not in lyric_info:
        continue
    lyric = lyric_info.get('lrc').get('lyric')
    if len(lyric) > 0:
        lyrics.append(lyric)
        print('Lyric for song {} downloaded...'.format(song_id))
print('Lyrics retrieved')

## Process lyrics into correct format for word analysis
##  Get rid of pronunciation hint (Japanese) and lrc file timestamp
def process_lrc(line):
    if '作曲' in line or '作詞' in line:
        return ''
    re_lrc = re.compile(r'\[.+\]')
    re_bracket = re.compile(r'\(.+\)')
    re_jp_bracket = re.compile(r'（([^）.]+)）')
    line = re.sub(re_lrc, '', line)
    line = re.sub(re_bracket, '', line)
    line = re.sub(re_jp_bracket, '', line)
    return line
for i in range(len(lyrics)):
    lyrics[i] = '\n'.join(map(process_lrc, lyrics[i].split('\n')))
print('Lyrics processed')

## Extract for individual words
##  Uses MeCab to retrive dictionary form for each word and take nouns, adjective, verbs only
mc = MeCab.Tagger("-Ochasen")
re_english = re.compile(r'[A-Za-z]')
extracted_words = []
counter = 0
for lyric in lyrics:
    counter += 1
    print('Extracting words in lyric: {}...'.format(counter))
    for word_info_line in mc.parse(lyric.strip()).split('\n'):
        word_info = word_info_line.split('\t')
        if len(word_info) < 4:
            continue
        word_orig = word_info[2]
        word_type = word_info[3]
        if word_orig not in FILTER_CHARS and \
            re.match(re_english, word_orig) is None and \
                word_orig not in FILTER_WORDS and \
                    len(list(filter(lambda t: t in word_type, FILTER_TYPES))) > 0:
            extracted_words.append(word_orig)
print('Lyrics analysis complete')

## Create a word cloud
print('Generating word cloud...')
font = './Kyokasho.ttc'
wc = WordCloud(collocations=True, font_path=font, width=2850, height=1800, margin=4).generate('\n'.join(extracted_words))
print('Done')

plt.imshow(wc)
plt.axis("off")
plt.show()