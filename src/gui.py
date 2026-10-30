
import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class ShellGUI:

    def __init__(self, shell, script_path=None):
        self.shell = shell
        self.window = tk.Tk()
        self.window.title(
            f"Эмулятор - [{self.shell.prompt().split(':')[0]}]"
        )
        self.window.geometry("850x560")
        self.output = ScrolledText(
            self.window, bg="#151515", fg="#eeeeee",
            insertbackground="white", font=("Courier New", 11),
            state="disabled", wrap="word"
        )
        self.output.pack(fill="both", expand=True, padx=8, pady=8)
        self.entry = tk.Entry(
            self.window, bg="#222222", fg="white",
            insertbackground="white", font=("Courier New", 11)
        )
        self.entry.pack(fill="x", padx=8, pady=(0, 8))
        self.entry.bind("<Return>", self._submit)
        self.entry.focus_set()

        self._write("Эмулятор командной оболочки запущен.")
        self._write("Доступные команды: ls, cd, cal, tree, who, cp, exit")
        self._write("Введите команду в нижнее поле и нажмите Enter.")
        self._write("")
        self._write(self.shell.prompt())

        if script_path:
            self._run_script(script_path)

    def _write(self, text):
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        self.output.see("end")
        self.output.configure(state="disabled")

    def _submit(self, event=None):
        line = self.entry.get()
        self.entry.delete(0, "end")
        self._run_line(line)

    def _run_line(self, line):
        self._write(f"{self.shell.prompt()} {line}")
        output, should_exit = self.shell.execute(line)
        if output:
            self._write(output)
        if should_exit:
            self.window.destroy()
        return output

    def _run_script(self, path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                for raw_line in file:
                    line = raw_line.strip()
                    if not line or line.startswith("#"):
                        continue
                    result = self._run_line(line)
                    if not self.window.winfo_exists():
                        return
                    if result.startswith("Error:"):
                        self._write("Startup script stopped after an error.")
                        return
        except OSError as error:
            self._write(f"Script error: {error}")

    def run(self):
        self.window.mainloop()
