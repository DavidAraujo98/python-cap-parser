from structures import classes, enums
import xml.etree.ElementTree as ET
import inspect


def parse(filePath=None, stringXML=None):
    if filePath != None:
        file = open(filePath, "r")
        stringXML = file.read()
        file.close()
    root = ET.fromstring(stringXML)
    return _recursiveParser(root)


def _recursiveParser(parent):
    _, _, tagName = parent.tag.rpartition('}')
    obj = None
    if(tagName == str(classes.Alert())):
        obj = classes.Alert()
    elif(tagName == str(classes.Info())):
        obj = classes.Info()
    elif(tagName == str(classes.EventCode())):
        obj = classes.EventCode()
    elif(tagName == str(classes.Parameter())):
        obj = classes.Parameter()
    elif(tagName == str(classes.Resource())):
        obj = classes.Resource()
    elif(tagName == str(classes.Area())):
        obj = classes.Area()
    elif(tagName == str(classes.Geocode())):
        obj = classes.Geocode()
    else:
        return None

    for child in parent:
        _, _, childTagName = child.tag.rpartition('}')
        if len(child) == 0:
            for attr in inspect.getmembers(obj):
                if attr[0] == childTagName:
                    if len(parent.findall(child.tag)) == 1:
                        setattr(obj, childTagName, child.text)
                    else:
                        getattr(obj, childTagName).append(child.text)
        else:
            getattr(obj, childTagName).append(_recursiveParser(child))

    return obj

def deparse(alert):
    return ET.tostring(_recursiveDeparser(alert), encoding='utf8')

def writeAlertToFile(alert, filePath):
    root = _recursiveDeparser(alert)
    tree = ET.ElementTree(root)
    with open("CAP-v1.2.xsd") as f:
        xmlschema_doc = etree.parse(f)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    xmlschema.assertValid(doc)

    with open(filePath, "wb") as files:
        tree.write(files)

def _recursiveDeparser(obj, outputFilePath=None):
    root = ET.Element(str(obj))
    for attr in inspect.getmembers(obj):
        if not attr[0].startswith('_') and not inspect.ismethod(attr[1]) and attr[1] != None and attr[0] != []:
            if attr[0] == "xmlns":
                root.set(attr[0], attr[1])
            elif isinstance(attr[1], list):
                for item in attr[1]:
                    if isinstance(item, classes.Alert) or isinstance(item, classes.Info) or isinstance(item, classes.EventCode) or isinstance(item, classes.Parameter) or isinstance(item, classes.Resource) or isinstance(item, classes.Area) or isinstance(item, classes.Geocode):
                        root.append(_recursiveDeparser(item))
                    else:
                        child = ET.SubElement(root, attr[0])
                        child.text = item
            else:
                if isinstance(attr[1], classes.Alert) or isinstance(attr[1], classes.Info) or isinstance(attr[1], classes.EventCode) or isinstance(attr[1], classes.Parameter) or isinstance(attr[1], classes.Resource) or isinstance(attr[1], classes.Area) or isinstance(attr[1], classes.Geocode):
                    root.append(_recursiveDeparser(attr[1]))
                else:
                    child = ET.SubElement(root, attr[0])
                    child.text = attr[1]

    return root

