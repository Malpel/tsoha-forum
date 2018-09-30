from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_manager, login_required
from application import app, db
from application.threads.models import Thread, Comment, Category
from application.threads.forms import ThreadForm, CommentForm
from collections import defaultdict


@app.route("/categories")
def list_categories():
    return render_template("threads/categories.html", categories=Category.query.all())

@app.route("/<string:id>/threads/")
def get_threads(id):
    category = Category.query.filter_by(id=id).first()
    threads = Thread.query.filter_by(category=id).all()
    return render_template("threads/threads.html", category=category, threads=threads)


@app.route("/<string:id>/new/", methods=["GET", "POST"])
@login_required
def new_thread(id):
    form = ThreadForm(request.form)
    if request.method == "POST" and form.validate():
        t = Thread(form.title.data)
        t.user = current_user.id
        t.category = id
        c = Comment(form.text.data)
        db.session().add(t)
        db.session().commit()
        c.thread_id = t.id
        c.user = current_user.id
        db.session().add(c)
        db.session().commit()
        return redirect(url_for("read_thread", id=id, thread_id=t.id))
    return render_template("threads/new.html", form=ThreadForm())


@app.route("/<string:id>/threads/<string:thread_id>/", methods=["GET", "POST"])
def read_thread(id, thread_id):
    form = CommentForm(request.form)
    thread = Thread.query.get(thread_id)

    cte = db.session.query(Comment).filter_by(thread_id=thread_id)\
    .filter(Comment.parent_id == None)\
    .cte(recursive=True)
    parent = db.aliased(cte)
    child = db.aliased(Comment)
 
    kwery = parent.union_all(db.session.query(child)\
    .join(parent, child.parent_id == parent.c.id))
    
    comments = db.session.query(kwery).order_by(kwery.c.id).all()
    
    # TODO: laita threaded comments toimimaan jotenkin herokussa
    #Comment.comment_thread(thread_id)
    if request.method == "POST" and form.validate():
        new_comment(thread_id, form)
        return redirect(url_for("read_thread", id=id, thread_id=thread_id))
    return render_template("threads/thread.html", category=id, thread=thread, comments=comments, form=form)


#@app.route("/<string:id>/threads/<string:thread_id>/poista")
#@login_required
#def delete_thread(id, thread_id):
#    db.session.query(Comment).filter(Comment.thread_id==thread_id).delete()
#    db.session.query(Thread).filter(Thread.id==thread_id).delete()
#    db.session.commit()
#    return redirect(url_for("get_threads"))

    
@login_required
def new_comment(thread_id, form):
    c = Comment(form.text.data)
    c.thread_id = thread_id
    c.user = current_user.id
    db.session().add(c)
    db.session().commit()


@app.route("/<string:comment_id>/edit", methods=["GET", "POST"])
@login_required
def edit_comment(comment_id):
    
    form = CommentForm(request.form)
    comment = db.session.query(Comment).filter(Comment.id==comment_id).first()
    if request.method == "POST" and form.validate():
        text = form.text.data
        db.session.query(Comment).\
        filter(Comment.id==id).\
        update({Comment.text: text}, synchronize_session=False)    
        db.session.commit()
        return redirect(url_for("read_thread", id=id, thread_id=comment.thread_id))
    form.text.data = comment.text
    return render_template("threads/edit.html", form=form, comment=comment)


@app.route("/<string:thread_id>/<string:comment_id>/reply", methods=["GET", "POST"])
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
        return redirect(url_for("read_thread", id=id, thread_id=thread_id))
    return render_template("threads/reply.html", form=form)
   

    