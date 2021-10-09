# Script by Bastien Mathou
#
#  ______   _______  _        _        _______  _                      _______  _______  _______ _________ _______  _______ _________
# (  ___ \ (  ___  )( \      | \    /\(  ___  )( (    /||\     /|     (  ____ )(  ____ )(  ___  )\__    _/(  ____ \(  ____ \\__   __/
# | (   ) )| (   ) || (      |  \  / /| (   ) ||  \  ( |( \   / )     | (    )|| (    )|| (   ) |   )  (  | (    \/| (    \/   ) (   
# | (__/ / | (___) || |      |  (_/ / | (___) ||   \ | | \ (_) /_____ | (____)|| (____)|| |   | |   |  |  | (__    | |         | |   
# |  __ (  |  ___  || |      |   _ (  |  ___  || (\ \) |  \   /(_____)|  _____)|     __)| |   | |   |  |  |  __)   | |         | |   
# | (  \ \ | (   ) || |      |  ( \ \ | (   ) || | \   |   ) (        | (      | (\ (   | |   | |   |  |  | (      | |         | |   
# | )___) )| )   ( || (____/\|  /  \ \| )   ( || )  \  |   | |        | )      | ) \ \__| (___) ||\_)  )  | (____/\| (____/\   | |   
# |/ \___/ |/     \|(_______/|_/    \/|/     \||/    )_)   \_/        |/       |/   \__/(_______)(____/   (_______/(_______/   )_(   
#

# DESCRIPTION :
# this is an mixed ia/classical-stat program for predict result of french loto
# this python script run multiple time a modify version of this ia-script : 
# https://github.com/berba1995/Deep_Learning_et_le_Hasard/blob/main/DEEP_LEARNING_ET_LE_HASARD.ipynb
# After an acquisition result sequence the script process data mixed ia-result with more classic statistical calculus result. 
#
# warning:this script was realized by an totaly neewbie python user.
#
# This is THE BALKANIE PROJECT
# Good Luck !

from pymongo import MongoClient
from Prediction import Prediction
from Occurence import Occurence
import os

#Nb de cycle d'aprentisage / prediction
NB_LEARNING_CYCLE=70

#############################################################################
# definition: Predict loto result just that.
#############################################################################
def predictLoto(): 
    launchAcquisitionSequence()
    predictions = getIaPredictionResult()
    processPredictions(predictions)

#############################################################################
# definition: launchAcquisitionSequence
# This function call an limited number of iteration the ia-script
# the ia script save the result of each iteration in mongodb database
#############################################################################
def launchAcquisitionSequence():
    print('----- START ACQUISITION -----')
    for i in range(NB_LEARNING_CYCLE):
        os.system('runipy ./LOTO-ENGINE/predict-engine.ipynb')
    print('----- END ACQUISITION -----')


#############################################################################
# definition: getIaPredictionResults
# This function retrieve data from mongoDb
#############################################################################
def getIaPredictionResult():
    bddData = getPredictionsFromBdd()
    predictions = []

    for data in bddData:
        tirage = getTirageFromPrediction(data)    
        nbChance = getNbChanceFromPrediction(data)
        predictions.append(Prediction(nbChance,tirage))

    return predictions

#############################################################################
# definition: getPredictionsFromBdd
# This function retrieve data from mongoDb
#############################################################################
def getPredictionsFromBdd():
    client = MongoClient("mongodb://localhost:27017")
    dbConnection=client.prediction
    collection = dbConnection.lotoPrediction
    bddData = collection.find()
    return bddData

#############################################################################
# definition: getTirageFromPrediction
# This function format tirage data from mongoDb
#############################################################################
def getTirageFromPrediction(cursor):
    tirage = [0] * 5
    tirage[0] = int(cursor['1nb'])
    tirage[1] = int(cursor['2nb'])
    tirage[2] = int(cursor['3nb'])
    tirage[3] = int(cursor['4nb'])
    tirage[4] = int(cursor['5nb'])
    return tirage

#############################################################################
# definition: getNbChanceFromPrediction
# This function format nbChance data from mongoDb
#############################################################################
def getNbChanceFromPrediction(cursor):
    return cursor['chanceNb']

#############################################################################
# definition: def processPredictions
# This function format tirage data from mongoDb
#############################################################################
def processPredictions(predictions):
    nbOccurenceByNumber = getNbOccurenceByNumber(predictions)

    NAME_FILE_OCCURENCE = "prediction-occurence.txt"
    os.system('touch '+ NAME_FILE_OCCURENCE)

    for prediction in predictions:
        writePredictionInFile(prediction)

    nbOccurenceByNumber.sort(key=lambda x: x.number)
    for occurence in nbOccurenceByNumber:
        writeOccurenceInFile(NAME_FILE_OCCURENCE,occurence)

    for i in [0,1,2,3,4]:
         writeOccurenceByPositionInFile(NAME_FILE_OCCURENCE, getNbOccurenceByNumberByPosition(predictions,i), i)

    return nbOccurenceByNumber

#############################################################################
# definition: getNbOccurenceByNumberByPosition
# Get number occurence by number in positions 
#############################################################################
def getNbOccurenceByNumberByPosition(predictions, position):
    nbOccurenceByNumberPosition = []

    for prediction in predictions:
        number = prediction.tirage[position]
        if (not existInOccurenceList(number,nbOccurenceByNumberPosition)):
            nbOccurenceByNumberPosition.append(Occurence(number))

    return nbOccurenceByNumberPosition

#############################################################################
# definition: processPredictions
# Get number occurence by number
#############################################################################
def getNbOccurenceByNumber(predictions):
    nbOccurenceByNumber = []

    for prediction in predictions:
        for number in prediction.tirage:
            if (not existInOccurenceList(number,nbOccurenceByNumber)):
               nbOccurenceByNumber.append(Occurence(number))

    return nbOccurenceByNumber

#############################################################################
# definition: existInOccurenceList
# if the number 
#############################################################################
def existInOccurenceList(number, nbOccurenceByNumber):
    isExist = False

    for occurence in nbOccurenceByNumber:
        if(occurence.number == number):
            isExist = True
            occurence.incrementOccurence()

    return isExist

################# TEMPS QUE PAS D'IHM #########################################
def writePredictionInFile(prediction):

    NAME_FILE_PREDICTION = "prediction-tirage.txt"
    os.system('touch '+ NAME_FILE_PREDICTION)

    f = open(NAME_FILE_PREDICTION, "a")
    f.write(str(prediction.tirage[0])+ " " 
            + str(prediction.tirage[1])+ " "
            + str(prediction.tirage[2])+ " "
            + str(prediction.tirage[3])+ " "
            + str(prediction.tirage[4])+ "  "
            + str(prediction.nbChance)
            + "\n")
    f.close()

def writeOccurenceInFile(NAME_FILE_OCCURENCE, occurence):
    f = open(NAME_FILE_OCCURENCE, "a")
    f.write("number " + str(occurence.number)
            +" occurence " + str(occurence.totalOccurence)
            + "\n")
    f.close()

def writeOccurenceByPositionInFile(NAME_FILE_OCCURENCE, ocurences , position):

    f = open(NAME_FILE_OCCURENCE, "a")
    f.write("\n \n ################### position : " + str(position) + " ########## \n")
    ocurences.sort(key=lambda x: x.number)
    for ocurence in ocurences:
        f.write("number " + str(ocurence.number)
                +" occurence " + str(ocurence.totalOccurence)
                + "\n")
    f.close()

## Launch Script ##
predictLoto()




