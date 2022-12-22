from Models import CellStyle
from Helpers import JsonHelper
import constants

def registerStyles(book):
    CellStyle.registerStyles(book)

def createPatternFill(startColor, endColor, fillType):
    return CellStyle.createPatternFill(startColor, endColor, fillType)

def getStyle(name):
    styleLists = JsonHelper.readJson(constants.STYLE_JSON_PATH)
    return next(style for style in styleLists if style["name"].lower() == name.lower())