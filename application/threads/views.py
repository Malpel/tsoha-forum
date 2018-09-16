from flask import render_template, request, redirect, url_for
from application import app, db
from application.threads.models import Thread, Comment
from application.threads.forms import ThreadForm, CommentForm


@app.route("/threads/")
def get_threads():
    return render_template("threads/threads.html", threads = Thread.query.all())

@app.route("/threads/new", methods=["GET", "POST"])
def new_thread():
    form = ThreadForm(request.form)
    if request.method == "POST" and form.validate():
        t = Thread(form.title.data)
        c = Comment(form.text.data)
        db.session().add(t)
        db.session().commit()
        c.thread_id = t.id
        db.session().add(c)
        db.session().commit()
        return redirect(url_for("read_thread", id=t.id))
    return render_template("threads/new.html", form=ThreadForm())

@app.route("/threads/<string:id>/", methods=["GET", "POST"])
def read_thread(id):
    form = CommentForm(request.form)
    thread = Thread.query.get(id)
    comments = db.session.query(Comment).filter_by(thread_id=id).all()
    if request.method == "POST" and form.validate():
        new_comment(id, form)
        return redirect(url_for("read_thread", id=id))
    return render_template("threads/thread.html", thread=thread, comments=comments, form=form)

@app.route("/threads/<string:id>/poista")
def delete_thread(id):
    db.session.query(Comment).filter(Comment.thread_id==id).delete()
    db.session.query(Thread).filter(Thread.id==id).delete()
    db.session.commit()
    return redirect(url_for("get_threads"))

def new_comment(id, form):
    c = Comment(form.text.data)
    c.thread_id = id
    db.session().add(c)
    db.session().commit()


@app.route("/edit/<string:id>/", methods=["GET", "POST"])
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
    