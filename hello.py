# A very simple Flask Hello World app for you to get started with...
from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello_world():
    return '<p>Alterações por meio do PythonAnyWhere -> GitHub</p><table><tr><td><b>Professor:</b></td><td>Professor Fabio Teixeira</td></tr><tr><td><b>Prontuário:</b></td><td>PT3935999</td></tr></table>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)

@app.route('/contextorequisicao')
def contextorequisicao():
    user_agent = request.headers.get('User-Agent')
    return '<p>Você está usando o navegador: {}'.format(user_agent)

@app.route('/codigostatusdiferente')
def codigostatusdiferente():
    return '<h1>Bad Request</h1>', 400

@app.route('/objetoresposta')
def objetoresposta():
    resposta = make_response('<h1>Document Cookies</h1>')
    resposta.set_cookie('id_sessao', '12345')
    return resposta

# REDIRECIONAMENTO
@app.route('/redirecionamento')
def redirecionamento():
    return redirect('https://ptb.ifsp.edu.br/')

# ABORT 404
@app.route('/abortar')
def abortar():
    abort(404)