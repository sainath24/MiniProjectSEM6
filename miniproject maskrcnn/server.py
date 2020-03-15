from flask import Flask,request
app = Flask(__name__)


@app.route('/')
def home():
    return 'HOME PAGE'

@app.route('/uploadmeal', methods=["GET","POST"])
def uploadMeal():
    content = request.get_json()
    print(content)
    picnp = np.fromstring(base64.b64decode(content['pic']), dtype=np.uint8)
    img = cv2.imdecode(picnp, 1)
    return 'Uploading Meal'

if __name__ == '__main__':
    app.run(host = '192.168.1.19', port = '4444')
