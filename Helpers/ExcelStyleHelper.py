from Models import CellStyle

def registerStyles():
    CellStyle.registerStyles()

def createPatternFill(startColor, endColor, fillType):
    return CellStyle.createPatternFill(startColor, endColor, fillType)