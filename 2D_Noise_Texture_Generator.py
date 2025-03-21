import tkinter as tk

from editor.editor import NoiseGeneratorApp

if __name__ == "__main__":
    root = tk.Tk()
    app = NoiseGeneratorApp(root)
    root.mainloop()