class ColorNames:
    ImageMagickColorMap = {}
    ImageMagickColorMap["1"] = "#FFFFFF"
    ImageMagickColorMap["2"] = "#C1C1C1"
    ImageMagickColorMap["3"] = "#EF130B"
    ImageMagickColorMap["4"] = "#FF7100"
    ImageMagickColorMap["5"] = "#FFE400"
    ImageMagickColorMap["6"] = "#00CC00"
    ImageMagickColorMap["7"] = "#00B2FF"
    ImageMagickColorMap["8"] = "#231FD3"
    ImageMagickColorMap["9"] = "#A300BA"
    ImageMagickColorMap["10"] = "#D37CAA"
    ImageMagickColorMap["11"] = "#A0522D"
    ImageMagickColorMap["12"] = "#000000"
    ImageMagickColorMap["13"] = "#4C4C4C"
    ImageMagickColorMap["14"] = "#740B07"
    ImageMagickColorMap["15"] = "#C23800"
    ImageMagickColorMap["16"] = "#E8A200"
    ImageMagickColorMap["17"] = "#006400"
    ImageMagickColorMap["18"] = "#00569E"
    ImageMagickColorMap["19"] = "#0E0865"
    ImageMagickColorMap["20"] = "#550069"
    ImageMagickColorMap["21"] = "#A75574"
    ImageMagickColorMap["22"] = "#63300D"
    @staticmethod
    def rgbFromStr(s):
        # s starts with a #.
        r, g, b = int(s[1:3],16), int(s[3:5], 16),int(s[5:7], 16)
        return r, g, b

    @staticmethod
    def findNearestImageMagickColorName(RGB_tuple):
        return ColorNames.findNearestColorName(RGB_tuple, ColorNames.ImageMagickColorMap)

    @staticmethod
    def findNearestColorName(RGB_tuple, Map):
        R = RGB_tuple[0]
        G = RGB_tuple[1]
        B = RGB_tuple[2]
        mindiff = None
        for d in Map:
            r, g, b = ColorNames.rgbFromStr(Map[d])
            diff = abs(R -r)*256 + abs(G-g)* 256 + abs(B- b)* 256
            if mindiff is None or diff < mindiff:
                mindiff = diff
                mincolorname = d
        return mincolorname