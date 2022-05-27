import utils.parser as parser

available_language = parser.available_language

class Context:
    def __init__(self, path: str='') -> None:
        if path == '':
            self.content = list()
        else:
            self.content = parser.parse_file(path)


    def add_to_context(self, name: str, course: str, group: str, total: str, done: str, language: str, not_done: str):
        self.content.append(parser.Student(name, course, group, total, done, language, not_done))
        available_language.add(language)


    def delete_from_context(self, key: str, info: str) -> int:
        tag_name = ''
        if key == 'Имя':
            tag_name = 'name'
        elif key == 'Курс':
            tag_name = 'course'
        elif key == 'Группа':
            tag_name = 'group'
        elif key == 'Общее число работ':
            tag_name = 'total'
        elif key == 'Количество выполненных работ':
            tag_name = 'done'
        elif key == 'Язык программирования':
            tag_name = 'language'
        elif key == 'Количество не выполненных работ':
            tag_name = 'not_done'
        to_remove = []
        language_counter = 0
        for i in self.content:
            if key == 'Язык программирования' and i.language == info:
                language_counter += 1
            if i.__dict__[tag_name] == info:
                to_remove.append(i)
        for i in to_remove:
            self.content.remove(i)
        if key == 'Язык программирования' and language_counter == 0:
            available_language.remove(info)
        return len(to_remove)


    def save_context(self, path: str):
        parser.write_to_xml(self.content, path)


    def find_in_context(self, key: str, info: str) -> list[parser.Student]:
        tag_name = ''
        if key == 'Имя':
            tag_name = 'name'
        elif key == 'Курс':
            tag_name = 'course'
        elif key == 'Группа':
            tag_name = 'group'
        elif key == 'Общее число работ':
            tag_name = 'total'
        elif key == 'Количество выполненных работ':
            tag_name = 'done'
        elif key == 'Язык программирования':
            tag_name = 'language'
        elif key == 'Количество не выполненных работ':
            tag_name = 'not_done'
        found = []
        for i in self.content:
            if i.__dict__[tag_name] == info:
                found.append(i)
        return found
    pass