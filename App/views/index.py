from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for
from App.models import db, Exercise
from App.controllers import create_user
import csv

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('login.html')

@index_views.route('/index', methods=['GET'])
def get_index_page():
    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    csv_file = 'csv/MegaGymDataset.csv'

    try:
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Handle missing or empty fields
                for key, value in row.items():
                    if value == '':
                        row[key] = None
                
                # Create Exercise object and add to database
                exercise = Exercise(
                    title=row['Title'],
                    description=row['Desc'],
                    exercise_type=row['Type'],
                    bodypart=row['BodyPart'],
                    equipment=row['Equipment'],
                    level=row['Level'],
                    rating=float(row['Rating']) if row['Rating'] else None,
                    rating_desc=row['RatingDesc']
                )
                db.session.add(exercise)

        # Commit changes to the database
        db.session.commit()
        print("Exercises initialized successfully.")

    except Exception as e:
        # Rollback changes and print error message
        db.session.rollback()
        print("Error initializing exercises:", e)
    create_user('bob', 'bobpass')
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

