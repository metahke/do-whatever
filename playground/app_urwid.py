import urwid

# Define the menu options
menu_options = [
    ('Option 1', 'You selected Option 1'),
    ('Option 2', 'You selected Option 2'),
    ('Option 3', 'You selected Option 3'),
    ('Quit', 'Exiting the application...')
]

# Create a class for the Menu
class Menu:
    def __init__(self, options):
        self.options = options
        self.selected = 0
        self.body = urwid.SimpleListWalker(self._create_list())

        # Create a ListBox for the menu
        self.listbox = urwid.ListBox(self.body)
        self.loop = urwid.MainLoop(self.listbox, unhandled_input=self._input)

    def _create_list(self):
        # Create a list of MenuItems
        return [urwid.Button(label, on_press=self._select, user_data=index) for index, (label, _) in enumerate(self.options)]

    def _select(self, button, user_data):
        self.selected = user_data
        response = self.options[self.selected][1]
        self._show_response(response)

    def _show_response(self, response):
        # Clear the current list and show the response
        self.body.clear()
        self.body.append(urwid.Text(response))
        self.body.append(urwid.Button('Back', on_press=self._back))

    def _back(self, button):
        # Go back to the menu
        self.body.clear()
        self.body.extend(self._create_list())

    def _input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def run(self):
        self.loop.run()

# Instantiate and run the menu
if __name__ == '__main__':
    menu = Menu(menu_options)
    menu.run()
