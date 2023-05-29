from flask import Flask,jsonify, request
import os
import requests

app = Flask(__name__)

@app.route("/calculate", methods=['POST'])
def calculate():
    print("works!",flush=True)
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
    current_dir = os.getcwd()
    print("container2", current_dir)

    file_path= current_dir+ '/files/'+file
    try: 
        if not os.path.exists(file_path):
            raise FileNotFoundError
        container2 = "http://container2:7000/sum"
        response= requests.post(container2, json=data)
        return jsonify(response.json())
        
    except FileNotFoundError:
        print("returning from C1")
        return jsonify(
            {
                "file": file,
                "error": "File not found."
            }
        )
    
