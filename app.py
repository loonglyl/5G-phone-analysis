from flask import Flask, render_template
from flask import redirect
from flask import url_for
from flask import request
from read_xslx import read_only
from sentiment_analysis_new import sentiment_analysis_new
from visual_tools_new import generate_wordcloud_of_an_item, plot_scores_of_an_item
import shutil
from radar_graph import radar


# 放置图片<img src="{{ url_for('static', filename='images/20180819002220436.png') }}">
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sfasf'    # 配置SECRET_KEY，该值为任意字符

@app.route('/', methods=["GET", "POST"])
def root():
    # title = 'xxxxxxxxxx'
    # flash('验证成功xxxxx')  # 使用flash方法传递信息
    # return render_template('index.html', Heading=title)
    return render_template('index.html')  # 弹窗


@app.route('/huawei', methods=['GET', 'POST'])
def huawei():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))
    item_list_var, _ = read_only("jd_item.xlsx")
    categorized_list = []
    for i in item_list_var:
        if i['category'] == "华为":
            categorized_list.append(i)
    # print(item_list_var)
    # item_list_var = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
    # show the form, it wasn't submitted
    return render_template('second.html', manufacturer="huawei", item_list=categorized_list)


@app.route('/apple', methods=['GET', 'POST'])
def apple():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))
    item_list_var, _ = read_only("jd_item.xlsx")
    categorized_list = []
    for i in item_list_var:
        if i['category'] == "apple":
            categorized_list.append(i)
    # show the form, it wasn't submitted
    return render_template('second.html', manufacturer="apple", item_list=categorized_list)


@app.route('/xiaomi', methods=['GET', 'POST'])
def xiaomi():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))
    item_list_var, _ = read_only("jd_item.xlsx")
    categorized_list = []
    for i in item_list_var:
        if i['category'] == "小米":
            categorized_list.append(i)
    # show the form, it wasn't submitted
    return render_template('second.html', manufacturer="xiaomi", item_list=categorized_list)


@app.route('/samsung', methods=['GET', 'POST'])
def samsung():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))
    item_list_var, _ = read_only("jd_item.xlsx")
    categorized_list = []
    for i in item_list_var:
        if i['category'] == "三星":
            categorized_list.append(i)
    # show the form, it wasn't submitted
    return render_template('second.html', manufacturer="samsung", item_list=categorized_list)


@app.route('/honor', methods=['GET', 'POST'])
def honor():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))
    item_list_var, _ = read_only("jd_item.xlsx")
    categorized_list = []
    for i in item_list_var:
        if i['category'] == "荣耀":
            categorized_list.append(i)
    # show the form, it wasn't submitted
    return render_template('second.html', manufacturer="honor", item_list=categorized_list)


@app.route('/oppo', methods=['GET', 'POST'])
def oppo():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))
    item_list_var, _ = read_only("jd_item.xlsx")
    categorized_list = []
    for i in item_list_var:
        if i['category'] == "oppo":
            categorized_list.append(i)
    # show the form, it wasn't submitted
    return render_template('second.html', manufacturer="oppo", item_list=categorized_list)


@app.route('/vivo', methods=['GET', 'POST'])
def vivo():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))
    item_list_var, _ = read_only("jd_item.xlsx")
    categorized_list = []
    for i in item_list_var:
        if i['category'] == "vivo":
            categorized_list.append(i)
    # show the form, it wasn't submitted
    return render_template('second.html', manufacturer="vivo", item_list=categorized_list)


@app.route('/iqoo', methods=['GET', 'POST'])
def iqoo():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))
    item_list_var, _ = read_only("jd_item.xlsx")
    categorized_list = []
    for i in item_list_var:
        if i['category'] == "iqoo":
            categorized_list.append(i)
    # show the form, it wasn't submitted
    return render_template('second.html', manufacturer="iqoo", item_list=categorized_list)


@app.route('/redmi', methods=['GET', 'POST'])
def redmi():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))
    item_list_var, _ = read_only("jd_item.xlsx")
    categorized_list = []
    for i in item_list_var:
        if i['category'] == "红米":
            categorized_list.append(i)
    # show the form, it wasn't submitted
    return render_template('second.html', manufacturer="redmi", item_list=categorized_list)


@app.route('/oneplus', methods=['GET', 'POST'])
def oneplus():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))
    item_list_var, _ = read_only("jd_item.xlsx")
    categorized_list = []
    for i in item_list_var:
        if i['category'] == "一加":
            categorized_list.append(i)
    # show the form, it wasn't submitted
    return render_template('second.html', manufacturer="oneplus", item_list=categorized_list)


@app.route('/realme', methods=['GET', 'POST'])
def realme():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))
    item_list_var, _ = read_only("jd_item.xlsx")
    categorized_list = []
    for i in item_list_var:
        if i['category'] == "真我":
            categorized_list.append(i)
    # show the form, it wasn't submitted
    return render_template('second.html', manufacturer="realme", item_list=categorized_list)


@app.route('/meizu', methods=['GET', 'POST'])
def meizu():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))
    item_list_var, _ = read_only("jd_item.xlsx")
    categorized_list = []
    for i in item_list_var:
        if i['category'] == "魅族":
            categorized_list.append(i)
    # show the form, it wasn't submitted
    return render_template('second.html', manufacturer="meizu", item_list=categorized_list)


@app.route('/<category>/id/<int:k>', methods=['GET', 'POST'])
def phone(category, k):
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))
    item_list_var, link_list = read_only("jd_item.xlsx")
    item_list = item_list_var[k - 1]
    link = link_list[k - 1]
    scores_dict, des_dict = sentiment_analysis_new(item_list, 'jd_scores.xlsx', 'jd_des.txt')
    generate_wordcloud_of_an_item('jd_des.txt', str(k))
    best_comments = "None"
    with open('jd_des.txt', 'r') as f:
        for line in f:
            key, good, bad, best = line.strip().split('||')
            if key == str(k):
                best_comments = best
            else:
                continue
    plot_scores_of_an_item('jd_scores.xlsx', k)
    # show the form, it wasn't submitted
    radar('jd_item.xlsx', k)
    return render_template('third.html', manufacturer=category, id_num=str(k), item_list=item_list, specification_dict=item_list['specifications'], best_comments=best_comments, link=link)


if __name__ == "__main__":
    app.run()
    path = 'static/wordcloud_pictures'
    shutil.rmtree(path)  # 递归删除文件夹，即：删除非空文件夹
    path = 'static/score_pictures'
    shutil.rmtree(path)
    path = 'static/radar'
    shutil.rmtree(path)
    path = 'jd_scores.xlsx'
    shutil.rmtree(path)
    path = 'jd_des.txt'
    shutil.rmtree(path)
