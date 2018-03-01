#!/usr/bin/env python3

from flask import Flask, request, redirect, url_for

from logdb import article, g_authors, g_log

app = Flask(__name__)

# HTML template for the forum page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>LOG ANALYSIS</title>
    <style>
      h1, form { text-align: center; }
      textarea { width: 400px; height: 100px; }
      div.post { border: 1px solid #999;
                 padding: 10px 10px;
                 margin: 10px 20%%; }
      hr.postbound { width: 50%%; }
      em.date { color: #999 }
    </style>
  </head>
  <body>
    <h1>DB Forum</h1>
    <form method=post>
      <div><textarea id="content" name="content"></textarea></div>
      <div><button id="go" type="submit">Post message</button></div>
    </form>
    <!-- post content will go here -->
<ol>
%s
</ol>

%s
<br><br>
%s

  </body>
</html>
'''
ARTICLES = '''\
    <li>%s - %s views</li>
'''
AUTHORS = '''\
    <li>%s - %s views</li>
'''
LOG = '''\
    <li>%s - %s errors</li>
'''


@app.route('/', methods=['GET'])
def main():
    '''Main page of the forum.'''
    articles = "".join(ARTICLES % (title, num) for title, num in article())
    authors = "".join(AUTHORS % (name, num) for name, num in g_authors())
    log = "".join(LOG % (date, result) for date, result in g_log())
    html = HTML_WRAP % (articles, authors, log)
    return html


@app.route('/', methods=['POST'])
def post():
    '''New post submission.'''
    message = request.form['content']
    add_post(message)
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
