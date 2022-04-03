import os
from random import shuffle
from flask import Flask, session, request, redirect, render_template, url_for
from db_scripts import get_question_after, get_quises, check_answer

def start_quiz(quiz_id):
    '''создаёт нужные значения в словаре session'''
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['answers'] = 0
    session['total'] = 0

def end_quiz():
    session.clear()

def quiz_form():
    ''' функция получает список викторин из базы и формирует форму с выпадающим списком'''
    q_list = get_quises()
    return render_template('start.html', q_list=q_list)

def index():
    ''' Первая страница: если пришли запросом GET, то выбрать викторину, 
    если POST - то запомнить id викторины и отправлять на вопросы'''
    if request.method == 'GET':
        # викторина не выбрана, сбрасываем id викторины и показываем форму выбора
        start_quiz(-1)
        return quiz_form()
    else:
        # получили дополнительные данные в запросе! Используем их:
        quest_id = request.form.get('quiz') # выбранный номер викторины 
        start_quiz(quest_id)
        return redirect(url_for('test'))

def save_answers():
    '''получает данные из формы, проверяет, верен ли ответ, записывает итоги в сессию'''
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')
    # этот вопрос уже задан:
    session['last_question'] = quest_id
    # увеличиваем счетчик вопросов:
    session['total'] += 1
    # проверить, совпадает ли ответ с верным для этого id
    if check_answer(quest_id, answer):
        session['answers'] += 1

def question_form(question):
    '''получает строку из базы данных, соответствующую вопросу, возвращает html с формой '''
    # question - результат работы get_question_after
    # поля: 
            # [0] - номер вопроса в викторине, 
            # [1] - текст вопроса, 
            # [2] - правильный ответ, [3],[4],[5] - неверные

    # перемешиваем ответы:
    answers_list = [
        question[2], question[3], question[4], question[5]
    ]
    shuffle(answers_list)
    # передаём в шаблон, возвращаем результат:
    return render_template('test.html', question=question[1], quest_id=question[0], answers_list=answers_list)

def test():
    '''возвращает страницу вопроса'''
    # что если пользователь без выбора викторины пошел сразу на адрес '/test'? 
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        # если нам пришли данные, то их надо прочитать и обновить информацию:
        if request.method == 'POST':
            save_answers()
        # в любом случае разбираемся с текущим id вопроса
        next_question = get_question_after(session['last_question'], session['quiz'])
        if next_question is None or len(next_question) == 0:
            # вопросы закончились:
            return redirect(url_for('result'))
        else:            
            return question_form(next_question)

def result():
    html = render_template('result.html', right=session['answers'], total=session['total'])
    end_quiz()
    return html

folder = os.getcwd() # запомнили текущую рабочую папку
# Создаём объект веб-приложения:
app = Flask(__name__, template_folder=folder, static_folder=folder)  
app.add_url_rule('/', 'index', index, methods=['post', 'get'])   # создаёт правило для URL '/'
app.add_url_rule('/test', 'test', test, methods=['post', 'get']) # создаёт правило для URL '/test'
app.add_url_rule('/result', 'result', result) # создаёт правило для URL '/test'
# Устанавливаем ключ шифрования:
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'

if __name__ == "__main__":
    # Запускаем веб-сервер:
    app.run()
