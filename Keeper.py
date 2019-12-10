import webbrowser
from tkinter import *

import pickle


# Classes:

# Keeper - keeps all the information that is used by the app
class Keeper:
    # Default window size when there are no bookmarks
    hight = 275

    width = 320

    # First button row (used to place the buttons, each new button below it's predeccor)
    button_row = 1

    # Used only if there are default buttons added for testing
    i = 0

    # The actual window size
    size = '%sx%s' % (width, hight)

    # All currently existing bookmarks
    bookmarks = []

    buttons = []

    # Entries used to receive input in "Add Bookmark" , "Remove Bookmark" and "Highlight Bookmark" windows.
    entry_1 = ""
    entry_2 = ""
    tkvar_1 = ""

    # "root" - tkinter object expected.
    def __init__(self, hight, width, root):
        self.hight = hight
        self.width = width
        self.root = root

    # Opens a new browser window, using the URL provided
    def go_to(self, path):
        print("Going to: " + path)
        webbrowser.open_new(path)

    # Add new bookmark - "Confirm" clicked
    def handle_confirm(self, window, root):
        name = self.entry_1.get()
        url = self.entry_2.get()
        print("Name: {name}, URL: {url}".format(name=name, url=url))
        self.add_new_bookmark(name, url)
        self.add_last_bookmark(root)
        self.increase(root)
        self.close_window(window)

    # Remove a bookmark - "Confirm" clicked
    def handle_cancel(self, window, root):
        bookmark_to_remove = self.tkvar_1.get()
        print("To remove: " + bookmark_to_remove)
        result_list = []

        for button in self.buttons:
            if button["text"] == bookmark_to_remove:
                button.config(state=DISABLED)
                # button.config(bg="black",fg="red")

        for bookmark in self.bookmarks:
            if bookmark.name != bookmark_to_remove:
                result_list.append(bookmark)
        self.bookmarks = result_list
        window.destroy()
        self.save_bookmarks("book.txt", root, 1)

    # Highlight a bookmark - "Confirm" clicked
    def highlight_bookmark(self, window, root):
        bookmark_to_highlight = self.tkvar_1.get()
        print("Highlight: " + bookmark_to_highlight)
        result_list = []

        for button in self.buttons:
            if button["text"] == bookmark_to_highlight:
                button.config(bg="black", fg="red")

        for bookmark in self.bookmarks:
            if bookmark.name == bookmark_to_highlight:
                bookmark.highlighted = 1
            result_list.append(bookmark)

        self.bookmarks = result_list
        window.destroy()
        self.save_bookmarks("book.txt", root, 1)

    # Close provided window
    def close_window(self, window):
        window.destroy()

    ##Put all existing bookmarks on screen
    def add_all_bookmarks(self, root):
        for bookmark in self.bookmarks:
            path = bookmark.url
            nav_button = Button(root, text=bookmark.name, command=lambda path=path: self.go_to(path), width=20)
            nav_button.grid(row=self.button_row + self.i, column=0, padx=12, pady=5)

            # If the button (bookmark) was previously highlighted
            if bookmark.highlighted == 1:
                nav_button.config(bg="black", fg="red")

            self.buttons.append(nav_button)
            self.increase(root)
            self.i += 1

    ##Put the last added bookmark on screen
    def add_last_bookmark(self, root):
        last = len(self.bookmarks) - 1
        print("Last: " + str(last))
        nav_button = Button(root, text=self.bookmarks[last].name, command=lambda: self.go_to(self.bookmarks[last].url),
                            width=20)
        nav_button.grid(row=self.button_row + self.i, column=0, padx=12, pady=5)
        self.buttons.append(nav_button)
        self.i += 1

    # Save all bookmarks to file
    def save_bookmarks(self, file_name, window, close=None):
        with open(file_name, "wb") as output:
            pickle.dump(self.bookmarks, output, pickle.HIGHEST_PROTOCOL)
            print("Logs: Saving content")
            output.flush()
            output.close()
            if close is None:
                window.destroy()

    # Load all existing bookmarks from a file
    def load_bookmarks(self, file_name):
        try:
            with open(file_name, "rb") as input:
                result = pickle.load(input)
                self.bookmarks = result

        # Creating the file from scratch if not exists.
        except FileNotFoundError:
            print("Log: Error - storage file doesn't exists, creating from scratch.")
            open(file_name, "w+")
            self.load_bookmarks(file_name)


    # Add new bookmark
    def add_new_bookmark(self, name, url):
        new_bookmark = Bookmark(name, url)
        self.bookmarks.append(new_bookmark)

    # Increases the window high by 30
    def increase(self, root):
        self.hight += 30
        self.size = '%sx%s' % (self.width, self.hight)
        print(self.size)
        root.geometry(self.size)

    ############################## New Bookmark Window #####################################

    # Opens the "New Bookmark" window with two buttons and two enteries.
    # User input provided here is handled in "handle_confirm".
    def add_new_boomark_window(self):
        secondary = Tk()
        secondary.geometry("550x100")

        label_1 = Label(secondary, text="Enter name:", fg="blue", font=("", 11))
        self.entry_1 = Entry(secondary, width="70")

        label_2 = Label(secondary, text="Enter URL: ", fg="blue", font=("", 11))
        self.entry_2 = Entry(secondary, width="70")

        confirm_button = Button(secondary, text="Confirm", command=lambda: self.handle_confirm(secondary, self.root),
                                width=20, bg="blue",
                                fg="white")
        cancel_button = Button(secondary, text="Cancel", command=lambda: self.close_window(secondary), width=20,
                               bg="red", fg="white")

        label_1.grid(row=0, column=0, sticky=E)
        self.entry_1.grid(row=0, column=1)

        label_2.grid(row=1, column=0, sticky=E)
        self.entry_2.grid(row=1, column=1)

        confirm_button.grid(row=3, column=1, pady=6, sticky=W)
        cancel_button.grid(row=3, column=1, pady=6, sticky=E)

        secondary.mainloop()

    ############################## Delete Bookmark Window #####################################
    # Opens the "Remove Bookmark" window with two buttons and drop down menu.
    # User input provided here is handled in "handle_cancel".
    def remove_bookmark_window(self):
        tertiary = Tk()
        tertiary.geometry("550x100")

        label_1 = Label(tertiary, text="Enter name:", fg="blue", font=("", 11))
        # self.entry_1 = Entry(tertiary, width="70")

        label_1.grid(row=0, column=0, pady=6, sticky=E)
        # self.entry_1.grid(row=0, column=1, pady=6)

        confirm_button = Button(tertiary, text="Confirm", command=lambda: self.handle_cancel(tertiary, self.root),
                                width=20, bg="blue",
                                fg="white")
        cancel_button = Button(tertiary, text="Cancel", command=lambda: self.close_window(tertiary), width=20,
                               bg="red", fg="white")

        confirm_button.grid(row=3, column=3, pady=6, padx=90, sticky=W)
        cancel_button.grid(row=3, column=1, pady=6, sticky=E)

        ############### Drop Down ############

        options = []

        for bookmark in self.bookmarks:
            options.append(bookmark.name)

        self.tkvar_1 = StringVar(tertiary)

        menu = OptionMenu(tertiary, self.tkvar_1, *options)
        menu.config(width=50)
        menu.grid(row=0, column=0, pady=6)
        menu.grid(columnspan=4)

        tertiary.mainloop()

    ############################## Delete Bookmark Window - END #########################################
    ############################# Highligh Bookmark Window #####################################
    # Opens the "Highlight Bookmark" window with two buttons and drop down menu.
    # The selected bookmark is highlighted. User input provided here is handled in "handle_cancel".
    def highlight_bookmark_window(self):
        tertiary = Tk()
        tertiary.geometry("550x100")

        label_1 = Label(tertiary, text="Enter name:", fg="blue", font=("", 11))
        # self.entry_1 = Entry(tertiary, width="70")

        label_1.grid(row=0, column=0, pady=6, sticky=E)
        # self.entry_1.grid(row=0, column=1, pady=6)

        confirm_button = Button(tertiary, text="Confirm", command=lambda: self.highlight_bookmark(tertiary, self.root),
                                width=20, bg="blue",
                                fg="white")
        cancel_button = Button(tertiary, text="Cancel", width=20, command=lambda: self.close_window(tertiary),
                               bg="red", fg="white")

        confirm_button.grid(row=3, column=3, pady=6, padx=90, sticky=W)
        cancel_button.grid(row=3, column=1, pady=6, sticky=E)

        ############### Drop Down ############

        options = []

        for bookmark in self.bookmarks:
            options.append(bookmark.name)

        self.tkvar_1 = StringVar(tertiary)

        menu = OptionMenu(tertiary, self.tkvar_1, *options)
        menu.config(width=50)
        menu.grid(row=0, column=0, pady=6)
        menu.grid(columnspan=4)

        tertiary.mainloop()


# Bookmark class
class Bookmark:
    name = ""
    url = ""
    highlighted = 0

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return f"{self.url}"