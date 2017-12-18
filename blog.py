#!usr/bin/env/python
# -*- coding: utf-8 -*-
"""IS211_FinalProject-Blogging"""

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import datetime

app = Flask(__name__)

blogs = [{"title":"Title2"}]
users = {"user":"pass"} # using a user:password dict
# title, data, author, content

logged_in = False;


@app.route('/')
def displaylist():
    return render_template('list.html', blogs=blogs)


@app.route('/dashboard')
def display():
    if(logged_in):
        return render_template('dashboard.html', blogs=blogs)
    else:
        return redirect("/login")


@app.route('/add')
def add():
    if (logged_in):
        return render_template('add.html', blogs=blogs)
    else:
        return redirect("/login")


@app.route('/edit', methods=['GET'])
def edit():
    if (logged_in):
        index = int(request.args["index"])
        return render_template('edit.html', blogpost=blogs[index-1], index=index)
    else:
        return redirect("/login")


@app.route('/submit', methods=['POST'])
def submit():
    if (not logged_in):
        return redirect("/")

    global status
    print(request.form)
    title = request.form['title']
    # user = request.form['email']
    author = request.form['author']
    date = datetime.datetime.now()
    content = request.form['content']
    index = request.form.get(
        'index'
    )  # get the index if it is available(only in the case of edit requests)
    print(index)
    post = {"title": title, "date": date, "author": author, "content": content}
    print(post)

    if title == "":
        status = "Error: A title is required."
        return redirect("/")
    elif author == "":
        status = "Error: Empty author"
        return redirect("/")
    elif date == "":
        status = "Error: Invalid Date."
        return redirect("/")
    elif content == "":
        status = "Error: Empty content!"
        return redirect("/")
    else:
        if(index is None):
            blogs.append(post)
        else:
            blogs[int(index)-1] = post  # replacing the post if we had a defined index

    return redirect("/dashboard")


@app.route('/login', methods=['GET'])
def loginview():
    # msg=request.args['message']
    # print("message",msg)
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login():
    global logged_in
    print("inside post", request.form)
    username = str(request.form['username'])
    passw = str(request.form['password'])
    if(users[username]==passw):
        logged_in = True
        return redirect("/dashboard")
    else:
        return redirect("/login", message="Login Error")


@app.route('/clear', methods=['POST'])
def clear():

    del blogs[:]
    return redirect("/")


@app.route('/delete', methods=['POST'])
def delete():
    delete_index = int(request.form['index'])
    del blogs[delete_index-1]
    return redirect("/dashboard")


if __name__ == "__main__":
    app.run()
