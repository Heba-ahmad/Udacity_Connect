from flask import Flask, render_template, request, redirect, url_for, flash
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from startup_setup import Startup, Base, Founder

app = Flask(__name__)
engine = create_engine('sqlite:///startup.db?check_same_thread=False')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

@app.route('/')
@app.route('/startups')
def index():
    startups = session.query(Startup).all()
    flash("new startup created!")
    flash("Startup Starter has been edited")
    flash("Startup Starter has been deleted")
    return render_template('index_startups.html', startups= startups)

@app.route('/startups/<int:startup_id>')
def startup(startup_id):
    startupQuery = session.query(Startup).filter_by(id=startup_id).one()
    foundersQuery = session.query(Founder).filter_by(startup_id=startup_id).all()
    flash("new founder created!")
    flash("Founder has been edited")
    flash("Founder has been deleted")
    return render_template('startup.html', startupQuery=startupQuery, foundersQuery=foundersQuery)

@app.route('/startups/new', methods=['GET','POST'])
def newStartup():
    if request.method=='POST':
        newstartup= Startup(name = request.form['name'])
        session.add(newstartup)
        session.commit()
        flash("new startup created!")
        return redirect(url_for('index'))
    else:
        return render_template('new.html')


@app.route('/startups/<int:startup_id>/editstarter', methods=['GET','POST'])
def editstarter(startup_id):
    editStartup = session.query(Startup).filter_by(id=startup_id ).one()
    if request.method == 'POST':
        if request.form['name']:
            editStartup.name = request.form['name']
        session.add(editStartup)
        session.commit()
        flash("Startup Starter has been edited")
        return redirect(url_for('index'))
    else:
		return render_template('editstarter.html', startup_id=startup_id, startup= editStartup)

@app.route('/startups/<int:startup_id>/deletestartup', methods=['GET','POST'])
def deleteStartup(startup_id):
    deletestartup = session.query(Startup).filter_by(id= startup_id).one()
    if request.method == 'POST':
        session.delete(deletestartup)
        session.commit()
        flash("Startup Starter has been deleted")
        return redirect(url_for('index'))
    else:
        return render_template('deletestarter.html', startup_id=startup_id, startup= deletestartup)

@app.route('/startups/<int:startup_id>/newfounder', methods=['GET','POST'])
def newFounder(startup_id):
    if request.method=='POST':
        newfounder= Founder(name = request.form['name'], bio= request.form['bio'], startup_id=startup_id)
        session.add(newfounder)
        session.commit()
        flash("new founder created!")
        return redirect(url_for('startup', startup_id=startup_id))
    else:
        return render_template('newfounder.html', startup_id=startup_id)

@app.route('/startups/<int:startup_id>/<int:founder_id>/editfounder', methods=['GET','POST'])
def editfounder(startup_id, founder_id):
    editedItem = session.query(Founder).filter_by(id = founder_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("Founder has been edited")
        return redirect(url_for('startup', startup_id=startup_id))
    else:
		return render_template('editfounder.html', startup_id=startup_id, founder_id=founder_id, founder=editedItem)

@app.route('/startups/<int:startup_id>/<int:founder_id>/deletefounder', methods=['GET','POST'])
def deleteFounder(startup_id, founder_id):
    deletefounder = session.query(Founder).filter_by(id = founder_id).one()
    if request.method == 'POST':
        session.delete(deletefounder)
        session.commit()
        flash("Founder has been deleted")
        return redirect(url_for('startup', startup_id=startup_id))
    else:
        return render_template('deletefounder.html', startup_id=startup_id, founder=deletefounder)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
