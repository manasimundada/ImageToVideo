import mysql.connector
import json
import os
import shutil
import numpy as np
import cv2
import hashlib
import psycopg2
from io import BytesIO
from werkzeug.datastructures import FileStorage

def test():
    db = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = db.cursor()
    query = "SELECT * FROM users;"
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)

def add_user(username, email, password, name):
    db = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = db.cursor()
    id_get = "SELECT user_id FROM users;"
    cursor.execute(id_get)
    results = cursor.fetchall()
    if len(results) == 0:
        new_id = 1
    else:
        new_id = int(results[-1][0]) + 1
    query = "INSERT INTO users VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (new_id, username, email, password, name))
    db.commit()
    #remember: ALTER TABLE your_table_name AUTO_INCREMENT = 1;
    #nvm no longer necessary just changed auto increment

def add_image(user_id, filename):
    db = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = db.cursor()
    id_get = "SELECT image_id FROM images;"
    cursor.execute(id_get)
    results = cursor.fetchall()
    if len(results) == 0:
        new_id = 1
    else:
        new_id = int(results[-1][0]) + 1
    query = "INSERT INTO images (image_id, user_id, filename) VALUES (%s, %s, %s)"
    cursor.execute(query, (new_id, user_id, filename))
    db.commit()

def delete_user(user_id):
    db = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = db.cursor()
    user_command = "DELETE FROM users WHERE user_id = %s;"
    image_command = "DELETE FROM images WHERE user_id = %s;"
    cursor.execute(user_command, (user_id,))
    cursor.execute(image_command, (user_id,))
    db.commit()

def delete_image(user_id, image_id):
    db = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = db.cursor()
    command = "DELETE FROM images WHERE user_id = %s AND image_id = %s;"
    cursor.execute(command, (user_id, image_id))
    db.commit()

def delete_all_image(user_id):
    db = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = db.cursor()
    command = "DELETE FROM images WHERE user_id = %s;"
    cursor.execute(command, (user_id,))
    db.commit()

def erase(table_name):
    db = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = db.cursor()
    command = "DELETE FROM %s;"
    cursor.execute(command, (table_name,))
    db.commit()

def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

#checks if user exists or checks for admin creds
def check_user(username, password):
    db = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = db.cursor()
    if username == 'susadmin' and password == 'amogus':
        return 1
    password = hash_password(password)
    query = "SELECT * FROM users WHERE username = %s AND password = %s;"
    cursor.execute(query, (username, password))
    results = cursor.fetchall()
    if len(results) == 0: #invalid username or password
        return 0
    return 1

def move_images(username,uid,files):
    db = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = db.cursor()
    for file in files:
        if file.filename == '':
            return 'No selected file', 400
        user_id = uid
        command = "SELECT COUNT(image_id) FROM images;"
        cursor.execute(command)
        image_id = cursor.fetchone()[0] + 1
        file_contents = file.read()
        binary_data = BytesIO(file_contents).read()
        insert_query = "INSERT INTO images (image_id, user_id, data, filename) VALUES (%s, %s, %s, %s)"
        image_metadata = file.filename
        image_values = (image_id, user_id, psycopg2.Binary(binary_data),image_metadata)
        cursor.execute(insert_query, image_values)
        db.commit()
    db.commit()

def fetch_images(user_id):
    db = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = db.cursor()
    query = "SELECT data FROM images WHERE user_id= %s;"
    cursor.execute(query,(user_id,))
    results = cursor.fetchall()
    img_list = []
    for row in results:
        image_data = row[0]
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img_list.append(img)
        # cv2.imshow('Image', img)
        # cv2.waitKey(0)
        #press ANY button to close the window UwU
    cv2.destroyAllWindows()
    return img_list

def fetch_users():
    db = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = db.cursor()
    query = "SELECT * FROM users;"
    cursor.execute(query)
    results = cursor.fetchall()
    dic = {}
    for i in results:
        dic[i[1]] = {'user_id': i[0], 'username': i[1], 'password': i[3], 'name': i[4], 'email': i[2]}
    # print(dic)
    return dic

def add_audio(filename):
    db = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = db.cursor()
    id_get = "SELECT audio_id FROM audio;"
    cursor.execute(id_get)
    results = cursor.fetchall()
    if len(results) == 0:
        new_id = 1
    else:
        new_id = int(results[-1][0]) + 1
    with open(f'/home/vishal/ug1/ISS/course-project-edgarallanpoopoo/{filename}', 'rb') as f:
        audio_data = f.read()
        command = "INSERT INTO audio (audio_id, data, filename) VALUES (%s, %s, %s);"
        cursor.execute(command, (new_id, audio_data, filename))
    db.commit()

# image_file_paths = ['./static/images/image6.png','./static/images/image5.png']
# image_files = [FileStorage(open(file_path, 'rb')) for file_path in image_file_paths]
# move_images('amol',1,image_files)