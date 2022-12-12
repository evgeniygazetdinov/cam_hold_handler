import os
import random
import string

randoms = "".join(
    [
        random.choice(string.ascii_letters + string.digits + string.punctuation)
        for n in range(12)
    ]
)


class RefreshSaver:
    LOG_PLACE = "{}/photo_catch.txt".format(os.getcwd())

    def set_position(self):
        f1 = open(self.LOG_PLACE, "a+")
        f1.write("1")
        f1.close()

    def photo_is_already_exist(self):
        if os.path.exists(self.LOG_PLACE):
            with open(self.LOG_PLACE) as f:
                lines = [line.rstrip("\n") for line in f]
                if "1" not in lines:
                    res = True
                else:
                    res = False
                    os.system(f"rm -rf {self.LOG_PLACE}")
        else:
            res = False
        return res
