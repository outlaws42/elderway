import sys
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
#from flask_babel import _, get_locale
#from guess_language import guess_language
from app import db
from app.main.forms import EditProfileForm, TeamForm
from app.models import User, Teams
#from app.translate import translate
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')



@bp.route('/qsg', methods=['GET', 'POST'])
@login_required
def qsg():
    teams = Teams.query.filter(Teams.user_id == current_user.id)
    form = TeamForm()
    if form.validate_on_submit():
        team = Teams(team=form.team.data.upper(), abbr=form.abbr.data.upper(), author=current_user)
        print(team, file=sys.stderr)
        try:
            db.session.add(team)
            db.session.commit()
            flash('{} was added!'.format(team.team), 'success')
        except Exception as e:
            flash('Team already exist', 'danger')
            print(e, file=sys.stderr)
        return redirect(url_for('main.qsg'))
    return render_template('qsg.html', title='Home', form=form, teams=teams)

@bp.route('/qsg_edit_team/<string:id>', methods=['GET', 'POST'])
@login_required
def qsg_edit_team(id):
    team = Teams.query.get(id)
    form = TeamForm(obj=team)

    if form.validate_on_submit():
        form.populate_obj(team)
        try:
            db.session.add(team)
            db.session.commit()
            flash('{} was changed successfully!'.format(team.team), 'success')
        except Exception as e:
            flash('Team already exist', 'danger')
            print(e, file=sys.stderr)
        return redirect(url_for('main.qsg'))
    return render_template('qsg_edit_team.html', title='Home', form=form)

@bp.route('/qsg_add_team', methods=['GET', 'POST'])
@login_required
def qsg_add_team():
    teams = Teams.query.filter(Teams.user_id == current_user.id)
    form = TeamForm()
    if form.validate_on_submit():
        team = Teams(team=form.team.data.upper(), abbr=form.abbr.data.upper(), author=current_user)
        print(team, file=sys.stderr)
        try:
            db.session.add(team)
            db.session.commit()
            flash('{} was added!'.format(team.team), 'success')
        except Exception as e:
            flash('Team already exist', 'danger')
            print(e, file=sys.stderr)
        return redirect(url_for('main.qsg'))
    return render_template('qsg_add_team.html', title='Home', form=form, teams=teams)

@bp.route('/qsg_delete_team/<string:id>', methods=['POST'])
@login_required
def qsg_delete_team(id):
    team = Teams.query.get(id)
    db.session.delete(team)
    db.session.commit()
    flash('{} Deleted'.format(team.team), 'success')
    return redirect(url_for('main.qsg'))

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    return render_template('user.html', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
