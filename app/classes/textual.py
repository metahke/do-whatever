from textual.widgets import ListView, ListItem, Label, Tree, TextArea
from textual.containers import Horizontal

class InboxList(ListView):
    def refresh_items(self, data):
        for list_item_text in data["inbox"]:
            list_item = ListItem(Label(list_item_text))
            self.append(list_item)


class ButtonsContainer(Horizontal):
    pass


class HorizontalContainer(Horizontal):
    pass


class NotesTree(Tree):
    pass


class NotesTextArea(TextArea):
    pass
