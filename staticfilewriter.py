import datetime
import fcntl

class StaticFileWriter:
  fileName = "primes" + datetime.datetime.now().isoformat()
  fileName = fileName.replace(":","")
  fileName = fileName.replace("-","")
  fileName = fileName.replace("T"," ")
  fileName = fileName.replace(".","")
  fileName = fileName +  ".txt"
  path = "/output/"

  def appendLine(self, stringToWrite):
    print("Writing to %s%s"%(StaticFileWriter.path, StaticFileWriter.fileName))
    with open(StaticFileWriter.path + StaticFileWriter.fileName,"a") as fileout:
        fcntl.flock(fileout, fcntl.LOCK_EX)
        fileout.write(stringToWrite + "\n")
        fcntl.flock(fileout, fcntl.LOCK_UN)