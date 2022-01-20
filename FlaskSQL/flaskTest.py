from flask import Flask, render_template, request, escape
from vsearch import search4letters
import mysql.connector

dbconfig = {'host': 'localhost', 'user': 'vsearch', 'password': 'vsearchpasswd', 'database': 'vsearchlogDB', 'port': 3309} # Наши данные по подключению к бд

app = Flask(__name__)


def log_request(req: 'flask_request', res: str) -> None:
    '''
        Этот код сохраняет значения в файл
    with open('vsearch.log', 'a') as log:
            #print(str(dir(req)), res, file=log) # dir(req) - возвращает список методов и атрибутов этого объекта

            # Выводим четыре нужных нам значения веб-запроса: 1) что ввел пользователь; 2) айпишник, с которого произошли изменения;
            # 3) браузер, который использует пользователь; 4) результат запроса

            print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')

            # КСТАТИ! "sep" - разделитель, который используется для написания в одну строку (print)
    '''

    '''А этот сохраняет в БД (используется mysql)'''
    conn = mysql.connector.connect(**dbconfig) # Звездочки обязательны!!!
    cursor = conn.cursor() # Открываем соединение
    _SQL = """insert into log (phrase, letters, ip, browser_string, results) values (%s, %s, %s, %s, %s)"""
    cursor.execute(_SQL, (req.form['phrase'],
                          req.form['letters'],
                          req.remote_addr,
                          req.user_agent.browser,
                          res,))

    conn.commit() # Следующие три строки закрывают соединение
    cursor.close()
    conn.close()


@app.route('/search4', methods=['POST'])
def do_search()-> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    query = str(search4letters(phrase, letters))

    title = 'Здесь Ваш результат:'
    results = query
    log_request(request, results)
    the_letters = letters
    the_phrase = phrase

    return render_template('results.html',
                           the_phrase = phrase,
                           the_title = title,
                           the_letters = letters,
                           the_results = results,)

@app.route('/') # Два url ассоциируются с одной функцией, соотвественно, нагрузки на ресуры у нас не будет
@app.route('/entry')
def entry_page() -> 'html':
        return render_template('entry.html',
                               the_title = 'Приветствуем Вас!')

@app.route('/viewlog')
def view_the_log() -> str: # Аннотация - функция чтения журнала из файла vsearch.log, возвращаем строку
    #with open('vsearch.log') as log:
        #contents = log.readlines() # метод read() (есть только с инструкцией with) позволяет прочитать за раз все содержимое файла (альтернатива циклу)
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([]) # список списков
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Введенные пользователем данные', 'IP-адрес', 'Браузер пользователя (агент)', 'Результат') # Кортеж из заголовков
    return render_template('viewlog.html', # Открываем нужный нам файл
                           the_title='View Log', # Название самой страницы
                           the_row_titles=titles, # Кортеж заголовков
                           the_data=contents,) # Сами данные

#app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)
