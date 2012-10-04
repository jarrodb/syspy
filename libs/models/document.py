from mongokit import Document as MongoDocument

class Document(MongoDocument):

    def choice_title_from_id(self, choices, cid):
        for i, t, s in choices:
            if isinstance(i, int):
                cid = int(cid)
            else:
                cid = str(cid)

            if i == cid:
                return t

        raise ValueError('Invalid Choice ID')

    def choice_id_from_shortname(self, choices, shortname):
        for i, t, s in choices:
            if s.lower() == shortname.lower():
                return i

    def choice_id_from_title(self, choices, title):
        for i, c, s in choices:
            if c.lower() == title.lower():
                return i

