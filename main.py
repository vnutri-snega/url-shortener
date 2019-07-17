from flask import Flask, request, render_template, redirect
from urllib.parse import urlparse
import encode
import database

host = 'http://localhost:5000/'
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form.get('url')
        if urlparse(original_url).scheme == '':
            return render_template("short_url.html", short_url='Wrong url!')
        short_url = encode.encode_url(original_url)
        if database.update_url_count(original_url):
            return render_template("short_url.html", short_url=host + database.get_short_url(original_url))
        period = request.form.get('period')
        database.save_to_bd(original_url, short_url, period)
        return render_template("short_url.html", short_url=host + short_url)
    return render_template("url.html")


@app.route('/<short_url>')
def redirect_short_url(short_url):
    redirect_url = database.get_original_url(short_url)
    return redirect(redirect_url)


if __name__ == "__main__":
    database.create_db()
    database.check_dates()
    database.update_local_storage()
    app.run()
