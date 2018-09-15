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
        return redirect(url_for("get_threads"))
    return render_template("threads/new.html", form=ThreadForm())

@app.route("/threads/<string:id>/", methods=["GET", "POST"])
def read_thread(id):
    thread = Thread.query.get(id)
    comment = db.session.query(Comment).filter_by(thread_id=id).first()
    return render_template("threads/thread.html", thread=thread, comment=comment)