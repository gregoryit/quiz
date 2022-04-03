from flask import Flask

def index():
    return '<a href="/test"> Начать викторину </a>'

def test():
    return '<p> Вопрос 1 и блаблбла </p>'


def result():
    return '<h1> Результат </h1>'

app = Flask(__name__) 
app.add_url_rule('/', 'index', index) 
app.add_url_rule('/test', 'test', test)
app.add_url_rule('/result', 'result', result)

if __name__ == '__main__':
   app.run(host='0.0.0.0')
