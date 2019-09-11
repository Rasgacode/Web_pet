from flask import Flask, request, render_template, redirect, url_for, make_response, session, escape
import background_functions
import data_manager, data_manager_users
import password_funct

app = Flask(__name__)


app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/set-cookie')
def cookie_insertion():
    redirect_to_index = redirect('/')
    response = make_response(redirect_to_index)
    response.set_cookie('cookie_name', value='values')
    return response


@app.route('/')
@app.route('/<wrong>')
def index(wrong=None):
    if 'username' in session:
        return render_template('index.html',
                               new_league=url_for('pick'),
                               continue_league=url_for('continue_', create='actual_league'),
                               logout=url_for('logout'),
                               logged_in_as=escape(session['username'])
                               )
    return render_template('index.html',
                           registration=url_for('registration'),
                           login=url_for('login'),
                           wrong=wrong,
                           )


@app.route('/reg', methods=['GET', 'POST'])
def registration():
    username = request.form['username']
    password = password_funct.hash_pass(request.form['password'])
    if username in data_manager_users.get_usernames():
        return redirect(url_for('index', wrong='taken'))
    data_manager_users.add_user({'username': username, 'password': password})
    return redirect("index")


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    if username not in data_manager_users.get_usernames() or len(username) == 0:
        return redirect(url_for('index', wrong='wrong'))
    elif password_funct.verify_pass(request.form['password'], data_manager_users.get_a_pass(username)):
        session['username'] = username
        return redirect(url_for('index'))
    return redirect(url_for('index', wrong='wrong'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/new/', methods=['GET', 'POST'])
def pick():
    if 'username' not in session:
        return redirect('index')
    if request.method == 'GET':
        data_manager.set_pos_def()
    if request.method == 'POST':
        data_manager.update_position(request.args.get('name'))
    table_in = data_manager.get_teams('in')
    table_out = data_manager.get_teams('out')
    return render_template('pick.html',
                           table_in=table_in,
                           table_out=table_out,
                           logged_in_as=escape(session['username']))


@app.route('/continue/<create>', methods=['GET', 'POST'])
def continue_(create):
    if 'username' not in session:
        return redirect('index')
    if create == 'create':
        new_schedule = background_functions.creat_schedule(data_manager.get_teams('out'))
        data_manager.creat_league_table_n_schedule(data_manager.get_teams('out'), new_schedule)
        next_round = background_functions.creat_round(data_manager.get_schedule())
        data_manager.set_last_round(next_round)
        last_round = data_manager.get_last_round()
    if create == 'actual_league':
        last_round = data_manager.get_last_round()
        next_round = background_functions.creat_round(data_manager.get_schedule())
        data_manager.set_last_round(next_round)
    return render_template('continue.html',
                           league_table=data_manager.get_league_table(),
                           next_round=next_round,
                           last_round=last_round,
                           logged_in_as=escape(session['username']))


if __name__ == '__main__':
    app.run(debug=True)
