from auth import db
from app import Task

def test_task_crud_and_filtering(logged_in,app):
    client = logged_in
    client.post('/tasks',data={'title':'Revise SQL','priority':'High','due':'2026-10-20'})
    assert b'Revise SQL' in client.get('/').data
    with app.app_context(): identifier = db.session.scalar(db.select(Task.id))
    client.post(f'/tasks/{identifier}/edit',data={'title':'Revise joins','priority':'Normal','due':''})
    client.post(f'/tasks/{identifier}/toggle')
    assert b'Revise joins' not in client.get('/?filter=pending').data
    assert b'Revise joins' in client.get('/?filter=done').data
    client.post(f'/tasks/{identifier}/delete')
    assert b'Revise joins' not in client.get('/').data

def test_other_accounts_cannot_read_or_modify(logged_in,app):
    logged_in.post('/tasks',data={'title':'Private task','priority':'Normal'})
    with app.app_context(): identifier = db.session.scalar(db.select(Task.id))
    second = app.test_client()
    second.post('/register',data={'username':'another','password':'another-test-pass'})
    assert b'Private task' not in second.get('/').data
    assert second.get(f'/tasks/{identifier}/edit').status_code==404
    assert second.post(f'/tasks/{identifier}/delete').status_code==404
    assert second.post(f'/tasks/{identifier}/toggle').status_code==404

def test_invalid_date_and_html_are_handled(logged_in):
    logged_in.post('/tasks',data={'title':'Bad date','due':'nonsense','priority':'Low'})
    assert b'Bad date' not in logged_in.get('/').data
    logged_in.post('/tasks',data={'title':'<script>alert(1)</script>','priority':'Normal'})
    assert b'&lt;script&gt;' in logged_in.get('/').data
