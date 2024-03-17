import tkinter as tk

class SkillTask:
    def __init__(self, name, task_type):
        self.name = name
        self.task_type = task_type
        self.completed = False

class SkillTrackerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Skill Tracker")
        self.master.geometry("400x400")

        self.skills = {}
        self.tasks = []
        self.xp = 0

        self.master.configure(bg="#f0f0f0")

        self.skill_label = tk.Label(master, text="Add Skills:", bg="#f0f0f0", font=("Arial", 12))
        self.skill_label.grid(row=0, column=0, padx=10, pady=10)

        self.skill_entry = tk.Entry(master, width=20)
        self.skill_entry.grid(row=0, column=1, padx=10, pady=10)

        self.add_skill_button = tk.Button(master, text="Add Skill", command=self.add_skill, bg="#4CAF50", fg="white")
        self.add_skill_button.grid(row=0, column=2, padx=10, pady=10)

        self.task_label = tk.Label(master, text="Add Tasks:", bg="#f0f0f0", font=("Arial", 12))
        self.task_label.grid(row=1, column=0, padx=10, pady=10)

        self.task_entry = tk.Entry(master, width=20)
        self.task_entry.grid(row=1, column=1, padx=10, pady=10)

        self.task_type_label = tk.Label(master, text="Task Type:", bg="#f0f0f0", font=("Arial", 12))
        self.task_type_label.grid(row=1, column=2, padx=10, pady=10)

        self.task_type_entry = tk.Entry(master, width=20)
        self.task_type_entry.grid(row=1, column=3, padx=10, pady=10)

        self.add_task_button = tk.Button(master, text="Add Task", command=self.add_task, bg="#4CAF50", fg="white")
        self.add_task_button.grid(row=1, column=4, padx=10, pady=10)

        self.complete_task_button = tk.Button(master, text="Complete Task", command=self.complete_task, bg="#008CBA", fg="white")
        self.complete_task_button.grid(row=3, column=2, columnspan=2, padx=10, pady=10)

        self.xp_label = tk.Label(master, text="XP: 0", bg="#f0f0f0", font=("Arial", 12))
        self.xp_label.grid(row=3, column=0, padx=10, pady=10)

        self.xp_bar = tk.Canvas(master, width=200, height=20, bg="#ffffff", highlightthickness=0)
        self.xp_bar.grid(row=3, column=1, columnspan=2, padx=10, pady=10)
        self.draw_xp_bar()

        self.level_label = tk.Label(master, text="Levels:", bg="#f0f0f0", font=("Arial", 12))
        self.level_label.grid(row=4, column=0, padx=10, pady=10)

        self.levels_text = tk.Text(master, height=5, width=30, bg="#ffffff", font=("Arial", 10))
        self.levels_text.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

        self.tasks_label = tk.Label(master, text="Tasks:", bg="#f0f0f0", font=("Arial", 12))
        self.tasks_label.grid(row=5, column=0, padx=10, pady=10)

        self.tasks_listbox = tk.Listbox(master, bg="#ffffff", font=("Arial", 10))
        self.tasks_listbox.grid(row=5, column=1, columnspan=2, padx=10, pady=10)

    def add_skill(self):
        skill = self.skill_entry.get()
        if skill and skill not in self.skills:
            self.skills[skill] = {'type': "", 'level': 1}  # Initially set skill level to 1
            self.skill_entry.delete(0, tk.END)
            self.update_levels_text()

    def add_task(self):
        task_name = self.task_entry.get()
        task_type = self.task_type_entry.get()
        if task_name and task_type:
            task = SkillTask(task_name, task_type)
            self.tasks.append(task)
            self.tasks_listbox.insert(tk.END, f"{task_name} ({task_type})")
            self.task_entry.delete(0, tk.END)
            self.task_type_entry.delete(0, tk.END)

    def complete_task(self):
        selected_task_index = self.tasks_listbox.curselection()
        if selected_task_index:
            selected_task = self.tasks[selected_task_index[0]]
            if not selected_task.completed:
                selected_task.completed = True
                self.gain_xp(selected_task.task_type)
                self.update_task_listbox()

    def gain_xp(self, task_type):
        self.xp += 10  # For demonstration, you can adjust the XP gained
        self.skills[task_type]['level'] += 1  # Increase skill level by 1
        self.draw_xp_bar()
        self.update_xp_label()
        self.update_levels_text()

    def draw_xp_bar(self):
        self.xp_bar.delete("all")
        filled_width = (self.xp / 100) * 200
        self.xp_bar.create_rectangle(0, 0, filled_width, 20, fill="#4CAF50")

    def update_xp_label(self):
        self.xp_label.config(text=f"XP: {self.xp}")

        if self.xp >= 100:
            self.add_skill_button.config(state=tk.DISABLED)
            self.add_task_button.config(state=tk.DISABLED)
            self.complete_task_button.config(state=tk.DISABLED)
            self.xp_label.config(text="XP: MAX")

    def update_task_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            if task.completed:
                self.tasks_listbox.insert(tk.END, f"{task.name} ({task.task_type}) (Completed)")
            else:
                self.tasks_listbox.insert(tk.END, f"{task.name} ({task.task_type})")

    def update_levels_text(self):
        self.levels_text.delete(1.0, tk.END)
        for skill, details in self.skills.items():
            self.levels_text.insert(tk.END, f"{skill}: {details['type']} - Level {details['level']}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = SkillTrackerApp(root)
    root.mainloop()
