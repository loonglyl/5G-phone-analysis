import pandas as pd
import re
import snownlp
import jieba
from aip import AipNlp
import matplotlib.pyplot as plt

def load_comments_xlsx(xlsx_path):
    df = pd.read_excel(xlsx_path)
    return df

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
        product_name = row.iloc[0]
        comments = row.iloc[5:].tolist()
        text_comments = []
        for x in comments:
            if isinstance(x, str):
                # cleaned_x = remove_invalid_chars(x)
                if x == '此用户没有填写评价。':
                    continue
                x = clean(x)
                x = filter_emoji(x)
                text_comments.append(x)
        text_comments = list(set(text_comments))
        print(text_comments)
        comments_dict[product_name] = text_comments
    return comments_dict
    
def min_max_normalize(min_original, max_original, score):
    normalized_score = (score - min_original) * 2 / (max_original - min_original) -1
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

def get_scores_dict(comments_dict, file_path, save=True):
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
                good_descriptions.extend(good_words)
                bad_descriptions.extend(bad_words)
                count += 1
                j += 1
            score_snownlp_avg = score_snownlp_total / count
            score_boson_avg = score_boson_total / count
            score_baidu_avg = score_baidu_total / count
            score_all_avg = (score_snownlp_avg + score_boson_avg + score_baidu_avg) / 3
            scores.append(score_snownlp_avg)
            scores.append(score_boson_avg)
            scores.append(score_baidu_avg)
            scores.append(score_all_avg)
        scores_dict[key] = scores
        des_dict[key] = (good_descriptions, bad_descriptions)
    if save:
        column_names = ['snow_nlp', 'boson', 'baidu', 'avg']
        scores_df = pd.DataFrame.from_dict(scores_dict, orient='index', columns=column_names)
        scores_df.to_excel(file_path, index=False)
        print('Result is saved.')
    return scores_dict, des_dict

def sentiment_analysis(xlsx_path, save_path):
    df = load_comments_xlsx(xlsx_path)
    comments_dict = text_preprocessing(df)
    scores_dict, des_dict = get_scores_dict(comments_dict, save_path)
    return scores_dict, des_dict

def plot_scores(scores_list, save=False):
    colors = ['red' if score > 0 else 'blue' for score in scores_list]
    plt.figure(figsize=(8, 6))
    plt.bar(range(len(scores_list)), scores_list, color=colors)
    plt.title('Emotion Scores for the Product')
    plt.xlabel('Score Type')
    plt.ylabel('Score')
    if save:
        plt.savefig('emotion_scores_of_a_product.png', dpi=300, bbox_inches='tight')
    
    

if __name__ == '__main__':
    scores_dict, des_dict = sentiment_analysis('tb_item.xlsx', 'scores_tb.xlsx')
    
    
    

    
