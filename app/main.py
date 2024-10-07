from textual.app import App, ComposeResult
from textual import events, on
from textual.containers import *
from textual.widgets import *
from classes.textual import *
from classes.jsondata import JsonData
import random


class EndoTree(App):
    # INIT
    CSS_PATH = "styles.tcss"
    BINDINGS= [
        ("a", "add_task_to_inbox", "Display input"),
        ("d", "delete_highlighted_task", "Delete highlighted task")
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="inbox_tab"):
            with TabPane("Przegląd", id="review_tab", disabled=True):
                yield Label("Automatycznie wylosowany element listy inbox:")
                yield ListView(id="review-list")
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
                    yield Input(
                        placeholder="Co chcesz dodać?",
                        id="inbox-input"
                    )
                    yield InboxList(id="inbox-list")

            with TabPane("Projekty", id="projects_tab", disabled=True):
                pass

            with TabPane("Notatki", id="notes_tab"):
                yield Input(
                    placeholder="Co chcesz dodać?",
                    id="notes-input"
                )
                yield HorizontalContainer(
                    NotesTree("Notatki", id="notes-tree"),
                    NotesTextArea(id="notes-textarea")
                )

        yield Footer()


    # PROPERTIES
    @property
    def inbox_input(self) -> Input:
        return self.query_one("#inbox-input", Input)

    @property
    def inbox_list(self) -> InboxList:
        return self.query_one("#inbox-list", InboxList)

    @property
    def review_list(self) -> ListView:
        return self.query_one("#review-list", ListView)

    @property
    def notes_tree(self) -> NotesTree:
        return self.query_one("#notes-tree", NotesTree)

    @property
    def notes_textarea(self) -> NotesTextArea:
        return self.query_one("#notes-textarea", NotesTextArea)


    # ON'S
    def on_mount(self) -> None:
        # INIT
        self.data = JsonData(path="data.json")

        # INBOX_TAB
        self.inbox_list.refresh_items(self.data.data)

        # REVIEW_TAB


        # PROJECTS_TAB


        # NOTES_TAB
        self.notes_tree.root.expand()

        for note in self.data.data["notes"]:
            id, name, content = note.values()
            self.notes_tree.root.add_leaf(
                label=name,
                data={"id": id}
            )

    def on_key(self, event: events.Key):
        if event.key == "escape": quit()

    def on_input_submitted(self, event: Input.Submitted):
        if not event.input.value: return

        match event.input.id:
            case "inbox-input":
                self.handle_inbox_input_submit(event.input.value)

    @on(TabbedContent.TabActivated)
    def switch_tabs(self, event: TabbedContent.TabActivated):
        match event.pane.id:
            case "inbox_tab":
                pass
            case "review_tab":
                self.handle_review_tab_activation()
            case "projects_tab":
                pass
            case "notes_tab":
                pass

    @on(NotesTree.NodeSelected)
    def update_textarea_content(self, event: NotesTree.NodeSelected):
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
        if highlighted_item is not None: highlighted_item.highlighted = False

    def action_delete_highlighted_task(self):
        highlighted_item = self.inbox_list.highlighted_child

        if highlighted_item is not None:
            highlighted_item.remove()
            highlighted_item_index = self.inbox_list.index

            self.data.data["inbox"].pop(highlighted_item_index)
            self.data.save()


    # HANDLERS
    def handle_review_tab_activation(self):
        self.review_list.clear()

        random_inbox_item_index = random.randrange(0, len(self.data.data["inbox"]))
        random_inbox_item_text = self.data.data["inbox"][random_inbox_item_index]
        random_inbox_element =  ListItem(Label(random_inbox_item_text))

        self.review_list.append(random_inbox_element)

    def handle_inbox_input_submit(self, value):
        # get_value()
        # save_value()
        # list_value()
        new_label = ListItem(Label(value))

        self.data.data["inbox"].append(value)
        self.data.save()

        self.inbox_list.append(new_label)
        self.inbox_input.clear()


if __name__ == "__main__":
    app = EndoTree()
    app.run()
