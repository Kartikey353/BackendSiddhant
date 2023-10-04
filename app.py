from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from bson import ObjectId
import json
from pymongo.mongo_client import MongoClient 
import os


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
CORS(app) 
uri = "mongodb+srv://jainsiddhant214:FmTsBxus6uc7hjc7@cluster0.nepyf8e.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri) 
env_config = os.getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)


try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client['universities']
collection1 = db['university_data']
collection2 = db['scholarship_data']
collection3 = db['courses_data']


@app.route('/university', methods=['POST'])
def add_university():
    university_data = request.json
    university_name = university_data.get('university_name')

    existing_data = collection1.find_one({'university_name': university_name})
    if existing_data:
        return jsonify({'message': 'University already registered'}), 400

    collection1.insert_one(university_data)
    return jsonify({'message': 'University added successfully'}), 200


@app.route('/university/<university_name>', methods=['PUT'])
def update_university(university_name):
    updated_data = request.json

    existing_data = collection1.find_one({'university_name': university_name})
    if not existing_data:
        return jsonify({'message': 'University not found'}), 404

    collection1.update_one({'university_name': university_name}, {
                           '$set': updated_data})
    return jsonify({'message': 'University updated successfully'}), 200


@app.route('/university', methods=['GET'])
def get_all_universities():
    universities = list(collection1.find())
    return json.dumps(universities, default=str), 200


@app.route('/university/<university_name>', methods=['GET'])
def get_university(university_name):
    university = collection1.find_one({'university_name': university_name})
    if not university:
        return jsonify({'message': 'University not found'}), 404
    return json.dumps(university, default=str), 200


@app.route('/scholarship', methods=['POST'])
def add_scholarship():
    scholarship_data = request.json
    scholarship_name = scholarship_data.get('scholarship_name')

    existing_data = collection2.find_one(
        {'scholarship_name': scholarship_name})
    if existing_data:
        return jsonify({'message': 'Scholarship already registered'}), 400

    collection2.insert_one(scholarship_data)
    return jsonify({'message': 'Scholarship added successfully'}), 200


@app.route('/scholarship/<scholarship_name>', methods=['PUT'])
def update_scholarship(scholarship_name):
    updated_data = request.json

    existing_data = collection2.find_one(
        {'scholarship_name': scholarship_name})
    if not existing_data:
        return jsonify({'message': 'Scholarship not found to update'}), 404

    collection2.update_one({'scholarship_name': scholarship_name}, {
                           '$set': updated_data})
    return jsonify({'message': 'Scholarship updated successfully'}), 200


@app.route('/scholarship', methods=['GET'])
def get_all_scholarships():
    scholarships = list(collection2.find())
    return json.dumps(scholarships, default=str), 200


@app.route('/scholarship/<scholarship_name>', methods=['GET'])
def get_scholarship(scholarship_name):
    scholarship = collection2.find_one({'scholarship_name': scholarship_name})
    if not scholarship:
        return jsonify({'message': 'Scholarship not found'}), 404
    return json.dumps(scholarship, default=str), 200


@app.route('/courses', methods=['POST'])
def add_course():
    course_data = request.json
    course_name = course_data.get('course_name')

    existing_data = collection1.find_one({'course_name': course_name})
    if existing_data:
        return jsonify({'message': 'University already registered'}), 400

    collection3.insert_one(course_data)
    return jsonify({'message': 'University added successfully'}), 200


@app.route('/courses/<course_name>', methods=['PUT'])
def update_course_name(course_name):
    updated_data = request.json

    existing_data = collection3.find_one({'course_name': course_name})
    if not existing_data:
        return jsonify({'message': 'University not found'}), 404

    collection3.update_one({'course_name': course_name}, {
                           '$set': updated_data})
    return jsonify({'message': 'University updated successfully'}), 200


@app.route('/courses', methods=['GET'])
def get_all_courses():
    courses = list(collection3.find())
    return json.dumps(courses, default=str), 200


@app.route('/courses/<course_name>', methods=['GET'])
def get_course(course_name):
    coursename = collection2.find_one({'course_name': course_name})
    if not coursename:
        return jsonify({'message': 'course name not found'}), 404
    return json.dumps(coursename, default=str), 200


if __name__ == '__main__':
    app.run()
