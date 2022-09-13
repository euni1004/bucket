from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.iygss54.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']

    bucket_list = list(db.bucket.find({}, {'_id': False}))
    b_list = []
    for i in bucket_list:
        b_list.append(i['num'])
    count = int(max(b_list)) + 1

    doc={
        'num': count,
        'bucket': bucket_receive,
        'done': 0
    }
    db.bucket.insert_one(doc)

    return jsonify({'msg': '등록완료'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '버킷 완료!'})

@app.route("/bucket/cancel", methods=["POST"])
def bucket_cancel():
    cancel_receive = request.form['cancel_give']
    db.bucket.update_one({'num': int(cancel_receive)}, {'$set': {'done': 0}})
    return jsonify({'msg': '버킷 취소 완료!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': bucket_list})

@app.route("/bucket/delete", methods=["POST"])
def bucket_del():
    del_receive = request.form['delete_give']
    db.bucket.delete_one({'num': int(del_receive)})
    return jsonify({'msg': '삭제 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)