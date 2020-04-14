from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource, reqparse
from simplexml import dumps
import json

from estimator import estimator

app = Flask(__name__)
api = Api(app, default_mediatype=None)

@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp

def output_xml(data, code, headers=None):
    """Make a Flask response with a XML encoded body"""
    resp = make_response(dumps({'response': data}), code)
    resp.headers.extend(headers or {})

    return resp

@app.after_request
def after_request(response):
    app.logger.info('%s %s %s', request.method, request.url_rule, response.status_code)
    return response

class Covid19EstimatorApi(Resource):
    def __init__(self, representations=None):
        self.representations = representations
        super(Covid19EstimatorApi, self).__init__()
    
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        
        parser.add_argument('periodType', type=str, required=True, location='form')
        parser.add_argument('timeToElapse', type=int, required=True, location='form')
        parser.add_argument('reportedCases', type=int, required=True, location='form')
        parser.add_argument('population', type=int, required=True, location='form')
        parser.add_argument('totalHospitalBeds', type=int, required=True, location='form')
        
        args = parser.parse_args(strict=True)
        
        output = estimator(args) 

        return output

api.add_resource(Covid19EstimatorApi, '/api/v1/on-covid-19')
api.add_resource(Covid19EstimatorApi, '/api/v1/on-covid-19/json', 
                                resource_class_kwargs={'representations': {'application/json': output_json}},
                                endpoint='covid19_estimator_api_json'
                            )
api.add_resource(Covid19EstimatorApi, '/api/v1/on-covid-19/xml', 
                                resource_class_kwargs={'representations': {'application/xml': output_xml}},
                                endpoint='covid19_estimator_api_xml'
                            )

app.run(debug=True)
