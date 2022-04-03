from flask import Flask, session


def index():
   session['counter'] = 0
   return '<a href="/counter">Дальше</a>'
 
def counter():
   
   session['counter'] += 1
   return '<h1>' + str(session['counter']) + '</h1>'

app = Flask(__name__)

app.add_url_rule('/', 'index', index) 
app.add_url_rule('/counter', 'counter', counter)
app.config['SECRET_KEY'] = 'asdoi;fusdoi;afgasiof`12321312dsf' 

 
if __name__ == '__main__':
   app.run(host='0.0.0.0')
