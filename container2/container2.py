from flask import Flask, jsonify, request
import csv

app = Flask(__name__)

@app.route("/sum",methods=['POST'])
def sum():
    data=request.get_json()
    file=data["file"]
    product=data["product"]
    try:
        with open(file,'r') as f:
            dialect = csv.Sniffer().sniff(f.read(1024))
            f.seek(0)
            if dialect.delimiter!=',':
                raise csv.Error

            filereader = csv.reader(f,dialect)
            total=0
            for row in filereader:
                if len(row) == 2:
                    row_product = row[0].strip()
                    row_amount = row[1].strip()
                    if row_product == product:
                        total += int(row_amount)
                else:
                    raise csv.Error
    # If the filename provided via the input JSON is found in the mounted disk volume,
    # the calculation is performed
            return jsonify(
                {
                    "file": file,
                    "sum": total
                }
            )
    # If a filename is provided, but the file contents cannot be parsed due to not following the CSV
    # format described an error message is "Input file not in CSV format." is returned
    except csv.Error:
        return jsonify(
            {
                "file": file,
                "error": "Input file not in CSV format."
            }
        )
 
   

if __name__ == '__main__':
    app.run(host="localhost", port=7000)
