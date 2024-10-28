import pandas as pd
import re
import snownlp
import jieba
from aip import AipNlp
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
import xiangshi as xs
import networkx as nx

def load_comments_xlsx(xlsx_path):
    df = pd.read_excel(xlsx_path)
    sub_df = df.iloc[121:122] # 450
    return sub_df

def clean(desstr,restr=''):  
    #过滤表情   
    try:  
        co = re.compile(u'['u'\U0001F300-\U0001F64F' u'\U0001F680-\U0001F6FF'u'\u2600-\u2B55]+')  
    except re.error:  
        co = re.compile(u'('u'\ud83c[\udf00-\udfff]|'u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'u'[\u2600-\u2B55])+')  
    return co.sub(restr, desstr)

def filter_emoji(desstr, restr=''):
    # 过滤表情
    res = re.compile(u'[\U00010000-\U0010ffff\\uD800-\\uDBFF\\uDC00-\\uDFFF]')
    return res.sub(restr, desstr)

def text_preprocessing(df):
    print('Text preprocessing...')
    comments_dict = {}
    for index, row in df.iterrows():
        text_comments = []
        product_name = row.iloc[0]
        comments = row.iloc[8]
        # print(comments)
        if not isinstance(comments, str):
            comments_dict[product_name] = text_comments
            continue
        comments = eval(comments)
        for x in comments:
            if isinstance(x, str):
                # cleaned_x = remove_invalid_chars(x)
                # if x == '此用户没有填写评价。':
                #     continue
                x = clean(x)
                x = filter_emoji(x)
                if len(x) > 10:
                    text_comments.append(x)
        text_comments = list(set(text_comments))
        # sorted_comments = sorted(text_comments, key=lambda x: len(x), reverse=True)
        comments_dict[product_name] = text_comments
    return comments_dict
    
def min_max_normalize(min_original, max_original, score):
    normalized_score = (score - min_original) * 2 / (max_original - min_original) - 1
    return normalized_score

def sentiment_analysis_snownlp(text):
    sentiment = snownlp.SnowNLP(text).sentiments
    return min_max_normalize(0, 1, sentiment)

def sentiment_analysis_boson(text):
    sentiment_words = []
    with open('resources/BosonNLP_sentiment_score.txt', 'r', encoding='utf-8') as f:
        for line in f:
            word, sentiment = line.strip().split()
            sentiment_words.append((word, float(sentiment)))
    
    # 分词
    words = list(jieba.cut(text))
    
    # 统计情感词数量
    sentiment_count = 0
    count = 0
    good_word_list = []
    bad_word_list = []
    for word, sentiment in sentiment_words:
        if word in words:
            sentiment_count += sentiment
            count += 1
            if sentiment > 0:
                good_word_list.append(word)
            else:
                bad_word_list.append(word)
    if count == 0:
        return 0.0, good_word_list, bad_word_list
    else:
        return min_max_normalize(-6.7, 6.37, sentiment/count), good_word_list, bad_word_list
    
def sentiment_analysis_baidu(text):  # 这里是我自己的API信息，后面用完了可能要改
    APP_ID = '68539651'
    API_KEY = 'yncuXESstSOD6XMLgF90PbLD'
    SECRET_KEY = 'SMn4ZjAdjzCyewiAw424DRihgk97dhjN'
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    result = client.sentimentClassify(text)
    key = 'items'
    if key in result:
        return result['items'][0]['positive_prob']-result['items'][0]['negative_prob']
    else:
        return 0.0  
'''
{ 
   'items': [ {
        'confidence': 0.528202, //表示分类的置信度
        'negative_prob': 0.787691, //表示属于消极类别的概率
        'positive_prob': 0.212309, //表示属于积极类别的概率
        'sentiment': 0 //表示情感极性分类结果
        } 
    ], 
    'text': '以前约过一个电子系妹子...... '
}
'''

def views_extract_baidu(text):
    APP_ID = '68539651'
    API_KEY = 'yncuXESstSOD6XMLgF90PbLD'
    SECRET_KEY = 'SMn4ZjAdjzCyewiAw424DRihgk97dhjN'
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    # all = {}
    good_abst = ''
    bad_abst = ''
    options = {}
    options['type'] = 13
    result=client.commentTag(text, options)
    # print(result)
    if "error_code" in result.keys():
        good_abst += ''
        bad_abst += ''
        # all['abstract'] = abst
    else:
        data = result['items']
        # print(data)
        for items in data:
            if items['sentiment'] == 2:
                good_abst += items['abstract']
            elif items['sentiment'] == 0:
                bad_abst += items['abstract']
    return good_abst, bad_abst

def views_parser(comment):
    soup = BeautifulSoup(comment, 'html.parser')
    return [span.text for span in soup.find_all('span')]

def calculate_distance(text1, text2):
    distance = 0.0
    distance += xs.cossim(text1, text2)
    distance += xs.simhash(text1, text2)
    distance += xs.minhash(text1, text2)
    distance += xs.jaccard(text1, text2)
    return distance/4

