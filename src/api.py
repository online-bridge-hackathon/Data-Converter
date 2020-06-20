from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api
from pbn import parse_pbn_string


app = Flask(__name__)
CORS(app)
api = Api(app)


class Convert(Resource):
    """Add pbn linter. New endpoint or library? PBN has import and export formats."""
    def get(self):
        return {'hello': 'world'}

    def post(self, output):
        """Reads a file, verifies what type it is, and either converts it or rejects it"""
        if 'file' not in request.files:
            return {'status': 'no file'}
        file_obj = request.files['file'] 
        deals = file_obj.read().decode('utf-8')
        deals_json = parse_pbn_string(deals)

        return deals_json

api.add_resource(Convert, '/api/boards/<output>')

if __name__ == "__main__":
    app.run(debug=True)
    # curl -F "file=@/full/path/to/pbn" http://localhost:5000/api/boards/test


