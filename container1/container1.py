from flask import Flask,jsonify, request
app = Flask(__name__)

@app.route("/calculate", method=['POST'])
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
    try: 
        open(file)
    except FileNotFoundError:
        return jsonify(
            {
                "file": file,
                "error": "File not found."
            }
        )
    
    #Container 1 sends input to Container 2
    product=data["product"]
    container2="http://localhost:6000/sum"

    response = request.post(container2,json={
        "file": file,
        "product": product
    })
    return response.json()

if __name__ == 'main':
    app.run(host='0.0.0.0', port=6000 )