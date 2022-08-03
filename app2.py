from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
app = Flask(__name__)
client = MongoClient('mongodb+srv://test:sparta@Cluster0.dlhbsnt.mongodb.net/Cluster()?retryWrites=true&w=majority')
db = client.dbtest

SECRET_KEY = 'SPARTA'

@app.route('/')
def home():
    return render_template('comb.html')

# Author : 이혜민
# Function : 회원가입
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "id": username_receive,
        "pw": password_hash,
    }
    db.user.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.user.find_one({"id": username_receive}))
    # print(value_receive, type_receive, exists)
    return jsonify({'result': 'success', 'exists': exists})


# Author : 손지아
# Function : 포스팅
@app.route("/post_place", methods=["POST"])
def restaurant_post():
    url_receive = request.form['url_give']
    category_receive = request.form['category_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    name = soup.select_one('가게 이름 크롤링')
    image = soup.select_one('가게 이미지 크롤링')
    desc = soup.select_one('가게 소개 크롤링')
    spot = soup.select_one('가게 주소 크롤링')

    doc = {
        'category': category_receive,
        'star': star_receive,
        'comment': comment_receive,
        'name':name,
        'image':image,
        'desc':desc,
        'spot':spot
    }
    db.restaurants.insert_one(doc)

    return jsonify({'msg': '등록 완료'})

#카테고리별 포스트 카드 붙여넣기
@app.route("/<keyword>", methods=["GET"])
def restaurant_get(keyword):
    restaurant_list = list(db.restaurants.find({"category": str(keyword) }))

    return render_template("comb.html", restaurant_list=restaurant_list)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
