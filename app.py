from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbjungle

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/list', methods=['GET'])
def show_stars():
    stars = list(db.mystar.find({}, {'_id': False}).sort('like', -1))

    return jsonify({'result': 'success', 'stars_list': stars})

@app.route('/api/like', methods=['POST'])
def like_stars():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    name_receive = request.form['name_give']
    # 2. mystar 목록에서 find_one으로 name이 name_receive와 일치하는 star를 찾습니다.
    star = db.mystar.find_one({'name': name_receive})
    # 3. star의 like 에 1을 더해준 new_like 변수를 만듭니다.
    new_like = star['like']+1
    # 4. mystar 목록에서 name이 name_receive인 문서의 like 를 new_like로 변경합니다.
    db.mystar.update_one({'name': name_receive}, {'$set': {'like': new_like}})

    return jsonify({'result': 'success'})

@app.route('/api/delete', methods=['POST'])
def delete_starvotes():
    name_receive = request.form['name_give']
    star = db.mystar.find_one({'name': name_receive})
    db.mystar.delete_one({'name': name_receive})

    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
