from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.2pji0js.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


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