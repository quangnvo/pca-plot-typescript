import random
import string

from flask import Blueprint, jsonify

bp = Blueprint('generateSampleData', __name__)


@bp.route('/api/generate_data', methods=['GET'])
#########################
# Generate random data
#########################
def generate_data():
    data = []
    # Generate 300 random samples
    for _ in range(300):
        sample = {
            # Generate a random 10-character string of uppercase letters and digits (to make it as a name)
            'Gene': ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),

            # Generate random values for conditions
            # f"" is a string formatting method that is used to insert the value into a string
            'condition 1': f"{random.uniform(-2, 2):.2f}",
            'condition 2': f"{random.uniform(3, 7):.2f}",
            'condition 3': f"{random.uniform(0, 1):.2f}",
            'condition 4': f"{random.uniform(0, 1):.2f}",
            'condition 5': f"{random.uniform(4, 10):.2f}"
        }
        data.append(sample)
    return jsonify(data)
