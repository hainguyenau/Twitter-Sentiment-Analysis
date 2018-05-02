from flask import Flask, request, render_template, make_response
import pickle
from GetTweets import get_tweets, get_text
import random



app = Flask(__name__)

# load pickles
with open('data/clf.pkl', 'rb') as f:
    clf = pickle.load(f)
with open('data/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)


# home page
@app.route('/')
def search():
    return render_template('search.html')


# predict
@app.route('/predict', methods=['POST'])
def predict():
    topic = request.form['user_input']
    topic = str(topic)
    tweets = get_tweets(topic, 5)

    # classify texts
    tweet_texts = get_text(tweets)
    dates = [tweet.created_at for tweet in tweets]
    users = [tweet.user.screen_name for tweet in tweets]
    content = vectorizer.transform(tweet_texts)
    labels = clf.predict(content)
    probas = clf.predict_proba(content)
    results = zip(tweet_texts, probas, dates, users, labels)

    return render_template('predict.html', topic=topic, results=results)


# Matplotlib: use session to pass variables from above function
@app.route("/plot.png")
def plot():
    import io
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]

    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
