import jieba
import wordcloud
import os
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.cm import ScalarMappable

def load_words_data(file_path):
    views = {}
    with open(file_path, 'r') as f:
        for line in f:
            key, good, bad, best = line.strip().split('||')
            good = good.split(',')
            bad = bad.split(',')
            best = best.split(',')
            views[key] = (good, bad, best)
    return views
            
def process_single_views(text):
    ls = jieba.lcut(text) # 生成分词列表
    return ls

def get_words_from_views(views, key):
    (good, bad, best) = views[key]
    good_words_text = []
    bad_words_text = []
    for good_view in good:
        good_words_list = process_single_views(good_view)   
        good_words_text.extend(good_words_list)
    for bad_view in bad:
        bad_words_list = process_single_views(bad_view)   
        bad_words_text.extend(bad_words_list)
    return good_words_text, bad_words_text

def generate_wordcloud(words_list, data_path, file_name):
    text = ' '.join(words_list)
    stopwords = ["的","是","了"] # 去掉不需要显示的词
    if file_name == "bad.png":
        wc = wordcloud.WordCloud(font_path="msyh.ttc",
                                 width=400,
                                 height=300,
                                 background_color='white',
                                 colormap="Reds",
                                 max_words=100,
                                 stopwords=stopwords)
    else:
        wc = wordcloud.WordCloud(font_path="msyh.ttc",
                                 width=400,
                                 height=300,
                                 background_color='white',
                                 colormap="Greens",
                                 max_words=100,
                                 stopwords=stopwords)
    wc.generate(text)
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    wc.to_file(data_path + '/' + file_name)
    
def generate_wordcloud_of_an_item(file_path, key):
    views = load_words_data(file_path)
    good, bad = get_words_from_views(views, key)
    # print(good)
    # print(bad)
    data_path = 'static/wordcloud_pictures/' + str(key) + '/'
    good_file_name = 'good.png'
    bad_file_name = 'bad.png'
    if len(good) < 10 and len(bad) < 10:
        print('Both lists are too short!')
        return
    elif len(good) < 10 and len(bad) >= 10:
        print('Good list is too short')
        generate_wordcloud(bad, data_path, bad_file_name)
        print('Good wordcloud is saved')
    elif len(bad) < 10 and len(good) >= 10:
        print('Bad list is too short')
        generate_wordcloud(good, data_path, good_file_name)
        print('Bad wordcloud is saved')
    else:
        generate_wordcloud(bad, data_path, bad_file_name)
        generate_wordcloud(good, data_path, good_file_name)
        print('Both wordclouds are saved')
        
def load_scores_data(file_path):
    df = pd.read_excel(file_path)
    scores_dict = {}
    for index, row in df.iterrows():
        product_name = row.iloc[0]
        score_snow = row.iloc[1]
        score_boson = row.iloc[2]
        score_baidu = row.iloc[3]
        score_avg = row.iloc[4]
        scores_list = [score_snow, score_boson, score_baidu, score_avg]
        scores_dict[product_name] = scores_list
    return scores_dict
        
def plot_scores(scores_list, data_path):
    categories = ['SnowNLP', 'Boson', 'Baidu', 'Average']
    plt.figure(figsize=(8, 6))
    coolwarm_colors = [(0, 'red'), (0.5, 'white'), (1, 'green')]
    cmap = LinearSegmentedColormap.from_list('Custom', coolwarm_colors)
    bars = plt.barh(categories, scores_list, color=cmap([(x+1)/2 for x in scores_list]))
    plt.xlim(-1, 1)
    plt.title('Emotion Scores for the Product')
    plt.xlabel('Score')
    plt.ylabel('Score Type')
    sm = ScalarMappable(cmap=cmap)
    sm.set_array([-1, 1])  
    plt.axvline(x=0, color='blue', linestyle='-')
    plt.colorbar(sm, label='Color')
    plt.savefig(data_path, dpi=75, bbox_inches='tight')
    
def plot_scores_of_an_item(file_path, key):
    scores_dict = load_scores_data(file_path)
    scores_list = scores_dict[key]
    data_path = 'static/score_pictures/'
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    data_path = data_path + 'score_' + str(key) + '.png'
    plot_scores(scores_list, data_path)
    print('Score picture is saved.')
        
if __name__ == '__main__':
    # generate_wordcloud_of_an_item('jd_des.txt', '5')
    plot_scores_of_an_item('jd_scores.xlsx', 5)
    

    
    
    
    
    