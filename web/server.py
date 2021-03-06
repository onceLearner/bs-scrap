import os

from flask import Flask , request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from flask_cors import CORS, cross_origin
import time
from emploi.bsMethods import scrap_page_emploi,scrap_announces_url_into_array_from_Emploi
from rekrute.bsMethods import  scrap_page_rekrute,scrap_announces_url_into_array_from_Rekrute

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)



# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
emploi_ref = db.collection('emploi')


@app.route('/test', methods=['GET'])
def home():
    return "this is our first appi "


@cross_origin()
@app.route('/test1', methods=['GET'])
def home1():
    return "this is our first appi "



""""
-----------------
EMPLOI.ma

---------------
"""





@cross_origin()
@app.route('/emploi/scrap/oneJob/', methods=['GET'])
def scrap_one_page_emploi():
    url = request.args['url']
    return scrap_page_emploi(url)

@cross_origin()
@app.route('/emploi/scrap/multiplePages', methods=['GET'])
def scrap_pages_emploi():
    number_of_pages = int(request.args['number'])
    return jsonify(scrap_announces_url_into_array_from_Emploi(number_of_pages))

@cross_origin()
@app.route('/emploi/scrap/multipleJobs/', methods=['GET'])
def scrap_annonces_emploi():
    number_of_jobs = int(request.args['number'])
    print(number_of_jobs)
    return jsonify(scrap_announces_url_into_array_from_Emploi(number_of_jobs//25+1)[:number_of_jobs])






""""
-----------------
REKRUTE.com

---------------
"""


@cross_origin()
@app.route('/rekrute/scrap/oneJob/', methods=['GET'])
def scrap_one_page_rekrute():
    url = request.args['url']
    return scrap_page_rekrute(url)

@cross_origin()
@app.route('/rekrute/scrap/multiplePages', methods=['GET'])
def scrap_pages_rekrute():
    number_of_pages = int(request.args['number'])
    return jsonify(scrap_announces_url_into_array_from_Rekrute(number_of_pages))

@cross_origin()
@app.route('/rekrute/scrap/multipleJobs/', methods=['GET'])
def scrap_annonces_rekrute():
    number_of_jobs = int(request.args['number'])
    print(number_of_jobs)
    return jsonify(scrap_announces_url_into_array_from_Rekrute(number_of_jobs//25+1)[:number_of_jobs])





















#post new job
@cross_origin()
@app.route("/emploi/jobs",methods=["POST"])
def save_one_job():
    array_of_data = request.get_json()
    print(array_of_data)
    try:
        id = "emploi" +str(int(time.time()))
        print(id)
        emploi_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"




#get one or all jobs
@cross_origin()
@app.route('/emploi/jobs', methods=['GET'])
def read_jobs():
    """
        read() : Fetches documents from Firestore collection as JSON.
        todo : Return document that matches query ID.
        all_todos : Return all documents.
    """
    try:
        # Check if ID was passed to URL query
        job_id = request.args.get('id')
        if job_id:
            todo = emploi_ref.document(job_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_jobs = [doc.to_dict() for doc in emploi_ref.stream()]
            return jsonify(all_jobs), 200
    except Exception as e:
        return f"An Error Occured: {e}"





#delete a job by id
@cross_origin()
@app.route('/emploi/jobs', methods=['DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection.
    """
    try:
        # Check for ID in URL query
        job_id = request.args.get('id')
        emploi_ref.document(job_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"





port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True,port=port)