import tkinter as tk
import os


class PyToDo(tk.Frame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        parent.title("PyToDo")
        parent.geometry("400x600")
        parent.config(bg="#1f2428")

        self.entry_string = tk.StringVar()
        self.entry = tk.Entry(
            self.parent, textvariable=self.entry_string, bg="#2B3036", fg='#ffffff', font="Ubuntu 11")
        self.entry.bind("<Return>", self.enter)
        self.entry.grid(row=0, column=0, sticky="new", padx=10, pady=20)

        label_text1 = tk.StringVar()
        label_text1.set("To Do:")
        self.todolabel = tk.Label(parent, textvariable=label_text1,
                                  bg="#1f2428", fg='#ffffff', padx=10, pady=3, anchor="w", font="Ubuntu 11 bold")
        self.todolabel.grid(row=1, column=0, sticky="ew")

        self.tasks = []
        self.taskframe = tk.Frame(parent, bg="#1f2428")
        self.taskframe.grid(row=2, column=0, sticky="new", padx=10, pady=5)

        parent.grid_columnconfigure(0, weight=1)

        if os.path.exists("tdlist"):
            with open("tdlist", "r") as f:
                for line in f:
                    self.add_task(self.taskframe, line.strip())

    def enter(self, event):
        self.add_task(self.taskframe, self.entry_string.get())
        self.entry.delete(0, "end")

    def add_task(self, frame, text):
        tframe = tk.Frame(frame, bg="#1f2428")

        label_text = tk.StringVar()
        label_text.set("• " + text)
        task = tk.Label(tframe, borderwidth=2, relief="ridge", textvariable=label_text,
                        bg="#2B3036", fg='#ffffff', padx=10, pady=3, anchor="w", font="Ubuntu 11")
        self.tasks.append(task)
        task.grid(row=0, column=0, sticky="nsew")

        button_cross = tk.Button(
            tframe, text="✓", command=lambda: self.cross_task(button_cross, label_text), bg="#2B3036", fg='#ffffff', font="Ubuntu 11")
        button_cross.grid(row=0, column=5, sticky=tk.E)

        button_remove = tk.Button(
            tframe, text="-", command=lambda: self.remove_task(tframe, task), bg="#2B3036", fg='#ffffff', font="Ubuntu 11")
        button_remove.grid(row=0, column=6, sticky=tk.E)

        tframe.grid_rowconfigure(0, weight=1)
        tframe.grid_columnconfigure(0, weight=1)

        tframe.pack(fill=tk.BOTH)

    def cross_task(self, button, label_text):
        label_text.set(self.strike(label_text.get()))
        button.destroy()

    def remove_task(self, frame, task):
        self.tasks.remove(task)
        frame.destroy()

    def strike(self, text):
        res = ''
        for char in text:
            res += char + '\u0336'
        return res

    def on_close(self):
        with open("tdlist", "w") as f:
            for task in self.tasks:
                f.write(task.cget("text")[2:]+"\n")
        self.parent.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    main = PyToDo(root)
    root.protocol("WM_DELETE_WINDOW", main.on_close)
    root.mainloop()
