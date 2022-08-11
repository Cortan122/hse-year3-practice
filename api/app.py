from flask import Flask, jsonify
from werkzeug.routing import BaseConverter

app = Flask(
    __name__,
    static_url_path='',
    static_folder='../dist'
)

class NoExtentionConverter(BaseConverter):
    regex = r'(?:[a-zA-Z0-9]+)'

app.url_map.converters['ext'] = NoExtentionConverter

api_counter = 0

@app.route("/api/counter")
def ping():
    global api_counter
    api_counter += 1
    return jsonify(api_counter)

@app.route('/', defaults={'path': ''})
@app.route('/<ext:path>')
def index(path):
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run()
