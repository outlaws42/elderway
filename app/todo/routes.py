import sys
import time
from datetime import datetime, date
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import TodoForm
from app.models import User, Todo
from app.todo import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/todo', methods=['GET', 'POST'])  
@login_required
def todo():
    todos = Todo.query.filter(Todo.user_id == current_user.id)
    return render_template('todo/todo.html', title='Todo', todos=todos)

@bp.route('/edit_todo/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_todo(id):
    todo = Todo.query.get(id)
    form = TodoForm(obj=todo)
    if form.validate_on_submit():
        form.populate_obj(todo)
        try:
            db.session.merge(todo)
            db.session.commit()
            flash('{} was changed successfully!'.format(todo.todo), 'success')
        except Exception as e:
            flash('Team already exist', 'danger')
            print(e, file=sys.stderr)
        return redirect(url_for('todo.todo'))
    return render_template('todo/add_todo.html', title='Edit Todo', form=form, type='Edit Todo', todo=todo)

@bp.route('/add_todo', methods=['GET', 'POST'])
@login_required
def add_todo():
    todo = Todo.query.filter(Todo.user_id == current_user.id)
    form = TodoForm()
    if form.validate_on_submit():
        todo = Todo(todo=form.todo.data, desc=form.desc.data, 
                    mc_number=form.mc_number.data, dnc_doc=form.dnc_doc.data,
                    prog_edit=form.prog_edit.data, status=form.status.data, 
                    fal=form.fal.data, author=current_user)
        try:
            db.session.add(todo)
            db.session.commit()
            flash('{} was added!'.format(todo), 'success')
        except Exception as e:
            flash('Team already exist', 'danger')
            print(e, file=sys.stderr)
        return redirect(url_for('todo.todo'))
    return render_template('todo/add_todo.html', title='Add Todo', form=form, todo=todo, type='Add Todo')

@bp.route('/delete_todo/<string:id>', methods=['POST'])
@login_required
def delete_todo(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    flash('{} Deleted'.format(todo.todo), 'success')
    return redirect(url_for('todo.todo'))

