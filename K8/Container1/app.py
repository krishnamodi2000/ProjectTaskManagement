from flask import Flask, jsonify, request
import os
import csv
import requests

app = Flask(__name__)

@app.route("/store-file", methods=['POST'])
def store_file():
    data = request.get_json()

    # If the file name is not provided, an error message "Invalid JSON input." is returned
    if "file" not in data or data["file"] is None:
        return jsonify({
            "file": None,
            "error": "Invalid JSON input."
        })

    file = data["file"]

    file_path = '/Krishna_PV_dir/' + file
    try:

        file_data = data["data"]

        # Save the file data to the persistent storage
        with open(file_path, 'w') as f:
            f.write(file_data)

        return jsonify({
            "file": file,
            "message": "Success."
        })

    #if there is an error in storing the file
    except Exception as e:
        print("returning from C1")
        return jsonify({
            "file": file,
            "error": "Error while storing the file to the storage."
        })


@app.route("/calculate", methods=['POST'])
def calculate():
    data = request.get_json()

    # If the file name is not provided, an error message "Invalid JSON input." is returned
    if "file" not in data or data["file"] is None:
        return jsonify({
            "file": None,
            "error": "Invalid JSON input."
        })

    file = data["file"]

    file_path = '/Krishna_PV_dir/' + file
    try:
        #if the file does not exists in the /Krishna_PV_dir/
        if not os.path.exists(file_path):
            raise FileNotFoundError
        
        with open(file_path,'r') as f:
            dialect = csv.Sniffer().sniff(f.read(1024))
            f.seek(0)
            if dialect.delimiter != ',':
                return jsonify({
                    "file": file,
                    "error": "Input file not in CSV format."
                })  #if the file does not have the delimeter as ,/

            filereader = csv.reader(f, dialect)
            header = next(filereader)
            if header != ['product', 'amount ']:
                return jsonify({
                    "file": file,
                    "error": "Input file not in CSV format."
                })  #if the file does not have product and amount as their heading

            for row in filereader:
                if len(row) != 2:
                    return jsonify({
                        "file": file,
                        "error": "Input file not in CSV format." 
                    }) #if the file does not have exactly two values
            
    except FileNotFoundError:
        return jsonify({
            "file": file,
            "error": "File not found."
        })
    
   
            
    container2 = "http://container2-service:5001/sum"
    response = requests.post(container2, json=data)
    return jsonify(response.json())
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
