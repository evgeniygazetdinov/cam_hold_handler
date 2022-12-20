import threading, Queue

dead_files = Queue.Queue()
END_OF_DATA = object()  # a unique sentinel value


def background_deleter():
    import os

    while True:
        path = dead_files.get()
        if path is END_OF_DATA:
            return
        try:
            os.remove(path)
        except:  # add the exceptions you want to ignore here
            pass  # or log the error, or whatever


deleter = threading.Thread(target=background_deleter)
deleter.start()

# when you want to delete a file, do:
# dead_files.put(file_path)

# when you want to shut down cleanly,
dead_files.put(END_OF_DATA)
deleter.join()
