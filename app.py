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
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('comb.html', user_info=payload['id'])
    except jwt.ExpiredSignatureError:
        return render_template('comb.html', msg="로그인 시간이 만료되었습니다.")
    except jwt.exceptions.DecodeError:
        return render_template('comb.html', msg="로그인 정보가 존재하지 않습니다.")


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

# author: 김학준
# function: 로그인
@app.route('/login', methods=['POST'])
def login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.utcnow() + timedelta(minutes=30) # 30분 후 만료
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # access_token 전송
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '회원 정보가 없습니다.'})

@app.route('/post_place', methods=['POST'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


@app.route('/sort_places', methods=['GET'])
def sort_places():
    sort_receive = request.args.get('sort_give')
    sorted_list = list(db.places.find({},{'_id':False}).sort("sort_receive", -1))

    return jsonify({'result': 'success'})

# author: 안진우
# function: 리뷰 조회, 등록, 삭제
@app.route('/')
def home():
    review_list = list(db.review.find({}, {'_id': False}))
    count = len(review_list)
    avg = 0

    for review in review_list :
        avg = round(avg + int(review['star']) / count, 2)

    return render_template('index.html', reviews=review_list, count=count, avg=avg)

@app.route("/review", methods=["POST"])
def review_post():
    review_list = list(db.review.find({}, {'_id': False}))
    count = len(review_list) + 1

    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    star_recive = request.form['star_give']

    doc = {
        'name' : name_receive,
        'star': star_recive,
        'comment' : comment_receive,
        'num' : count
    }

    db.review.insert_one(doc)
    return jsonify({'msg':'리뷰 작성 완료!!'})

@app.route("/review", methods=["GET"])
def review_get():
    review_list = list(db.review.find({}, {'_id': False}))
    return jsonify({'reviews':review_list})

@app.route("/review/delete", methods=["POST"])
def review_delete():
    del_receive = request.form['del_give']
    db.review.delete_one({'name':del_receive})
    print(del_receive)
    return jsonify({'msg': f'{del_receive}님 리뷰 삭제'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)