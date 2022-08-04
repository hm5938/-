from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import re

app = Flask(__name__)
client = MongoClient('mongodb+srv://test:sparta@Cluster0.dlhbsnt.mongodb.net/Cluster()?retryWrites=true&w=majority')
db = client.dbsparta

SECRET_KEY = 'SPARTA'


# Author : 이혜민
# Function : 서버사이드렌더링을 위한 데이터 전달
@app.route('/')
def home():
    result = list()
    place_list = list(db.places.find({}, {}))
    for place in place_list:
        print(place)
        id = place['_id']
        reviews = find_review_with_place(id)
        title = place['title']
        address = place['address']
        category = place['category']
        desc = place['desc']
        img = place['img']
        review_list = reviews['reviews']
        review_total = reviews['count']
        star_total = reviews['avg']

        result.append({
            'id': id,
            'title': title,
            'address': address,
            'category': category,
            'desc': desc,
            'img': img,
            'review_list': review_list,
            'review_total': review_total,
            'star_total': star_total
        })

    print(result)
    return render_template('test.html', restaurants=result)


def find_review_with_place(place_id):
    print(list(db.review.find({}, {'_id': False})))
    review_list = list(db.reviews.find({'place_id': place_id}, {'_id': False}))
    count = len(review_list)
    avg = 0
    for review in review_list:
        avg = round(avg + int(review['star']) / count, 2)
    return {'reviews': review_list, 'count': count, 'avg': avg}


def make_restaurants_list(place_list):
    result = list()
    for place in place_list:
        print(place)
        id = place['_id']
        reviews = find_review_with_place(id)
        title = place['title']
        address = place['address']
        category = place['category']
        desc = place['desc']
        img = place['img']
        review_list = reviews['reviews']
        review_total = reviews['count']
        star_total = reviews['avg']

        result.append({
            'id': id,
            'title': title,
            'address': address,
            'category': category,
            'desc': desc,
            'img': img,
            'review_list': review_list,
            'review_total': review_total,
            'star_total': star_total
        })
        print(result)
    return result


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


# author: 이혜민
# function: 검색
@app.route('/search/<search_name>')
def search(search_name):
    rgx = re.compile('.*' + search_name + '.*', re.IGNORECASE)  # compile the regex
    place_list = list(db.places.find({'title': rgx}, {}))
    print(len(place_list))

    if len(place_list) != 0:
        result = make_restaurants_list(place_list)
        return render_template('test.html', restaurants=result)
    else:
        return render_template('test.html', mgs='검색결과가 존재하지 않습니다.')


# author: 안진우
# function: 리뷰 조회, 등록, 삭제

@app.route("/review", methods=["POST"])
def review_post():
    review_list = list(db.review.find({}, {'_id': False}))
    count = len(review_list) + 1

    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    star_recive = request.form['star_give']

    doc = {
        'name': name_receive,
        'star': star_recive,
        'comment': comment_receive,
        'num': count
    }

    db.review.insert_one(doc)
    return jsonify({'msg': '리뷰 작성 완료!!'})


@app.route("/review", methods=["GET"])
def review_get():
    review_list = list(db.review.find({}, {'_id': False}))
    return jsonify({'reviews': review_list})


@app.route("/review/delete", methods=["POST"])
def review_delete():
    del_receive = request.form['del_give']
    db.review.delete_one({'name': del_receive})
    print(del_receive)
    return jsonify({'msg': f'{del_receive}님 리뷰 삭제'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
