from flask import Flask, request, jsonify
from flask_cors import CORS
from gpx_pipeline import analyze_gpx_stream

app = Flask(__name__)
CORS(app)


@app.route('/api/health', methods=['GET'])
def health():
    """
    Simple health-check endpoint.
    """
    return jsonify({'status': 'healthy'}), 200


@app.route('/api/process-gpx', methods=['POST'])
def process_gpx():
    """
    Accepts a multipart/form-data upload with the field 'file' containing a GPX.
    Parses, analyzes, and returns a JSON of trail stats.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    gpx_file = request.files['file']
    try:
        # Delegate to the shared pipeline function:
        stats = analyze_gpx_stream(gpx_file.stream)
        return jsonify(stats), 200
    except Exception as e:
        # Return any parsing or analysis error as a 400 response
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    # Starts Flask in debug mode on port 5000
    app.run(debug=True, port=5000)
