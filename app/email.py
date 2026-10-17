import resend
from flask import current_app
from . import db
from .models import Email

def send_notification_email(new_username):
    sender_email = current_app.config['API_FROM']
    
    html_content = f"""
    <h3>Novo Cadastro no Flasky</h3>
    <p><b>Usuário cadastrado:</b> {new_username}</p>
    <p><b>Nome do aluno:</b> Thiago Silva Barbosa</p>
    <p><b>Prontuário:</b> PT3035999</p>
    """
    
    # E-mail fixo conforme exigência da atividade
    recipients = [
        "flaskaulasweb@zohomail.com",
        "thiago.barbosa1@aluno.ifsp.edu.br"
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