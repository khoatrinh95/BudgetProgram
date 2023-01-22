from Models import CellStyle
from Helpers import JsonHelper
import constants

def registerStyles(book):
    CellStyle.register_styles(book)

def createPatternFill(start_color, end_color, fill_type):
    return CellStyle.create_pattern_fill(start_color, end_color, fill_type)

def getStyle(name):
    styleLists = JsonHelper.read_json(constants.STYLE_JSON_PATH)
    return next(style for style in styleLists if style["name"].lower() == name.lower())