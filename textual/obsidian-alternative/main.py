from textual.app import App, ComposeResult
from textual import events, on
from textual.containers import Horizontal, ScrollableContainer, Container, Vertical
from textual.widgets import *
import json, random


class JsonData():
    @staticmethod
    def load(path):
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def save(path, data):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


class InboxList(ListView):
    def refresh_items(self, data):
        for list_item_text in data["inbox"]:
            list_item = ListItem(Label(list_item_text))
            self.append(list_item)


class ButtonsContainer(Horizontal):
    pass


class HorizontalContainer(Horizontal):
    pass


class EndoTree(App):
    CSS_PATH = "styles.tcss"

    # BINDINGS_TYPE = {
    #     "inbox": [
    #         ("a", "add_task_to_inbox", "Display input"),
    #         ("d", "delete_highlighted_task", "Delete highlighted task")
    #     ],
    #     "review": []
    # }

    BINDINGS= [
        ("a", "add_task_to_inbox", "Display input"),
        ("d", "delete_highlighted_task", "Delete highlighted task")
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="projects"):
            with TabPane("Nieprzetworzone zadania", id="inbox"):
                yield Input(
                    placeholder="Co chcesz dodać?",
                    id="add-to-inbox-input"
                )
                yield InboxList(id="tasks-list")

            with TabPane("Przegląd", id="review", disabled=True):
                yield Label("Automatycznie wylosowany element listy inbox:")
                yield ListView(id="random-inbox-items")
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
                    Button("Dodaj do listy", classes=""),
                    Button("Dodaj do projektu", classes=""),
                    Button("Dodaj do przemyśleń", classes=""),
                    Button("Usuń", classes=""),
                )

            with TabPane("Projekty", id="projects"):
                tree = Tree("Projekty")
                tree.root.expand()
                tree.root.add_leaf("Posprzątać kuchnię")
                tree.root.add_leaf("Stworzyć alternatywę dla Obisidana")
                tree.root.add_leaf("Pójść na zakupy")

                yield Input(
                    placeholder="Co chcesz dodać?",
                    id="add-project-input"
                )
                yield HorizontalContainer(
                    tree,
                    TextArea("Hello world")
                )

        yield Footer()


    # ON'S
    def on_mount(self) -> None:
        # może lepiej dodać to w konstruktorze
        self.data = JsonData.load(path="data.json")

        self.query_one("#tasks-list", InboxList).refresh_items(self.data)

    def on_key(self, event: events.Key):
        if event.key == "escape":
            quit()


    # Może dekorator zapisujący data do pliku po wykonaniu akcji
    def on_input_submitted(self, input_submitted: Input.Submitted):
        if not input_submitted.value: return

        input_widget= input_submitted.input

        if input_widget.id == "add-to-inbox-input":
            new_label = ListItem(Label(input_submitted.value))

            self.data["inbox"].append(input_submitted.value)
            JsonData.save(path="data.json", data=self.data)

            self.query_one("#tasks-list", ListView).append(new_label)
            input_widget.clear()

    @on(TabbedContent.TabActivated)
    def display_inbox_item(self, event: TabbedContent.TabActivated):
        if event.pane.id == "review":
            self.query_one("#random-inbox-items", ListView).clear()

            random_inbox_item_index = random.randrange(0, len(self.data["inbox"]))
            random_inbox_item_text = self.data["inbox"][random_inbox_item_index]
            random_inbox_element =  ListItem(Label(random_inbox_item_text))

            self.query_one("#random-inbox-items", ListView).append(random_inbox_element)


    # ACTION'S
    def action_add_task_to_inbox(self):
        self.query_one("#add-to-inbox-input").focus()

        list_items = self.query_one("#tasks-list", ListView)
        highlighted_item = list_items.highlighted_child

        if highlighted_item is not None: highlighted_item.highlighted = False

    def action_delete_highlighted_task(self):
        list_items = self.query_one("#tasks-list", ListView)
        highlighted_item = list_items.highlighted_child

        if highlighted_item is not None:
            highlighted_item.remove()

            highlighted_item_index = list_items.index
            self.data["inbox"].pop(highlighted_item_index)
            JsonData.save(path="data.json", data=self.data)


if __name__ == "__main__":
    app = EndoTree()
    app.run()
