from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User, Role
from ..email import send_notification_email

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        
        if user is None:
            user_role = Role.query.filter_by(name='User').first()
            user = User(username=form.name.data, role=user_role)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            
            send_notification_email(user.username, form.email.data)
            session['email_sent'] = True
        else:
            session['known'] = True
            session['email_sent'] = False
            
        session['name'] = form.name.data
        form.name.data = ''
        form.email.data = ''
        return redirect(url_for('main.index'))

    users = User.query.all()
    email_sent = session.pop('email_sent', False)

    return render_template('index.html', 
                           form=form, 
                           name=session.get('name'), 
                           known=session.get('known', False),
                           users=users,
                           email_sent=email_sent)

@main.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('Usuário removido com sucesso.', 'warning')
    return redirect(url_for('main.index'))

@main.route('/edit/<int:id>', methods=['POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    new_name = request.form.get('new_name')
    if new_name:
        user.username = new_name
        db.session.commit()
        flash('Nome do usuário atualizado com sucesso.', 'success')
    return redirect(url_for('main.index'))