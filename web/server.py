from flask import Flask , flash, request, redirect, url_for,send_file, send_from_directory, safe_join, abort,jsonify

from flask_cors import CORS, cross_origin

from bsMethods import scrap_emploi,scrap_announces_url_into_array

app = Flask(__name__)

cors = CORS(app)



@cross_origin()
@app.route('/test', methods=['GET'])
def home():
    return "this is our first appi "

@cross_origin()
@app.route('/scrap/oneJob/', methods=['GET'])
def scrap_one_page():
    url = request.args['url']
    return scrap_emploi(url)

@cross_origin()
@app.route('/scrap/multiplePages', methods=['GET'])
def scrap_pages():
    number_of_pages = int(request.args['number'])
    return jsonify(scrap_announces_url_into_array(number_of_pages))

@cross_origin()
@app.route('/scrap/multipleJobs/', methods=['GET'])
def scrap_annonces():
    number_of_jobs = int(request.args['number'])
    print(number_of_jobs)
    return jsonify( scrap_announces_url_into_array(number_of_jobs//25+1)[:number_of_jobs])





if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True)