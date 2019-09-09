from PyMessage import Message
from PyUUID import UUID
from PyGroup import PlayerItem, PlayerMap, Group
from PyPlayer import Player
from PyPolynomials import PolynomialVals
import json


class GroupSecretSetupMessage:

    def __init__(self, MsgType = Message.Type.GROUP_SECRET_SETUP, uri = None, groupID = None, playerMap = None):
        self.base = MsgType
        self.mProposerUri = uri
        self.mGroupID = groupID
        if (groupID is None):
          self.mGroupID = UUID().getUUIDString()
        self.mPlayers = playerMap
        if (playerMap is None):
          self.mPlayers = PlayerMap()
        self.polynomialFunctions = PolynomialVals()

    def  getProposerURI(self):
        return self.mProposerUri

    def getID(self):
        return self.mGroupID

    def setID(self, mGroupID):
        self.mGroupID = mGroupID

    def getPlayers(self):
        return self.mPlayers

    def jsonObjectType(self):
        return "GroupSecretSetupMessage"

    def addPolynomialFunction(self, byUrl, forUrl, polyVal):
      self.polynomialFunctions.addPolynomialFunction(byUrl, forUrl, polyVal)

    def removePolynomialFunction(self, byUrl, forUrl, polyVal=None):
        self.polynomialFunctions.removePolynomialFunction(byUrl, forUrl, polyVal)

    def clearPolynomialFunction(self):
        self.polynomialFunctions.clearPolynomialFunction()

    def getPolynomialFunction(self):
        return self.polynomialFunctions.getPolynomialFunction()


    def __eq__(self, other):
        if not isinstance(other, GroupSecretSetupMessage):
            return False
        return (self.getID() == other.getID()) and (self.getPlayers().getPlayersSortedByOrdinal() == other.getPlayers().getPlayersSortedByOrdinal()) and (self.getProposerURI() == other.getProposerURI()) and (self.base == other.base)

    def __str__(self):
        val = ""
        val += str(self.getID())+"\n\n"
        val += str(self.getProposerURI())+"\n\n"
        val += str(self.base)+"\n\n"
        for playerItem in self.getPlayers().getItems():
            val +=  str(playerItem.player)+"\n\n"
        val += str(self.polynomialFunctions)
        return val


    def to_json(self):
        gpStMsgDt = {}
        gpStMsgDt["Type"] = Message.getStrByType(self.base)
        gpStMsgDt["Proposer"] = self.mProposerUri
        gpStMsgDt["GroupID"] = self.getID()
        playerJson = []
        for playerItem in self.getPlayers().getItems():
            playerJson.append(playerItem.player.to_json())

        gpStMsgDt["Players"] = playerJson
        gpStMsgDt["Polynomials"] = self.polynomialFunctions.to_json()
        return json.dumps(gpStMsgDt)
    

    def from_json(self, gpStMsgStr):
        gpStMsgDt = json.loads(gpStMsgStr)
        self.base =  Message.getTypeByStr(gpStMsgDt["Type"])
        self.mProposerUri = gpStMsgDt["Proposer"]
        self.setID(gpStMsgDt["GroupID"])
        for playerDict in gpStMsgDt["Players"] :
            p = Player()
            p.from_json(playerDict)
            pi = PlayerItem(p.getURI(), p)
            self.getPlayers().add(pi)
        self.polynomialFunctions.from_json(gpStMsgDt["Polynomials"])
        '''
        for polyValStr in gpStMsgDt["Polynomials"]:
          # get into List
          polyValList = polyValStr.split(", ") 
          self.addPolynomialFunction(polyValList[0], polyValList[1], int(polyValList[2])) 
        '''

  

if __name__ == '__main__':
    p1 = Player("p1", 1, False, False)
    p2 = Player("p2", 2, False, False)
    p3 = Player("p3", 3, False, False)
    p4 = Player("p4", 4, False, False)


    p11 = PlayerItem("player1@mycorp.com", p1)
    p22 = PlayerItem("player2@mycorp.com", p2)
    p33 = PlayerItem("player3@mycorp.com", p3)
    p44 = PlayerItem("player4@mycorp.com", p4)

    playersMap = PlayerMap()
    playersMap.add(p11)
    playersMap.add(p22)
    playersMap.add(p33)
    playersMap.add(p44)

    gp = GroupSecretSetupMessage( uri="player1@mycorp.com", playerMap=playersMap)
    #gp1 = GroupSecretSetupMessage(MsgType= Message.Type.POOL_BUILDER_SETUP, uri="player1@mycorp.com", playerMap=playersMap)
    gpJson=gp.to_json()
    #print(gpJson)
    #print("#####################")
    print(gp)
    gpFJson = GroupSecretSetupMessage()
    gpFJson.from_json(gpJson)
    print(gpFJson == gp)



