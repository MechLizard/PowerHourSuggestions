class Suggestion:
    def __init__(self, id: int, username: str):
        self.id = None
        self.username = None
        self.url = None
        self.comment = None


    # TODO: Can these be removed?
    def set_url(self, url: str):
        self.url = url

    def set_comment(self, comment):
        self.comment = comment

