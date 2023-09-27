#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session,request
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

# @app.route('/articles')
# def index_articles():
#     session['page_views'] = session.get('page_views',0) 
#     # return make_response(jsonify(session), 200)
#     # response = make_response(jsonify({
#     #     'session':{
#     #         'session_value': session['page_views'],
#     #         'session_accessed': session.accessed,
#     #     },
#     #      'cookies': [{cookie: request.cookies[cookie]}
#     #         for cookie in request.cookies],
#     # }),200)
#     # response.set_cookie('mouse', 'Cookie')
#     # return response
#     articles = Article.query.all()
#     articles_list=[]
#     for article in articles:
#        article_dict ={
#             'id':article.id,
#             'author':article.author,
#             'title':article.title,
#             'content':article.content,
#             'preview':article.preview,
#             'minutes_to_read':article.minutes_to_read,
#             'date':article.date,
#         }
#        articles_list.append(article_dict)

#     return make_response(articles_list,200)

@app.route('/articles/<int:id>')
def show_article(id):
    session['page_views'] = session.get('page_views',0) 
    session['page_views'] +=1
    article =  Article.query.filter_by(id=id).first()
    if session['page_views'] <=3:
        # article_dict = article.to_dict()
        article_dict ={
          
            'author':article.author,
            'title':article.title,
            'content':article.content,
            'preview':article.preview,
            'minutes_to_read':article.minutes_to_read,
            'date':article.date,
        }
        return(jsonify(article_dict),200)
    

    else:
        r = {'message': 'Maximum pageview limit reached'}
        return jsonify(r),401
  

  
    

if __name__ == '__main__':
    app.run(port=5555,debug=True)