def get_n_closest_points(points, n):
    G = nx.Graph()
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if len(points[i]) > 0 and len(points[j]) > 0:
                distance = calculate_distance(points[i], points[j])  # 计算观点之间的距离
                G.add_edge(i, j, weight=distance)
    T = nx.minimum_spanning_tree(G)
    closest_nodes = sorted(T.edges(data=True), key=lambda x: x[2]['weight'])[:n]
    closest_points = [points[edge[0]] for edge in closest_nodes] + [points[edge[1]] for edge in closest_nodes]
    return closest_points

def get_scores_dict(comments_dict, score_path, des_path, save=True):
    scores_dict = {}
    des_dict = {}
    for key, comments in comments_dict.items():
        score_snownlp_total = 0
        score_boson_total = 0
        score_baidu_total = 0
        count = 0
        scores = []
        good_descriptions = []
        bad_descriptions = []
        best_views = []
        if comments == []:
            scores = [0.0, 0.0, 0.0, 0.0]
        else:
            j = 1
            for comment in comments:
                print('Processing', key, 'item', j, 'comment')
                score_snownlp = sentiment_analysis_snownlp(comment)
                score_boson, good_words, bad_words = sentiment_analysis_boson(comment)
                score_baidu = sentiment_analysis_baidu(comment)
                score_snownlp_total += score_snownlp
                score_boson_total += score_boson
                score_baidu_total += score_baidu
                count += 1
                j += 1
                good, bad = views_extract_baidu(comment)
                if good.isspace() and bad.isspace():
                    continue
                elif good.isspace():
                    good = []
                elif bad.isspace():
                    bad = []
                else:
                    good = views_parser(good)
                    bad = views_parser(bad)
                good_descriptions.extend(good)
                bad_descriptions.extend(bad)
            score_snownlp_avg = score_snownlp_total / count
            score_boson_avg = score_boson_total / count
            score_baidu_avg = score_baidu_total / count
            score_all_avg = (score_snownlp_avg + score_boson_avg + score_baidu_avg) / 3
            scores.append(key)
            scores.append(score_snownlp_avg)
            scores.append(score_boson_avg)
            scores.append(score_baidu_avg)
            scores.append(score_all_avg)
        scores_dict[key] = scores
        # sorted_good = sorted(good_descriptions, key=lambda x: len(x), reverse=True)
        # sorted_bad = sorted(good_descriptions, key=lambda x: len(x), reverse=True)
        print('Good:\n', good_descriptions)
        print('Bad:\n', bad_descriptions)
        if len(good_descriptions) > 5:
            best_good = get_n_closest_points(good_descriptions, 5)
            best_views.extend(best_good)
        if len(bad_descriptions) > 5:
            best_bad = get_n_closest_points(bad_descriptions, 5)
            best_views.extend(best_bad)
        best_views = list(set(best_views))
        print('Best views:\n', best_views)
        des_dict[key] = (good_descriptions, bad_descriptions, best_views)
    if save:
        column_names = ['index', 'snow_nlp', 'boson', 'baidu', 'avg']
        scores_df = pd.DataFrame.from_dict(scores_dict, orient='index', columns=column_names)
        if not os.path.exists(score_path):
            scores_df.to_excel(score_path, index=False)
        else:
            df = pd.read_excel(score_path)
            df = pd.concat([df, scores_df], ignore_index=True)
            df.to_excel(score_path, index=False)
        
        # des_df = pd.DataFrame({key: pd.Series(value) for key, value in des_dict.items()})
        # des_df.to_excel(des_path, index=False)
        with open(des_path, 'a') as f:
            for key, value in des_dict.items():
                list1 = ','.join(map(str, value[0]))
                list2 = ','.join(map(str, value[1]))
                list3 = ','.join(map(str, value[2]))
                f.write(f"{key}||{list1}||{list2}||{list3}\n")
        print('Result is saved.')
    return scores_dict, des_dict

def sentiment_analysis(xlsx_path, score_path, des_path):
    df = load_comments_xlsx(xlsx_path)
    comments_dict = text_preprocessing(df)
    scores_dict, des_dict = get_scores_dict(comments_dict, score_path, des_path)
    return scores_dict, des_dict

def sentiment_analysis_new(dic, score_path, des_path):
    df = pd.DataFrame([dic])
    comments_dict = text_preprocessing(df)
    scores_dict, des_dict = get_scores_dict(comments_dict, score_path, des_path)
    return scores_dict, des_dict
# def plot_scores(scores_list, save=False):
#     colors = ['red' if score > 0 else 'blue' for score in scores_list]
#     plt.figure(figsize=(8, 6))
#     plt.bar(range(len(scores_list)), scores_list, color=colors)
#     plt.title('Emotion Scores for the Product')
#     plt.xlabel('Score Type')
#     plt.ylabel('Score')
#     if save:
#         plt.savefig('emotion_scores_of_a_product.png', dpi=300, bbox_inches='tight')
    
    

if __name__ == '__main__':
    scores_dict, des_dict = sentiment_analysis('jd_item1.xlsx', 'jd_scores.xlsx', 'jd_des.txt')
    
    
    

    
