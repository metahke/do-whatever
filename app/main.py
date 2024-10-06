from textual.app import App, ComposeResult
from textual import events, on
from textual.containers import Horizontal, ScrollableContainer, Container, Vertical
from textual.widgets import *
import json, random


class JsonData():
    def __init__(self, path):
        self.path = path
        self.data = self.load()

    def load(self):
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save(self):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def get(self, key):
        return self.data[key]

    def update(self, key, content):
       self.data[key] = content


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
                yield Input(
                    placeholder="Co chcesz dodać?",
                    id="add-project-input"
                )
                yield HorizontalContainer(
                    Tree("Projekty", id="projects-tree"),
                    TextArea(id="projects-textarea")
                )

        yield Footer()


    # ON'S
    def on_mount(self) -> None:
        # może lepiej dodać to w konstruktorze
        self.data = JsonData(path="data.json")

        self.query_one("#tasks-list", InboxList).refresh_items(self.data.data)

        # sekcja projekty
        self.query_one("#projects-tree", Tree).root.expand()

        for project in self.data.data["projects"]:
            id, name, content = project.values()
            self.query_one("#projects-tree", Tree).root.add_leaf(
                label=name
            )

    def on_key(self, event: events.Key):
        if event.key == "escape":
            quit()

    # Może dekorator zapisujący data do pliku po wykonaniu akcji
    def on_input_submitted(self, input_submitted: Input.Submitted):
        if not input_submitted.value: return

        input_widget= input_submitted.input

        if input_widget.id == "add-to-inbox-input":
            new_label = ListItem(Label(input_submitted.value))

            self.data.data["inbox"].append(input_submitted.value)
            self.data.save()

            self.query_one("#tasks-list", ListView).append(new_label)
            input_widget.clear()

    @on(TabbedContent.TabActivated)
    def display_inbox_item(self, event: TabbedContent.TabActivated):
        if event.pane.id == "review":
            self.query_one("#random-inbox-items", ListView).clear()

            random_inbox_item_index = random.randrange(0, len(self.data.data["inbox"]))
            random_inbox_item_text = self.data.data["inbox"][random_inbox_item_index]
            random_inbox_element =  ListItem(Label(random_inbox_item_text))

            self.query_one("#random-inbox-items", ListView).append(random_inbox_element)

    def on_tree_node_selected(self, event: Tree.NodeSelected):
        # HERE WE GO
        text = self.data.data[event.node.id - 1]
        self.query_one("#projects-textarea", TextArea).text = text

    def on_textarea_selection_changed(self, event: TextArea.SelectionChanged):
        current_node = self.query_one("#projects-tree", Tree).cursor_node
        if current_node is not None:
            current_node.data = self.data.data[current_node.id - 1]


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
            self.data.data["inbox"].pop(highlighted_item_index)
            self.data.save()


if __name__ == "__main__":
    app = EndoTree()
    app.run()
