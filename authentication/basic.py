from similarity import feedback_relevent


with open("./authentication/relevent.txt", "r") as myfile:
    relevent = myfile.read()
feedback_relevent(relevent)