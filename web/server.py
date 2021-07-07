from flask import Flask , flash, request, redirect, url_for,send_file, send_from_directory, safe_join, abort

from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app)



@cross_origin()
@app.route('/test', methods=['GET'])
def home():
    return "this is our first appi "



if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True)