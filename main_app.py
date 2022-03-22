import time
import pymongo
from flask import Flask, render_template, request

# 创建Flask对象
app = Flask(__name__)
# 创建mongodb客户端
client = pymongo.MongoClient()
db = client.ybc


# 路由：'欢迎页面'
@app.route('/welcome')
def welcome():
    # 获取当前系统的时间
    now = time.localtime()
    # 转化日期格式
    date_time = time.strftime('%Y-%m-%d %H:%M', now)
    return render_template('welcome.html', t_time=date_time)


# 路由，'猿力家族 X 四大名著'
@app.route('/quiz')
def quiz():
    return render_template('quiz.html')


# 路由，刷新'答题页'
@app.route('/quiz_question')
def quiz_question():
    return render_template('quiz.html')


# 路由，'答题页'
@app.route('/quiz_question', methods=['POST'])
def get_question():
    nickname = request.form['nickname']
    return render_template('quiz_question.html',
                           t_nickname=nickname)


# 路由，刷新‘结果页’
@app.route('/quiz_result')
def get_quiz_result():
    return render_template('quiz.html')


# 路由，'匹配角色，返回测试结果'
@app.route('/quiz_result', methods=['POST'])
def quiz_result():
    # 获取昵称数据
    nickname = request.form['nickname']
    # 获取答题数据
    answer1 = request.form['answer1']
    answer2 = request.form['answer2']
    answer3 = request.form['answer3']
    answer4 = request.form['answer4']
    answer5 = request.form['answer5']
    # 创建答题列表
    answer_list = [answer1, answer2, answer3, answer4, answer5]
    # 使用get_role功能，匹配出最适合的人物
    role = get_role(answer_list)
    # 返回结果页面
    return render_template('quiz_result.html',
                           t_role=role, t_nickname=nickname)


# 路由，’保存装扮‘
@app.route('/dress_result', methods=['POST'])
def dress_result():
    nickname = request.form['nickname']
    role = request.form['role']
    stage = request.form['stage']
    title = request.form['title']
    time = get_date_time()
    data = {
        'nickname': nickname,
        'role': role,
        'stage': stage,
        'title': title,
        'time': time
    }
    db.dress.insert_one(data)
    dress_list = list(db.dress.find({}))
    return render_template('dress.html', t_dress=dress_list)


# 路由，'直接查看装扮大观园‘
@app.route('/dress_result')
def dress_list():
    dress_list = list(db.dress.find({}))
    return render_template('dress.html', t_dress=dress_list)


# 匹配最适合人物的方法
def get_role(answer_list):
    max_option = max(answer_list, key=answer_list.count)
    roles = {'A': '三国演义-关羽',
             'B': '西游记-孙悟空',
             'C': '红楼梦-林黛玉',
             'D': '水浒传-武松'}
    role = roles[max_option]
    return role


# 获取当前时间并格式化
def get_date_time():
    # 获取当前系统的时间
    now = time.localtime()
    # 转化日期格式
    date_time = time.strftime('%Y-%m-%d %H:%M:%S', now)
    return date_time


if __name__ == '__main__':
    app.run(port=5001, debug=True)
