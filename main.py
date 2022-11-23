import os
import datetime
import time
from threading import Thread

from flask import render_template, request, redirect, Response
from models import db, EmployeeModel
import cv2
from werkzeug.utils import secure_filename
from const import (
    make_flask_app,
    ALLOWED_EXTENSIONS,
    PATH_TO_YOUR_FOLDER,
    CAMERA_ADDRESS,
)

app = make_flask_app()
db.init_app(app)
global capture, rec_frame, grey, switch, neg, face, rec, out
capture = 0
grey = 0
neg = 0
face = 0
switch = 1
rec = 0
try:
    os.mkdir("./shots")
except OSError as error:
    pass


@app.route("/requests", methods=["POST", "GET"])
def tasks():
    global switch, camera
    if request.method == "POST":
        if request.form.get("click") == "Capture":
            global capture
            capture = 1
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
        elif request.form.get("stop") == "Stop/Start":

            if switch == 1:
                switch = 0
                camera.release()
                cv2.destroyAllWindows()

            else:
                camera = cv2.VideoCapture(0)
                switch = 1
        elif request.form.get("rec") == "Start/Stop Recording":
            global rec, out
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
        return render_template("index2.html")
    return render_template("index2.html")


@app.before_first_request
def create_table():
    db.create_all()


def record(out):
    global rec_frame
    while(rec):
        time.sleep(0.05)
        out.write(rec_frame)


def gen_frames():  # generate frame by frame from camera
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    video_capture = cv2.VideoCapture(0)
    # cv2.VideoCapture(addres)
    global out, capture, rec_frame
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
                print("here")
                capture = 0
                now = datetime.datetime.now()
                p = os.path.sep.join(
                    ["shots", "shot_{}.png".format(str(now).replace(":", ""))]
                )
                cv2.imwrite(p, frame)
            if(rec):
                rec_frame=frame
                frame= cv2.putText(cv2.flip(frame,1),"Recording...", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),4)
                frame=cv2.flip(frame,1)

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


@app.route("/")
def main():
    # Video streaming route. Put this in the src attribute of an img tag
    return render_template("index.html", count=0)


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


@app.route("/data")
def RetrieveList():
    employees = EmployeeModel.query.all()
    print(employees)
    return render_template("datalist.html", employees=employees)


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
    app.run(host="0.0.0.0", port=5001)
