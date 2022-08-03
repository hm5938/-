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

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')

    #맛집 리스트 불러오기
    place_list = list(db.places.find({}, {}))
    result = make_restaurants_list(place_list)

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('comb.html', user_info=payload['id'] , restaurant_list=result)
    except jwt.ExpiredSignatureError:
        return render_template('comb.html', msg="로그인 시간이 만료되었습니다.",restaurant_list=result)
    except jwt.exceptions.DecodeError:
        return render_template('comb.html', msg="로그인 정보가 존재하지 않습니다.", restaurant_list=result)


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

# 토큰 필요한 작업에 주기
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

# 정렬(미완성)
@app.route('/sort_places', methods=['GET'])
def sort_places():
    sort_receive = request.args.get('sort_give')
    sorted_list = list(db.places.find({},{'_id':False}).sort("sort_receive", -1))

    return jsonify({'result': 'success'})


# Author : 이혜민
# Function : 서버사이드렌더링을 위한 데이터 전달
def find_review_with_place(place_id):
    review_list = list(db.review.find({'place_id':place_id}, {'_id': False}))
    count = len(review_list)
    avg = 0
    for review in review_list :
        avg = round(avg + int(review['star']) / count, 2)
    return {'reviews':review_list,'count':count,'avg':avg}

def make_restaurants_list(place_list):
    result = list()
    for place in place_list :

        print(place)
        id = place['_id']
        reviews = find_review_with_place(id)
        title=place['title']
        address =place['address']
        category =place['category']
        desc=place['desc']
        img =place['img']
        review_list = reviews['reviews']
        review_total = reviews['count']
        star_total = reviews['avg']

        result.append({
            'id':id,
            'title': title,
            'address':address,
            'category':category,
            'desc':desc,
            'img':img,
            'review_list':review_list,
            'review_total':review_total,
            'star_total': star_total
        })

    return result

# author: 이혜민
# function: 검색
@app.route('/search/<search_name>')
def search(search_name):
    rgx = re.compile('.*' + search_name+ '.*', re.IGNORECASE)  # compile the regex
    place_list = list(db.places.find({'title': rgx}, {}))
    print(len(place_list))

    if len(place_list) != 0:
        result = make_restaurants_list(place_list)
        return render_template('comb.html', restaurant_list=result)
    else:
        return render_template('comb.html', mgs='검색결과가 존재하지 않습니다.')


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

    # 정연님 코드
    place = soup.select("ul.restaurant_list > div > div > li > div > a")

    title = place.select_one("strong.box_module_title").text
    address = place.select_one("div.box_module_cont > div > div > div.mil_inner_spot > span.il_text").text
    img = place.select_one("img.box_module_image")["src"]
    desc = place.select_one("span.box_module_stitle").text.strip()
    ##

    # title = soup.select_one('가게 이름 크롤링')
    # img = soup.select_one('가게 이미지 크롤링')
    # desc = soup.select_one('가게 소개 크롤링')
    # address = soup.select_one('가게 주소 크롤링')

    doc = {
        'category': category_receive,
        'star': star_receive,
        'comment': comment_receive,
        'title':title,
        'img':img,
        'desc':desc,
        'address':address
    }
    db.restaurants.insert_one(doc)

    return jsonify({'msg': '등록 완료'})

#카테고리별 포스트 카드 붙여넣기
@app.route("/<keyword>", methods=["GET"])
def restaurant_get(keyword):
    restaurant_list = list(db.restaurants.find({"category": str(keyword)}))

    return render_template("comb.html", restaurant_list=restaurant_list)


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