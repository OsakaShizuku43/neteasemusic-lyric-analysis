# NeteaseMusic Lyric Analysis
## Introduction
Analyze the composition of words in your NeteaseMusic favourite song list (Japanese songs only for this project).

The following aspects are customizable:
- Part of speech to include in the word cloud (noun, adjective, verbs, ...)
- Specific words to exclude
- Specific characters to exclude

## Acknowledgement
- NeteaseMusic API: [Binaryify/NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)
- MeCab (Extracting words from lyric): https://taku910.github.io/mecab/#usage-tools
- word_cloud: https://github.com/amueller/word_cloud

Without the above projects, this project won't be able to come true. Thank you!

## Requirements
- mecab-python3
- word_cloud
- matplotlib
- requests

## Get it working
1. Clone the API, [Binaryify/NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi), and run it following its documentation.
2. Install required packages for this project (listed in above section).
3. Copy `settings.sample.py` into `settings.py`, put credential of your NeteaseMusic account, and specify settings.
4. `python main.py` and enjoy!

This is the final result for my favourite songs :)
![](wordcloud.png)