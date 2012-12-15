class Path(object):
    def __init__(self, commands, style):
        self.commands = commands
        self.style = style

    def move(self, Br, Bi, angle):
        Br2 =  Br*cos(angle) + Bi*sin(angle)
        Bi2 = -Br*sin(angle) + Bi*cos(angle)

        for command in self.commands:
            if isinstance(command, list):
                try:
                    x, y = poincareDisk_to_hyperShadow(*internalToScreen(command[0], command[1], Br2, Bi2, angle))
                    command[0] = x
                    command[1] = y
                except ZeroDivisionError:
                    pass

    def svg(self):
        d = []
        for command in self.commands:
            if isinstance(command, list):
                x, y = command[0:2]
                d.append("%s %.18e,%.18e" % tuple([command[2]] + [x, -y])) # list(self.transformBack(*hyperShadow_to_poincareDisk(x, y)))))
            else:
                d.append("Z")
        d = " ".join(d)

        style = []
        for key, val in self.style.items():
            style.append("%s:%s" % (key, val))
        style = ";".join(style)

        return "<path d=\"%s\" style=\"%s\" />" % (d, style)

class Text(object):
    def __init__(self, position, position2, content, style):
        self.position = position
        self.position2 = position2
        self.content = content
        self.style = style

    def move(self, Br, Bi, angle):
        Br2 =  Br*cos(angle) + Bi*sin(angle)
        Bi2 = -Br*sin(angle) + Bi*cos(angle)
        self.position = poincareDisk_to_hyperShadow(*internalToScreen(self.position[0], self.position[1], Br2, Bi2, angle))
        self.position2 = poincareDisk_to_hyperShadow(*internalToScreen(self.position2[0], self.position2[1], Br2, Bi2, angle))

    def svg(self):
        selfstyle = dict(self.style)
        selfstyle["hackX2"] = "%.18e" % (self.position2[0])
        selfstyle["hackY2"] = "%.18e" % (-self.position2[1])

        style = []
        for key, val in selfstyle.items():
            style.append("%s:%s" % (key, val))
        style = ";".join(style)

        return "<text x=\"%.18e\" y=\"%.18e\" style=\"%s\">%s</text>" % (self.position[0], -self.position[1], style, self.content)

def loadSVG(documentRoot, coordinateSystem="hyperShadow"):
    originx = 0.0
    originy = 0.0
    unitx = 1.0
    unity = 1.0
    for elem in documentRoot.getchildren():
        if elem.tag == "{http://www.w3.org/2000/svg}rect" and elem.attrib["id"] == "UnitRectangle":
            originx = float(elem.attrib["x"])
            originy = float(elem.attrib["y"]) + float(elem.attrib["height"])
            unitx = float(elem.attrib["width"])
            unity = float(elem.attrib["height"])

    def transform(x, y):
        return (x - originx)/unitx, (originy - y)/unity

    def transformBack(x, y):
        return x*unitx + originx, -y*unity + originy

    def doit(elem, paths):
        style = dict(s.strip().split(":") for s in elem.attrib["style"].split(";"))
        # skip this path if it is not visible
        if style.get("visibility", "visible") == "visible" and style.get("display", "inline") != "none":
            d = re.split("[\s,]+", elem.attrib["d"].strip())
            commands = []
            i = 0
            while i < len(d):
                if d[i].upper() in ("M", "L"):
                    x, y = float(d[i+1]), float(d[i+2])
                    if coordinateSystem == "halfPlane":
                        commands.append(list(halfPlane_to_hyperShadow(*transform(x, y))) + [d[i].upper()])
                    elif coordinateSystem == "hyperShadow":
                        commands.append(list(transform(x, y)) + [d[i].upper()])
                    elif coordinateSystem == "poincareDisk":
                        commands.append(list(poincareDisk_to_hyperShadow(*transform(x, y))) + [d[i].upper()])
                    i += 2

                elif d[i].upper() == "Z":
                    commands.append("Z")

                i += 1

            p = Path(commands, style)
            p.transformBack = transformBack
            paths.append(p)

    paths = []
    for elem in documentRoot.getchildren():
        if elem.tag == "{http://www.w3.org/2000/svg}path":
            doit(elem, paths)
        elif elem.tag == "{http://www.w3.org/2000/svg}g":
            for e in elem.getchildren():
                if e.tag == "{http://www.w3.org/2000/svg}path":
                    doit(e, paths)

        if elem.tag == "{http://www.w3.org/2000/svg}text":
            style = dict(s.strip().split(":") for s in elem.attrib["style"].split(";"))
            a, b, c, d, e, f = map(float, elem.attrib.get("transform", "matrix(1,0,0,1,0,0)").replace("matrix(", "").replace(")", "").split(","))

            fontSize = float(style["font-size"].replace("px", ""))
            x1 = float(elem.attrib["x"])
            y1 = float(elem.attrib["y"])
            x2 = x1
            y2 = y1 - fontSize

            x1, y1 = (a*x1 + c*y1 + e), (b*x1 + d*y1 + f)
            x2, y2 = (a*x2 + c*y2 + e), (b*x2 + d*y2 + f)

            position1 = list(halfPlane_to_hyperShadow(*transform(x1, y1)))
            position2 = list(halfPlane_to_hyperShadow(*transform(x2, y2)))

            content = [elem.text.strip() if elem.text is not None else "",
                       elem.tail.strip() if elem.tail is not None else ""]
            for e in elem.getchildren():
                if e.tag == "{http://www.w3.org/2000/svg}tspan":
                    content.append(e.text.strip() if e.text is not None else "")
                    content.append(e.tail.strip() if e.tail is not None else "")
            text = Text(position1, position2, "".join(content), style)
            paths.append(text)

    return paths
