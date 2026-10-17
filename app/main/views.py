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
            
            # Dispara o e-mail automático (salvando também no banco)
            send_notification_email(user.username)
        else:
            session['known'] = True
            
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main.index'))

    return render_template('index.html', 
                           form=form, 
                           name=session.get('name'), 
                           known=session.get('known', False))