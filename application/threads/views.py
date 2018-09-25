from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from application import app, db
from application.threads.models import Thread, Comment
from application.threads.forms import ThreadForm, CommentForm
from sqlalchemy.orm.attributes import  set_committed_value
from collections import defaultdict


@app.route("/threads/")
def get_threads():
    return render_template("threads/threads.html", threads = Thread.query.all())


@app.route("/threads/new", methods=["GET", "POST"])
@login_required
def new_thread():
    form = ThreadForm(request.form)
    if request.method == "POST" and form.validate():
        t = Thread(form.title.data)
        t.user = current_user.id
        c = Comment(form.text.data)
        db.session().add(t)
        db.session().commit()
        c.thread_id = t.id
        c.user = current_user.id
        db.session().add(c)
        db.session().commit()
        return redirect(url_for("read_thread", id=t.id))
    return render_template("threads/new.html", form=ThreadForm())


@app.route("/threads/<string:id>/", methods=["GET", "POST"])
def read_thread(id):
    form = CommentForm(request.form)
    thread = Thread.query.get(id)
    '''
    WITH RECURSIVE cte AS ( 
    SELECT comment.id, commen.parent_id 
    FROM comment 
    WHERE parent_id IS NULL UNION ALL 
    SELECT comment.id, comment.parent_id FROM comment 
    INNER JOIN cte ON comment.parent_id = cte.id 
    WHERE comment.parent_id is NOT NULL ORDER BY parent_id DESC, id) 
    SELECT * FROM cte GROUP_BY id, parent_id;
    '''
    cte = db.session.query(Comment).filter_by(thread_id=id)\
    .filter(Comment.parent_id == None)\
    .cte(recursive=True)
    parent = db.aliased(cte)
    child = db.aliased(Comment)
 
    kwery = parent.union_all(db.session.query(child)\
    .join(parent, child.parent_id == parent.c.id))
    
    # ei lähelläkään yllä olevan sql-kyselyn tulosta, koska cte ei voi order_by eikä cte voi queryä
    comments = db.session.query(kwery).order_by(kwery.c.id).all()

    if request.method == "POST" and form.validate():
        new_comment(id, form)
        return redirect(url_for("read_thread", id=id))
    return render_template("threads/thread.html", thread=thread, comments=comments, form=form)


@app.route("/threads/<string:id>/poista")
@login_required
def delete_thread(id):
    db.session.query(Comment).filter(Comment.thread_id==id).delete()
    db.session.query(Thread).filter(Thread.id==id).delete()
    db.session.commit()
    return redirect(url_for("get_threads"))

    
@login_required
def new_comment(id, form):
    c = Comment(form.text.data)
    c.thread_id = id
    c.user = current_user.id
    db.session().add(c)
    db.session().commit()


@app.route("/edit/<string:id>/", methods=["GET", "POST"])
@login_required
def edit_comment(id):
    form = CommentForm(request.form)
    comment = db.session.query(Comment).filter(Comment.id==id).first()
    if request.method == "POST" and form.validate():
        text = form.text.data
        db.session.query(Comment).\
        filter(Comment.id==id).\
        update({Comment.text: text}, synchronize_session=False)    
        db.session.commit()
        return redirect(url_for("read_thread", id=comment.thread_id))
    form.text.data = comment.text
    return render_template("threads/edit.html", form=form, comment=comment)


@app.route("/threads/<string:thread_id>/<string:comment_id>/reply", methods=["GET", "POST"])
@login_required
def reply(thread_id, comment_id):
    form = CommentForm(request.form)
    if request.method == "POST" and form.validate():
        c = Comment(form.text.data)
        c.thread_id = thread_id
        c.parent_id = comment_id
        c.user = current_user.id
        db.session().add(c)
        db.session().commit()
        return redirect(url_for("read_thread", id=thread_id))
    return render_template("threads/reply.html", form=form)
   

    