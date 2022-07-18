# from flask import Flask, jsonify, request
# from bank_db_utils import (name of function returning json from mysql)
#
# app = Flask(__name__)
#
# Example
# @app.route('/students/<student_id>')
# def get_student_info(student_id):
#     res = db_get_student_info(student_id)
#     return jsonify(res)
#
# if __name__ == '__main__':
#     app.run(debug=True, port=5001)