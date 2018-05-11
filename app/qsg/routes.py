import sys
import time
from datetime import datetime, date
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, send_file, send_from_directory
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, TeamForm
from app.models import User, Teams
from app.qsg.xlsx_export import ExportXlsx
from app.qsg.pdf_export import ExportPdf
from app.qsg import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/qsg', methods=['GET', 'POST'])
@login_required
def qsg():
    teams = Teams.query.filter(Teams.user_id == current_user.id)
    return render_template('qsg/qsg.html', title='QSG Web', teams=teams)

@bp.route('/qsg_edit_team/<string:id>', methods=['GET', 'POST'])
@login_required
def qsg_edit_team(id):
    team = Teams.query.get(id)
    form = TeamForm(obj=team)
    if form.validate_on_submit():
        form.populate_obj(team)
        print(team.team.upper(), sys.stdout)
        try:
            db.session.merge(team)
            db.session.commit()
            flash('{} was changed successfully!'.format(team.team.upper()), 'success')
        except Exception as e:
            flash('Team already exist', 'danger')
            print(e, file=sys.stderr)
        return redirect(url_for('qsg.qsg'))
    return render_template('qsg/qsg_add_team.html', title='Edit Team', form=form, type='Edit Team')

@bp.route('/qsg_add_team', methods=['GET', 'POST'])
@login_required
def qsg_add_team():
    teams = Teams.query.filter(Teams.user_id == current_user.id)
    form = TeamForm()
    if form.validate_on_submit():
        team = Teams(team=form.team.data, abbr=form.abbr.data, author=current_user)
        try:
            db.session.add(team)
            db.session.commit()
            flash('{} was added!'.format(team.team), 'success')
        except Exception as e:
            flash('Team already exist', 'danger')
            print(e, file=sys.stderr)
        return redirect(url_for('qsg.qsg'))
    return render_template('qsg/qsg_add_team.html', title='Add Team', form=form, teams=teams,type='Add Team')

@bp.route('/qsg_delete_team/<string:id>', methods=['POST'])
@login_required
def qsg_delete_team(id):
    team = Teams.query.get(id)
    db.session.delete(team)
    db.session.commit()
    flash('{} Deleted'.format(team.team), 'success')
    return redirect(url_for('qsg.qsg'))

@bp.route('/qsg_gen_sch/<type>', methods=['GET', 'POST'])
@login_required
def qsg_gen_sch(type):
    filename = '{}_schedule_{}-{}.{}'.format(current_user.username,date.today(),time.strftime("%H-%M-%S"),type)
    print(filename)
    if type == 'pdf':
        ExportPdf(filename)
    else:
        ExportXlsx(filename)
    
    flash('Schedule Generated {}'.format(filename), 'success')
    return render_template('qsg/qsg_download.html', filename=filename, type=type, title='QSG Download')

@bp.route('/return-files/<filename>', methods=['GET', 'POST'])
@login_required
def return_files(filename):   
    return send_from_directory(directory='static/schedule', filename=filename , as_attachment=True )
