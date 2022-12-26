import os
import datetime
import time
from threading import Thread

from flask import render_template, request, redirect, url_for, Response
from flask_migrate import Migrate
from models import db, EmployeeModel, PhotoModel, PictureForSave
import cv2
from const import make_camera_flask_app, my_tiny_log_decorator
from writer import RefreshSaver
from packages.session import Session

refresh = RefreshSaver()
session = Session()
app = make_camera_flask_app()
db.init_app(app)
migrate = Migrate(app, db)
global capture, rec_frame, grey, switch, neg, face, rec, out, picture_name
capture = 0
grey = 0
neg = 0
face = 0
switch = 1
rec = 0


@my_tiny_log_decorator
def get_current_picture_name():
    # update to session with json
    now = datetime.datetime.now()
    formating_now = "shot_{}.png".format(str(now).replace(":", "").replace(" ", ""))
    location = os.path.sep.join(["shots", formating_now])
    session.store_photo(formating_now)
    return location


def store_photo():
    pic_location = get_current_picture_name()
    my_photo = PhotoModel(
        store_location=pic_location,
        name=datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
    )
    db.session.add(my_photo)
    db.session.commit()


def get_first_and_delete():
    for_store = PictureForSave.query.all()
    cur_loc = for_store.store_location
    db.session.delete(for_store)
    db.session.commit()
    return cur_loc


@app.route("/", methods=["POST", "GET"])
def tasks():
    global switch, camera
    if request.method == "POST":
        if request.form.get("click") == "Capture":
            if session.photo_not_exist():
                global capture
                capture = 1
                store_photo()
        elif request.form.get("grey") == "Grey":
            global grey
            grey = not grey
        elif request.form.get("neg") == "Negative":
            global neg
            neg = not neg
        elif request.form.get("face") == "Face Only":
            global face
            face = not face
            if face:
                time.sleep(4)
        elif request.form.get("all_photos") == "all photos":
            return redirect(url_for("photo_list"))
        elif request.form.get("stop") == "Stop/Start":
            if switch == 1:
                switch = 0
                camera.release()
                cv2.destroyAllWindows()
            else:
                camera = cv2.VideoCapture(0)
                switch = 1
        elif request.form.get("rec") == "Start/Stop Recording":
            global rec, out, rec_frame
            rec = not rec
            if rec:
                now = datetime.datetime.now()
                fourcc = cv2.VideoWriter_fourcc(*"XVID")
                out = cv2.VideoWriter(
                    "vid_{}.avi".format(str(now).replace(":", "")),
                    fourcc,
                    20.0,
                    (640, 480),
                )
                # Start new thread for recording the video
                thread = Thread(
                    target=record,
                    args=[
                        out,
                    ],
                )
                thread.start()
            elif rec == False:
                out.release()

    elif request.method == "GET":
        return render_template("index.html")
    return render_template("index.html")


@app.before_first_request
def create_table():
    db.create_all()
    db.session.commit()


def record(out):
    global rec_frame
    while rec:
        time.sleep(0.05)
        out.write(rec_frame)


def gen_frames():  # generate frame by frame from camera
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    video_capture = cv2.VideoCapture(0)
    # cv2.VideoCapture(addres)
    global out, capture, rec_frame, picture_name
    while True:
        # Capture frame-by-frame
        success, frame = video_capture.read()  # read the camera frame
        if not success:
            break
        else:
            ret, frame = video_capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5,
                minSize=(100, 100),
                flags=cv2.CASCADE_SCALE_IMAGE,
            )
            if capture:
                picture_name = session.get_photo_name()
                cv2.imwrite(picture_name, frame)
                capture = 0
            if rec:
                rec_frame = frame
                frame = cv2.putText(
                    cv2.flip(frame, 1),
                    "Recording ",
                    (0, 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    4,
                )
                frame = cv2.flip(frame, 1)

            for (x, y, w, h) in faces:
                # for each face on the image detected by OpenCV
                # draw a rectangle around the face
                cv2.rectangle(
                    frame,
                    (x, y),  # start_point
                    (x + w, y + h),  # end_point
                    (255, 0, 0),  # color in BGR
                    2,
                )  # thickness in px
                ret, buffer = cv2.imencode(".jpg", frame)
                frame = buffer.tobytes()
                yield (
                    b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                )  # concat frame one by one and show result


@app.route("/1")
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/data/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("createpage.html")

    if request.method == "POST":
        employee_id = request.form["employee_id"]
        name = request.form["name"]
        age = request.form["age"]
        position = request.form["position"]
        employee = EmployeeModel(
            employee_id=employee_id, name=name, age=age, position=position
        )
        db.session.add(employee)
        db.session.commit()
        return redirect("/data")


@app.route("/photo_list")
def photo_list():
    all_photos = PhotoModel.query.all()
    for photos in all_photos:
        photos.store_location = os.getcwd() + "/" + photos.store_location
    return render_template("all_photo.html", all_photos=all_photos)


@app.route("/photo_delete/<int:id>")
def remove_photo_by_id(id):
    employee = PhotoModel.query.filter_by(id=id).first()
    if employee:
        command = f"{os.getcwd() + '/'  + employee.store_location}"
        try:
            os.remove(command)
        except:
            pass
        db.session.delete(employee)
        db.session.commit()
    return redirect("/photo_list")


@app.route("/data/<int:id>")
def RetrieveEmployee(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if employee:
        return render_template("data.html", employee=employee)
    return f"Employee with id ={id} Doenst exist"


@app.route("/data/<int:id>/update", methods=["GET", "POST"])
def update(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == "POST":
        if employee:
            db.session.delete(employee)
            db.session.commit()
            name = request.form["name"]
            age = request.form["age"]
            position = request.form["position"]
            employee = EmployeeModel(
                employee_id=id, name=name, age=age, position=position
            )
            db.session.add(employee)
            db.session.commit()
            return redirect(f"/data/{id}")
        return f"Employee with id = {id} Does nit exist"

    return render_template("update.html", employee=employee)


@app.route("/data/<int:id>/delete", methods=["GET", "POST"])
def delete(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == "POST":
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return redirect("/data")
        abort(404)

    return render_template("delete.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
