from textual import events, on
from textual.app import App, ComposeResult
from textual.widgets import *
from textual.containers import *

from classes.textual import *
from classes.jsondata import JsonData


class EndoTree(App):
    # INIT
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        ("a", "add_task_to_inbox", "add to input"),
        ("d", "delete_highlighted_task", "delete highlighted"),
        ("e", "edit_inbox_element", "edit inbox element")
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="notes_tab"):
            with TabPane("Przegląd", id="review_tab", disabled=True):
                yield Label("Automatycznie wylosowany element listy inbox:")
                yield ReviewList(id="review-list")
                yield ButtonsContainer(
                    Select(
                        name="Hello?",
                        options=[
                            ("Ważne i pilne", ""),
                            ("Ważne i niepilne", ""),
                            ("Nieważne i pilne", ""),
                            ("Nieważne i niepilne", "")
                        ]
                    ),
                    Button("Dodaj do listy"),
                    Button("Dodaj do projektu"),
                    Button("Dodaj do przemyśleń"),
                    Button("Usuń"),
                )

            with TabPane("Nieprzetworzone zadania", id="inbox_tab"):
                    yield InboxInput(
                        placeholder="Co chcesz dodać?",
                        id="inbox-input"
                    )
                    yield InboxList(id="inbox-list")

            with TabPane("Projekty", id="projects_tab", disabled=True):
                pass

            with TabPane("Notatki", id="notes_tab"):
                yield NotesInput(
                    placeholder="Co chcesz dodać?",
                    id="notes-input"
                )
                yield HorizontalContainer(
                    NotesTree("Notatki", id="notes-tree", data={}),
                    NotesTextArea(id="notes-textarea")
                )

        yield Footer()


    # PROPERTIES
    @property
    def inbox_input(self) -> InboxInput:
        return self.query_one("#inbox-input", InboxInput)

    @property
    def notes_input(self) -> NotesInput:
        return self.query_one("#notes-input", NotesInput)

    @property
    def inbox_list(self) -> InboxList:
        return self.query_one("#inbox-list", InboxList)

    @property
    def review_list(self) -> ReviewList:
        return self.query_one("#review-list", ReviewList)

    @property
    def notes_tree(self) -> NotesTree:
        return self.query_one("#notes-tree", NotesTree)

    @property
    def notes_textarea(self) -> NotesTextArea:
        return self.query_one("#notes-textarea", NotesTextArea)


    # ON'S
    @on(events.Mount)
    def initialize_app_data(self):
        self.data = JsonData(path="data.json")
        self.inbox_item_being_edited = None

    @on(events.Mount)
    def expand_notes_tree(self):
        self.notes_tree.root.expand()

    @on(events.Key)
    def quit_app(self, event: events.Key):
        if event.key == "escape": quit()

    @on(InboxInput.Submitted)
    def handle_inbox_input_submit(self):
        if self.inbox_input.value == "": return

        self.data.data["inbox"].append(self.inbox_input.value)
        self.data.save()

        self.inbox_input.clear()
        self.inbox_list.refresh_items(self.data.data["inbox"])

    @on(NotesInput.Submitted)
    def handle_notes_input_submit(self):
        if self.notes_input.value == "": return

        new_note_index = max(note["id"] for note in self.data.data["notes"]) + 1
        new_note = {
            "id": new_note_index,
            "name": self.notes_input.value,
            "content": ""
        }

        self.data.data["notes"].append(new_note)
        self.data.save()

        self.notes_input.clear()
        self.notes_tree.refresh_notes(self.data.data["notes"])


    @on(TabbedContent.TabActivated)
    def switch_tabs(self, event: TabbedContent.TabActivated):
        match event.pane.id:
            case "inbox_tab":
                self.inbox_list.refresh_items(self.data.data["inbox"])
            case "review_tab":
                self.review_list.show_random_item(self.data.data["inbox"])
            case "projects_tab":
                pass
            case "notes_tab":
                self.notes_tree.refresh_notes(self.data.data["notes"])

    @on(NotesTree.NodeSelected)
    def update_textarea_content(self, event: NotesTree.NodeSelected):
        if event.node.data.get("id") is not None:
            note_id = event.node.data["id"]
            note_content = self.data.data["notes"][note_id]["content"]
            self.notes_textarea.text = note_content

    @on(NotesTextArea.SelectionChanged)
    def update_note_content(self, event: TextArea.SelectionChanged):
        current_node = self.notes_tree.cursor_node
        if current_node is not None:
            note_id = current_node.data["id"]
            self.data.data["notes"][note_id]["content"] = self.notes_textarea.text

            self.data.save()


    # ACTION'S
    def action_add_task_to_inbox(self):
        self.inbox_input.focus()
        highlighted_item = self.inbox_list.highlighted_child

        if highlighted_item is not None:
            highlighted_item.highlighted = False

    def action_delete_highlighted_task(self):
        if self.inbox_list.highlighted_child is None: return

        highlighted_item_index = self.inbox_list.index
        self.data.data["inbox"].pop(highlighted_item_index)
        self.data.save()

        self.inbox_list.refresh_items(self.data.data["inbox"])

    def action_edit_inbox_element(self):
        if self.inbox_list.highlighted_child is None: return

        highlighted_item_index = self.inbox_list.index

        text = self.data.data["inbox"][highlighted_item_index]
        self.inbox_input.value = text

        self.data.data["inbox"].pop(highlighted_item_index)
        self.inbox_list.highlighted_child.remove()

        self.inbox_input.focus()

        self.inbox_item_being_edited = highlighted_item_index

    def action_quit(self):
        quit()


if __name__ == "__main__":
    app = EndoTree()
    app.run()
