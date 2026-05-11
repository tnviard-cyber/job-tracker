from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://") if os.environ.get('DATABASE_URL') else 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='Envoyée')
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    cv_used = db.Column(db.String(200))
    cover_letter = db.Column(db.String(200))
    response = db.Column(db.Text)
    notes = db.Column(db.Text)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    jobs = JobApplication.query.order_by(JobApplication.id.desc()).all()
    return render_template('index.html', jobs=jobs)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        job = JobApplication(
            company=request.form['company'],
            position=request.form['position'],
            status=request.form['status'],
            cv_used=request.form['cv'],
            cover_letter=request.form['cover'],
            response=request.form['response'],
            notes=request.form['notes']
        )
        db.session.add(job)
        db.session.commit()
        flash('✅ Candidature ajoutée !')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
    job = JobApplication.query.get(id)
    db.session.delete(job)
    db.session.commit()
    flash('🗑️ Candidature supprimée')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
