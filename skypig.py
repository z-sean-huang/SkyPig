import Skype4Py
import time
import vtapi

PIG_ALERT = "('oo') skypig says:"

class MsgEvent(object):

    def __init__(self):
        APIKEY = "a90537cb88de70dcd81830bf602524055b7d3174f62322c36da9266f48d13638"
        self.vt = vtapi.VtApi(APIKEY)

    @staticmethod
    def __may_url(sUrl):
        if sUrl.startswith("www."):
            return True
        if sUrl.startswith("https://"):
            return True
        if sUrl.startswith("http://"):
            return True
        return False


    def MessageStatus(self, msg, status):
        if status not in [Skype4Py.cmsSent, Skype4Py.cmsReceived]:
            return

        sMsg = msg.Body
        if status == Skype4Py.cmsSent and sMsg.startswith(PIG_ALERT):
            return
        sMsg = sMsg.replace(";", " ").replace(",", " ")
        lWord = sMsg.split(" ")

        for sWord in lWord:
            if not self.__may_url(sWord):
                continue

            lRating = self.vt.rating(sWord)
            if not lRating:
                continue

            (iDetected, sLink) = lRating
            if iDetected == 0:
                continue

            msg.Chat.SendMessage("%s [%s] might be dangerous! Please check report: %s" % (PIG_ALERT, sWord, sLink))


# Create Skype instance
msgEvent = MsgEvent()
skype = Skype4Py.Skype(Events=msgEvent)
skype.Attach()


while(True):
    time.sleep(0.5)
