from textual.app import App, ComposeResult
from textual import events, on
from textual.containers import *
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


class ProjectsTree(Tree):
    pass


class ProjectsTextArea(TextArea):
    pass


class EndoTree(App):
    # INIT
    CSS_PATH = "styles.tcss"
    BINDINGS= [
        ("a", "add_task_to_inbox", "Display input"),
        ("d", "delete_highlighted_task", "Delete highlighted task")
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="projects_tab"):
            with TabPane("Nieprzetworzone zadania", id="inbox_tab"):
                yield Input(
                    placeholder="Co chcesz dodać?",
                    id="inbox-input"
                )
                yield InboxList(id="inbox-list")

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

            with TabPane("Projekty", id="projects_tab"):
                yield Input(
                    placeholder="Co chcesz dodać?",
                    id="projects-input"
                )
                yield HorizontalContainer(
                    ProjectsTree("Projekty", id="projects-tree"),
                    ProjectsTextArea(id="projects-textarea")
                )

        yield Footer()


    # PROPERTIES
    @property
    def inbox_input(self):
        return self.query_one("#inbox-input", Input)

    @property
    def inbox_list(self):
        return self.query_one("#inbox-list", InboxList)

    @property
    def review_list(self):
        return self.query_one("#review-list", ListView)

    @property
    def projects_tree(self):
        return self.query_one("#projects-tree", Tree)

    @property
    def projects_textarea(self):
        return self.query_one("#projects-textarea", TextArea)


    # ON'S
    def on_mount(self) -> None:
        # INIT
        self.data = JsonData(path="data.json")

        # INBOX_TAB
        self.inbox_list.refresh_items(self.data.data)

        # REVIEW_TAB


        # PROJECTS_TAB
        self.projects_tree.root.expand()

        for project in self.data.data["projects"]:
            id, name, content = project.values()
            self.projects_tree.root.add_leaf(
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

    @on(ProjectsTree.NodeSelected)
    def update_textarea_content(self, event: ProjectsTree.NodeSelected):
        project_id = event.node.data["id"]
        project_content = self.data.data["projects"][project_id]["content"]
        self.projects_textarea.text = project_content

    @on(ProjectsTextArea.SelectionChanged)
    def update_project_content(self, event: TextArea.SelectionChanged):
        current_node = self.projects_tree.cursor_node
        if current_node is not None:
            project_id = current_node.data["id"]
            self.data.data["projects"][project_id]["content"] = self.projects_textarea.text

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
        new_label = ListItem(Label(value))

        self.data.data["inbox"].append(value)
        self.data.save()

        self.inbox_list.append(new_label)
        self.inbox_input.clear()


if __name__ == "__main__":
    app = EndoTree()
    app.run()
