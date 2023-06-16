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
    current_dir = os.getcwd()

    file_path = current_dir + '/files/' + file
    try:

        file_data = data["data"]

        # Save the file data to the persistent storage
        with open(file_path, 'w') as f:
            f.write(file_data)

        return jsonify({
            "file": file,
            "message": "Success."
        })

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
    current_dir = os.getcwd()

    file_path = current_dir + '/files/' + file
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError
        
        with open(file_path,'r') as f:
            dialect = csv.Sniffer().sniff(f.read(1024))
            f.seek(0)
            if dialect.delimiter!=',':
                raise csv.Error

            filereader = csv.reader(f,dialect)
            header = next(filereader)
            if header == ['product', 'amount ']: #changed a condn here to make sure the code is running right. Confirm with others if it has to be done
                for row in filereader:
                    if len(row) == 2:
                        continue
                    else:
                        raise csv.Error
            else:
                raise csv.Error
            
        container2 = "http://localhost:5001/sum"
        print("reached line 82", flush=True)
        response = requests.post(container2, json=data)
        print("reached line 84", flush=True)
        return jsonify(response.json())
        

    except FileNotFoundError:
        return jsonify({
            "file": file,
            "error": "File not found."
        })
    
    except csv.Error:
        return jsonify(
            {
                "file": file,
                "error": "Input file not in CSV format."
            }
        )

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
