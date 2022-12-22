import constants
from Helpers import JsonHelper
from openpyxl.styles import NamedStyle, Font, Border, Side, PatternFill, Alignment, Protection


class AlignmentCustom:
    def __init__(self, horizontal=None, vertical=None, textRotation=None, wrapText=None, shrinkToFit=None, indent=None):
        self.indent = indent
        self.shrinkToFit = shrinkToFit
        self.wrapText = wrapText
        self.textRotation = textRotation
        self.vertical = vertical
        self.horizontal = horizontal


class FillCustom:
    def __init__(self, fillType=None, startColor=None, endColor=None):
        self.endColor = endColor
        self.startColor = startColor
        self.fillType = fillType


class FontCustom:
    def __init__(self, name=None, bold=None, size=None, italic=None, vertAlign=None, underline=None, strike=None,
                 color=None):
        self.color = color
        self.name = name
        self.underline = underline
        self.vertAlign = vertAlign
        self.italic = italic
        self.size = size
        self.bold = bold
        self.strike = strike


class BorderCustom:
    def __init__(self, borderStyle=None, color=None):
        self.color = color
        self.borderStyle = borderStyle


class ProtectionCustom:
    def __init__(self, locked=None, hidden=None):
        self.hidden = hidden
        self.locked = locked


class CellStyleCustom:
    def __init__(self, name=None, font=None, alignment=None, border=None, fill=None, protection=None):
        self.protection = protection
        self.name = name
        self.font = font
        self.alignment = alignment
        self.border = border
        self.fill = fill


def readStyles():
    styles = JsonHelper.readJson(constants.STYLE_JSON_PATH)
    cellStyleList = []

    for style in styles:
        name = style[constants.STYLE_NAME]
        font = FontCustom(**style[constants.STYLE_FONT]) if constants.STYLE_FONT in style else None
        border = BorderCustom(**style[constants.STYLE_BORDER]) if constants.STYLE_BORDER in style else None
        fill = FillCustom(**style[constants.STYLE_FILL]) if constants.STYLE_FILL in style else None
        alignment = AlignmentCustom(**style[constants.STYLE_ALIGNMENT]) if constants.STYLE_ALIGNMENT in style else None
        protection = ProtectionCustom(
            **style[constants.STYLE_PROTECTION]) if constants.STYLE_PROTECTION in style else None
        cellStyle = CellStyleCustom(name=name, font=font, alignment=alignment, border=border, fill=fill,
                                    protection=protection)
        cellStyleList.append(cellStyle)
    return cellStyleList


def registerStyle(style, book):
    styleName = style.name
    styleFont = style.font
    styleFill = style.fill
    styleAlignment = style.alignment
    styleBorder = style.border
    styleProtection = style.protection

    wb = book.book
    if styleName in wb.named_styles:
        del wb._named_styles[wb.style_names.index(styleName)]

    registeredStyle = NamedStyle(name=styleName)

    if styleFont is not None:
        registeredStyle.font = Font(name=styleFont.name, size=styleFont.size, bold=styleFont.bold,
                                    italic=styleFont.italic, vertAlign=styleFont.vertAlign, underline=styleFont.underline,
                                    strike=styleFont.strike, color=styleFont.color)

    if styleBorder is not None:
        bd = Side(style=styleBorder.borderStyle, color=styleBorder.color)
        registeredStyle.border = Border(left=bd, top=bd, right=bd, bottom=bd)

    if styleFill is not None:
        registeredStyle.fill = PatternFill(fill_type=styleFill.fillType, start_color=styleFill.startColor,
                                           end_color=styleFill.endColor)

    if styleAlignment is not None:
        registeredStyle.alignment = Alignment(horizontal=styleAlignment.horizontal, vertical=styleAlignment.vertical,
                                              text_rotation=styleAlignment.textRotation,
                                              wrap_text=styleAlignment.wrapText,
                                              shrink_to_fit=styleAlignment.shrinkToFit, indent=styleAlignment.indent)

    if styleProtection is not None:
        registeredStyle.protection = Protection(locked=styleProtection.locked, hidden=styleProtection.hidden)

    return registeredStyle


def registerStyles(book):
    styleList = readStyles()
    for style in styleList:
        namedStyle = registerStyle(style, book)
        book.book.add_named_style(namedStyle)


def createPatternFill(startColor, endColor, fillType):
    return PatternFill(start_color=startColor, end_color=endColor, fill_type=fillType)