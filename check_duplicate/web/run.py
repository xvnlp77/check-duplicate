from flask import Flask, request, render_template

from check_duplicate.server.check_duplicate import compute_duplicate_rate_2

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def response_request():
    if request.method == 'POST':
        content_1 = request.form.get('content_1')
        content_2 = request.form.get('content_2')

        c1_rate, c2_rate = compute_duplicate_rate_2(content_1, content_2)
        rate = "基于第一篇文章的重合度：{}\n基于第二篇文章的重合度：{}".format(c1_rate, c2_rate)
        return render_template("result.html", content_1=content_1, content_2=content_2, rate=rate)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
