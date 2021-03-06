'''
   Routing for the data
'''

from flask import Flask, request, redirect, url_for, render_template, flash, json
import json

from dbcontroller import JoinGraph
from conversion import Convert

with open('./config.json', 'rb') as f:
    config = json.load(f)

app = Flask(__name__)
app.config.update(config)

@app.route('/data', methods=['POST'])
def get_single_data():
   
    graph = request.get_json()
    data = JoinGraph(app.config['SPARQL']).get_original(graph['data'])
    return response_template(data, 200)

@app.route('/search/')
def search_data():
    search = request.args.get('term')
    data = JoinGraph(app.config['SPARQL']).search_data(search)
    return response_template(data, 200)

@app.route('/search/<dtype>')
def search_data_type(dtype):
    search = request.args.get('term')
    #dtype = request.args.get('type')
    if dtype is not None:
        data = JoinGraph(app.config['SPARQL']).search_data_type(search, dtype)
    else:
        data = JoinGraph(app.config['SPARQL']).search_data(search)
    return response_template(data, 200)

@app.route('/')
def get_index():
    workset = request.args.get('wsid')
    user = request.args.get('user')
    dtype = request.args.get('type')
    if workset is None:
        return render_template('search.html')
    else:
        return render_template('test.html', workset=workset, user=user, dtype=dtype)

@app.route('/predicates', methods=['POST'])
def sparql():
    '''
       Searches the predicates associated with an object
    '''
    graph = request.get_json()
    data = JoinGraph(app.config['SPARQL']).search_predicates(graph['entity'])
    return response_template(data, 200)

@app.route('/predicates/workset', methods=['POST'])
def search_pred_obj():
    '''
       Search (predicate, object) associated with a workset
    '''
    graph = request.get_json()
    data = JoinGraph(app.config['SPARQL']).search_predicates_object(graph['pred'], graph['ws'])
    return response_template(data, 200)

@app.route('/predicates/similarity', methods=['POST'])
@app.route('/predicates/similarity/workset', methods=['POST'])
def similarity_works():
    '''
       Route to return similarity counts for predicates
    '''
    graph = request.get_json()
    data = None
    if "flag" in graph:
        data = JoinGraph(app.config['SPARQL']).search_similarities(graph['dataObj'], ws=graph['flag'])
    else:
        data = JoinGraph(app.config['SPARQL']).search_similarities(graph['dataObj'])
    return response_template(data, 200)

@app.route('/subject', methods=['GET', 'POST'])
def get_linked_subjects():
    graph = request.get_json()
    data = JoinGraph(app.config['SPARQL']).search_subject(graph['subject'])
    return response_template(data, 200)

@app.route('/cluster', methods=['POST'])
def get_linked_graphs():
    graph = request.get_json()
    data = JoinGraph(app.config['SPARQL']).clustering(graph['dataObj'])
    return response_template(data, 200)

@app.route('/worksets', methods=['POST'])
def get_workset():
    _id = request.get_json();
    ws = JoinGraph(app.config['SPARQL']).worksets()
    return response_template(ws, 200)

@app.route('/worksets/item', methods=['POST'])
def get_item():
    _id = request.get_json();
    ws = JoinGraph(app.config['SPARQL']).id_details(_id['id'])
    return response_template(ws, 200)

@app.route('/worksets/items', methods=['POST'])
def get_workset_items():
    ws_id = request.get_json()
    ws = JoinGraph(app.config['SPARQL']).worksets_by_id(ws_id['id'])
    return response_template(ws, 200)

@app.route('/worksets/save', methods=['PUT'])
def save_workset():
    '''
       Method to allow for the writing of the JSON data to files
       Returns a dummy method
    '''
    ws_id = request.get_json()
    uid = Convert().dump_to_disk(app.config['fs'], ws_id['dataObj'], ws_id['user'])
    return response_template(uid, 200)
    

@app.route('/weight', methods=['POST'])
def store_weight():
    '''
       Route to allow a weighting from the client to be stored. 
       Only a dummy for the original prototype. 
    '''
    weight = request.get_json()
    return response_template("stored", 200)
    

def response_template(data, resp_status):
    '''
       Helper function for the JSON response template
    '''
    response = app.response_class(
        response=data,
        status=resp_status,
        mimetype='application/json'
    )
    return response
