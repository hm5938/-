@app.route('/')
def home():
    result = list()
    place_list = list(db.places.find({}, {}))
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
        print(result)


    return render_template('comb2.html', restaurants=result)

def find_review_with_place(place_id):
    review_list = list(db.reviews.find({'place':place_id}, {'_id': False}))
    count = len(review_list)
    avg = 0
    for review in review_list :
        avg = round(avg + int(review['star']) / count, 2)
    return {'reviews':review_list,'count':count,'avg':avg}
