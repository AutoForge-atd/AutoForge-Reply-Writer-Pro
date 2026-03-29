import tkinter as tk
from gui import ReplyWriterProGUI


def main():
    root = tk.Tk()
    app = ReplyWriterProGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()