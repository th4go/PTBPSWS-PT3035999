import resend
from flask import current_app, render_template
from . import db
from .models import Email

def send_notification_email(new_username, custom_email):
    sender_email = current_app.config['API_FROM']
    
    html_content = f"""
    <h3>Novo Cadastro no Flasky</h3>
    <p><b>Usuário cadastrado:</b> {new_username}</p>
    <p><b>Nome do aluno:</b>Thiago Silva Barbosa</p>
    <p><b>Prontuário:</b>PT3035999</p>
    """
    
    recipients = [
        "flaskaulasweb@zohomail.com",
        "thiago.barbosa1@aluno.ifsp.edu.br",
        custom_email
    ]
    
    recipients_str = ",\n".join([f"'{email}'" for email in recipients])
    
    params = {
        "from": f"Flasky Admin <{sender_email}>",
        "to": recipients,
        "subject": "[Flasky] Novo usuário cadastrado",
        "html": html_content,
    }
    
    try:
        resend.Emails.send(params)
        print(f"E-mail enviado com sucesso para: {recipients}")
        
        email_log = Email(
            sender_name=new_username,
            recipients=recipients_str,
            subject="[Flasky] Novo usuário cadastrado",
            body=f"Novo usuário cadastrado: {new_username}"
        )
        db.session.add(email_log)
        db.session.commit()
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

def send_auth_email(to, subject, template, **kwargs):
    sender_email = current_app.config['API_FROM']
    
    # O Flask renderiza o template HTML da pasta do professor injetando as variáveis (como o token)
    html_content = render_template(template + '.html', **kwargs)
    
    params = {
        "from": f"Flasky Admin <{sender_email}>",
        "to": [to],
        "subject": f"[Flasky] {subject}",
        "html": html_content,
    }
    
    try:
        resend.Emails.send(params)
        print(f"E-mail de autenticação enviado com sucesso para: {to}")
    except Exception as e:
        print(f"Erro ao enviar o e-mail de autenticação: {e}")