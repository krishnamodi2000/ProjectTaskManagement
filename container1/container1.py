from flask import Flask,jsonify, request
import os
import requests

app = Flask(__name__)

@app.route("/calculate", methods=['POST'])
def calculate():
    data= request.get_json()

    #if the file name is not provided an error message "Invalid JSON input." is returned
    if "file" not in data or data["file"] is None:
        return jsonify(
            {
                "file": None,
                "error": "Invalid JSON input."
            }
        )
    
    #if filename is provided but not found mounted on disk voulme an error message is "File not found." is returned
    file=data["file"]
    file_path = os.path.join(os.path.dirname(__file__), file)
    try: 
        if not os.path.exists(file_path):
            raise FileNotFoundError
        container2 = "http://localhost:7000/sum"
        response= requests.post(container2, json=data)
        return jsonify(response.json())
        
    except FileNotFoundError:
        return jsonify(
            {
                "file": file,
                "error": "File not found."
            }
        )
    
if __name__ == '__main__':
    app.run(host="localhost", port=6000)