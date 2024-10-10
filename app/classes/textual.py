from textual.widgets import ListView, ListItem, Label, Tree, TextArea, Input, TabPane
from textual.containers import Horizontal
import random

class InboxList(ListView):
    BINDINGS = [
        ("a", "app.add_task_to_inbox", "add to inbox"),
        ("d", "app.delete_highlighted_task", "delete highlighted"),
        ("e", "app.edit_inbox_element", "edit inbox element")
    ]

    def refresh_items(self, data):
        self.clear()
        for list_item_text in data:
            list_item = ListItem(Label(list_item_text))
            self.append(list_item)


class ReviewList(ListView):
    def show_random_item(self, data):
        self.clear()

        random_inbox_item_index = random.randrange(0, len(data))
        random_inbox_item_text = data[random_inbox_item_index]
        random_inbox_element =  ListItem(Label(random_inbox_item_text))

        self.append(random_inbox_element)


class ButtonsContainer(Horizontal):
    pass


class HorizontalContainer(Horizontal):
    pass


class NotesTree(Tree):
    BINDINGS = [
        ("a", "app.add_note_to_tree", "add note"),
        ("d", "app.delete_highlighted_note", "delete highlighted note")
    ]

    def refresh_notes(self, notes_data):
        self.clear()
        for note in notes_data:
            id, name, content = note.values()
            self.root.add_leaf(
                label=name,
                data={"id": id}
            )


class NotesTextArea(TextArea):
    pass


class InboxInput(Input):
    pass


class NotesInput(Input):
    pass
