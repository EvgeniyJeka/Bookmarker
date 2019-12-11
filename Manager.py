
from tkinter import *
from Keeper import Keeper


class Manager:

    def __init__(self):
        # Sanity + Before
        self.root = Tk()

        # Instances
        dragon = Keeper(250, 320, self.root)

        # Creating new window with the required size.
        self.root.geometry(dragon.size)

        # Placing the command buttons.
        self.place_buttons(self.root, dragon)

        try:
            # Loading the bookmarks from storage file
            dragon.load_bookmarks("book.txt")
        except EOFError:
            print("log: Warning - storage file is empty. No bookmarks to load.")

        print(f"Log: Currently saved bookmarks: {dragon.bookmarks}")

        dragon.add_all_bookmarks(dragon.root)

        self.root.mainloop()

    # Place the command buttons
    def place_buttons(self, root, keeper_object):

        # Increase window heigh (test
        add_button = Button(root, text="Add Height", command=lambda: keeper_object.increase(root), width=20)
        add_button.grid(row=0, column=0, padx=12, pady=2)

        # Add new bookmark (hardcoded)
        new_button = Button(root, text="Add New Bookmark", command=lambda: keeper_object.add_new_boomark_window(), width=15, height=3, bg="blue", fg="white")
        new_button.grid(row=2, column=1, padx=10, pady=2)
        new_button.grid(rowspan=2)

        # Save all bookmarks and close
        save_button = Button(root, text="Save & Exit", command=lambda: keeper_object.save_bookmarks("book.txt", root), width=15, height=3, bg="#00B395", fg="white")
        save_button.grid(row=0, column=1, padx=10, pady=5)
        save_button.grid(rowspan=2)

        # Remove an existing bookmark
        remove_button = Button(root, text="Remove bookmark", command=lambda: keeper_object.remove_bookmark_window(), width=15, height=3, bg="silver", fg="white")
        remove_button.grid(row=4, column=1, padx=10, pady=5)
        remove_button.grid(rowspan=2)

        # Highlight one of the bookmarks
        highlight_button = Button(root, text="Highlight Bookmark", command=lambda: keeper_object.highlight_bookmark_window(), width=15,height=3, bg="red", fg="white")
        highlight_button.grid(row=6, column=1, padx=10, pady=5)
        highlight_button.grid(rowspan=2)

