from flask import Flask, jsonify, request
import csv
import os

app = Flask(__name__)

@app.route("/sum", methods=['POST'])
def sum():
    data=request.get_json()
    file=data["file"]
    product=data["product"]
    current_dir = os.getcwd()
    print("container2", current_dir)

    file_path= current_dir+'/files/'+file
    
    with open(file_path,'r') as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        filereader = csv.reader(f,dialect)
        header = next(filereader)
        if header == ['product', 'amount']:
            total = 0
            for row in filereader:
                if len(row) == 2:
                    row_product = row[0].strip()
                    row_amount = row[1].strip()
                    if row_product == product:
                        total += int(row_amount)

        return jsonify(
            {
                "file": file,
                "sum": total
            }
            )



if __name__ == "__main__":
    app.run(host='localhost', port=5001)