import xml.sax as sax
from xml.sax import handler
from xml.dom import minidom


class Student:
    def __init__(self, name: str="", course: str="", group: str="", total: str="", done: str="", language: str="", not_done: str="") -> None:
        self.name = name
        self.course = course
        self.group = group
        self.total = total
        self.done = done
        self.language = language
        self.not_done = not_done
    pass

available_language = set()


class RegistryHandler(handler.ContentHandler):
    def __init__(self) -> None:
        self.registry = list()
        self.CurrentData = ""
        self.name = ""
        self.course = ""
        self.group = ""
        self.total = ""
        self.done = ""
        self.language = ""
        self.not_done = ""

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "student":
            self.registry.append(Student())


    def endElement(self, tag):
        self.CurrentData = ""


    def characters(self, content):
        if self.CurrentData == "name":
            self.registry[-1].name = content
        elif self.CurrentData == "course":
            self.registry[-1].course = content
        elif self.CurrentData == "group":
            self.registry[-1].group = content
        elif self.CurrentData == "total":
            self.registry[-1].total = content
        elif self.CurrentData == "done":
            self.registry[-1].done = content
        elif self.CurrentData == "language":
            available_language.add(content)
            self.registry[-1].language = content
        elif self.CurrentData == "not_done":
            self.registry[-1].not_done = content
    pass


def parse_file(path) -> list[Student]:
    content: str
    if path == "":
        return []
    else:
        with open(path) as xml_file:
            content = xml_file.read()
    reg_handler = RegistryHandler()
    # print(content)
    sax.parseString(content, reg_handler)
    return reg_handler.registry


def write_to_xml(students: list[Student], path):
    def create_field(dom: minidom.Document, tag_name: str, text) -> minidom.Element:
        tag = dom.createElement(tag_name)
        text_node = dom.createTextNode(text)
        tag.appendChild(text_node)
        return tag

    with open(path, mode="w") as xml_file:
        DOMTree = minidom.Document()
        registry = DOMTree.createElement("registry")
        for i in students:
            student = DOMTree.createElement('students')
            student.appendChild(create_field(DOMTree, "name", i.name))
            student.appendChild(create_field(DOMTree, "course", i.course))
            student.appendChild(create_field(DOMTree, "group", i.group))
            student.appendChild(create_field(DOMTree, "total", i.total))
            student.appendChild(create_field(DOMTree, "done", i.done))
            student.appendChild(create_field(DOMTree, "language", i.language))
            student.appendChild(create_field(DOMTree, "not_done", i.not_done))
            registry.appendChild(student)
        DOMTree.appendChild(registry)
        DOMTree.writexml(xml_file, addindent='\t', newl='\n', encoding="UTF-8")