import datetime

fileName = "primes" + datetime.datetime.now().isoformat()
fileName = fileName.replace(":","")
fileName = fileName.replace("-","")
fileName = fileName.replace("T"," ")
fileName = fileName.replace(".","")
fileName = fileName +  ".txt"
path = "/output/"

with open(path + fileName,"a") as fileout:
    fileout.write("This is a test" + "\n")