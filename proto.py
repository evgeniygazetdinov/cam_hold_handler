
import cv2
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse


#  ====== 

from fastapi import FastAPI, Depends

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
app = FastAPI()

engine = create_engine("sqlite:////~/Documents/ppython/my_db.db")
Session = sessionmaker(bind=engine)
def get_db():
    return Session()


from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from databases import Database

database = Database("sqlite:///test.db")


@app.on_event("startup")
async def database_connect():
    await database.connect()


@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect()


@app.post("/test")
async def fetch_data(id: int):
    query = "SELECT * FROM tablename WHERE ID={}".format(str(id))
    results = await database.fetch_all(query=query)


# ======

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
templates = Jinja2Templates(directory="templates")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades 
                                     + 'haarcascade_frontalface_default.xml')
video_capture = cv2.VideoCapture(0) 

def find_and_kill_camera_process():
    from subprocess import PIPE, Popen
    def command(command):
            process = Popen(
            args=command,
            stdout=PIPE,
            shell=True)
            return process.communicate()[0]
    process = command('fuser /dev/')
    if process:
        killing_process = str(process).split(' ')[-1]
        command(f'kill -9 {killing_process}')


def gen_frames():  # generate frame by frame from camera
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
                                                flags=cv2.CASCADE_SCALE_IMAGE
                                            )

            for (x, y, w, h) in faces:
            # for each face on the image detected by OpenCV
            # draw a rectangle around the face
                cv2.rectangle(frame, 
                            (x, y), # start_point
                            (x+w, y+h), # end_point
                            (255, 0, 0),  # color in BGR
                            2) # thickness in px
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/my_db")
def an_endpoint_using_sql(db = Depends(get_db)):
    # ...
    # do some SQLAlchemy
    # ...
    return {"msg": "an exceptionally successful operation!"}

@app.get('/video_feed')
def video_feed():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)
    find_and_kill_camera_process()