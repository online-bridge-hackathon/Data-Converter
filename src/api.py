from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api

from dds import DDS

app = Flask(__name__)
CORS(app)
api = Api(app)


class Convert(Resource):
    """Add pbn linter. New endpoint or library? PBN has import and export formats."""
    def get(self):
        return {'hello': 'world'}

    def post(self):
        """Reads a file, verifies what type it is, and either converts it or rejects it"""
        return


api.add_resource(DDSTable, '/api/convert/')

if __name__ == "__main__":
    app.run(debug=True)


