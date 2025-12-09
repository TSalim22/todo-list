import os
from datetime import date
from flask import render_template, request, redirect, session, flash, abort
from auth import db, make_app, login_required


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    priority = db.Column(db.String(10), nullable=False, default='Normal')
    due = db.Column(db.Date)
    done = db.Column(db.Boolean, nullable=False, default=False)


def read_form():
    title = request.form.get('title', '').strip()
    priority = request.form.get('priority', 'Normal')
    due_text = request.form.get('due', '')
    if not title or len(title) > 120 or priority not in ('Low', 'Normal', 'High'):
        raise ValueError('Enter a title up to 120 characters and a valid priority.')
    return title, priority, date.fromisoformat(due_text) if due_text else None


def create_app(config=None):
    app = make_app('To-Do List', 'Plan your tasks, one day at a time.', config)

    def owned(identifier):
        task = db.session.get(Task, identifier)
        if not task or task.user_id != session['user_id']:
            abort(404)
        return task

    @app.get('/')
    @login_required
    def index():
        mode = request.args.get('filter', 'all')
        query = db.select(Task).where(Task.user_id == session['user_id'])
        if mode in ('pending', 'done'):
            query = query.where(Task.done == (mode == 'done'))
        tasks = db.session.scalars(query.order_by(Task.done, Task.id.desc())).all()
        return render_template('index.html', title='Your tasks', tasks=tasks, mode=mode, today=date.today())

    @app.post('/tasks')
    @login_required
    def add():
        try:
            title, priority, due = read_form()
        except ValueError as error:
            flash(str(error))
            return redirect('/')
        db.session.add(Task(user_id=session['user_id'], title=title, priority=priority, due=due))
        db.session.commit()
        return redirect('/')

    @app.route('/tasks/<int:identifier>/edit', methods=['GET', 'POST'])
    @login_required
    def edit(identifier):
        task = owned(identifier)
        if request.method == 'POST':
            try:
                task.title, task.priority, task.due = read_form()
            except ValueError as error:
                flash(str(error))
                return render_template('edit.html', title='Edit task', task=task), 400
            db.session.commit()
            return redirect('/')
        return render_template('edit.html', title='Edit task', task=task)

    @app.post('/tasks/<int:identifier>/toggle')
    @login_required
    def toggle(identifier):
        task = owned(identifier)
        task.done = not task.done
        db.session.commit()
        return redirect('/')

    @app.post('/tasks/<int:identifier>/delete')
    @login_required
    def delete(identifier):
        db.session.delete(owned(identifier))
        db.session.commit()
        return redirect('/')

    with app.app_context():
        db.create_all()
    return app


if __name__ == '__main__':
    create_app().run(host=os.getenv('HOST','127.0.0.1'),port=5000)
