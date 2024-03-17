
import tkinter as tk
from tkinter import ttk

class SkillTask:
    def __init__(self, name, task_type, xp):
        self.name = name
        self.task_type = task_type
        self.xp = xp
        self.completed = False

class SkillTrackerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Skill Tracker")
        self.master.geometry("600x400")
        self.master.configure(bg="#f0f0f0")

        self.skills = {}
        self.tasks = []
        self.xp = 0

        self.style = ttk.Style()
        self.style.configure("TButton", padding=5, relief="flat", background="#4CAF50", foreground="black")
        self.style.map("TButton", background=[('active', '#45a049')])


        self.create_widgets()

    def create_widgets(self):
        self.create_skill_widgets()
        self.create_task_widgets()
        self.create_xp_widgets()

    def create_skill_widgets(self):
        skill_label = ttk.Label(self.master, text="Add Skills:", style="TLabel", font=("Arial", 12), foreground="black")
        skill_label.grid(row=0, column=0, padx=10, pady=10)

        self.skill_entry = ttk.Entry(self.master, width=20)
        self.skill_entry.grid(row=0, column=1, padx=10, pady=10)

        add_skill_button = ttk.Button(self.master, text="Add Skill", command=self.add_skill)
        add_skill_button.grid(row=0, column=2, padx=10, pady=10)

    def create_task_widgets(self):
        task_label = ttk.Label(self.master, text="Add Tasks:", style="TLabel", font=("Arial", 12), foreground="black")
        task_label.grid(row=1, column=0, padx=10, pady=10)

        self.task_entry = ttk.Entry(self.master, width=20)
        self.task_entry.grid(row=1, column=1, padx=10, pady=10)

        task_type_label = ttk.Label(self.master, text="Task Type:", style="TLabel", font=("Arial", 12), foreground="black")
        task_type_label.grid(row=1, column=2, padx=10, pady=10)

        self.task_type_entry = ttk.Entry(self.master, width=20)
        self.task_type_entry.grid(row=1, column=3, padx=10, pady=10)

        xp_label = ttk.Label(self.master, text="XP:", style="TLabel", font=("Arial", 12), foreground="black")
        xp_label.grid(row=1, column=4, padx=10, pady=10)

        self.xp_entry = ttk.Entry(self.master, width=10)
        self.xp_entry.grid(row=1, column=5, padx=10, pady=10)

        add_task_button = ttk.Button(self.master, text="Add Task", command=self.add_task)
        add_task_button.grid(row=1, column=6, padx=10, pady=10)

    def create_xp_widgets(self):
        complete_task_button = ttk.Button(self.master, text="Complete Task", command=self.complete_task)
        complete_task_button.grid(row=3, column=2, columnspan=2, padx=10, pady=10)

        self.xp_label = ttk.Label(self.master, text="XP: 0", style="TLabel", font=("Arial", 12), foreground="black")
        self.xp_label.grid(row=3, column=0, padx=10, pady=10)

        self.xp_bar = ttk.Progressbar(self.master, orient=tk.HORIZONTAL, length=200, mode="determinate", style="TProgressbar")
        self.xp_bar.grid(row=3, column=1, columnspan=2, padx=10, pady=10)
        self.xp_bar["value"] = 0

        levels_label = ttk.Label(self.master, text="Levels:", style="TLabel", font=("Arial", 12), foreground="black")
        levels_label.grid(row=4, column=0, padx=10, pady=10)

        self.levels_text = tk.Text(self.master, height=5, width=30, bg="#ffffff", font=("Arial", 10))
        self.levels_text.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

        tasks_label = ttk.Label(self.master, text="Tasks:", style="TLabel", font=("Arial", 12), foreground="black")
        tasks_label.grid(row=5, column=0, padx=10, pady=10)

        self.tasks_listbox = tk.Listbox(self.master, bg="#ffffff", font=("Arial", 10), selectbackground="#4CAF50")
        self.tasks_listbox.grid(row=5, column=1, columnspan=2, padx=10, pady=10)

    def add_skill(self):
        skill = self.skill_entry.get()
        if skill and skill not in self.skills:
            self.skills[skill] = {'type': "", 'level': 1, 'xp_needed': 10}  # Set initial XP needed to 10
            self.skill_entry.delete(0, tk.END)
            self.update_levels_text()

    def add_task(self):
        task_name = self.task_entry.get()
        task_type = self.task_type_entry.get()
        try:
            xp = int(self.xp_entry.get())
        except ValueError:
            xp = 0
        if task_name and task_type and xp >= 0:
            task = SkillTask(task_name, task_type, xp)
            self.tasks.append(task)
            self.tasks_listbox.insert(tk.END, f"{task.name} ({task.task_type}) - XP: {task.xp}")
            self.task_entry.delete(0, tk.END)
            self.task_type_entry.delete(0, tk.END)
            self.xp_entry.delete(0, tk.END)

    def complete_task(self):
        selected_task_index = self.tasks_listbox.curselection()
        if selected_task_index:
            selected_task = self.tasks[selected_task_index[0]]
            if not selected_task.completed:
                selected_task.completed = True
                self.gain_xp(selected_task.task_type, selected_task.xp)
                self.update_task_listbox()

    def gain_xp(self, task_type, xp):
        self.xp += xp
        self.skills[task_type]['level'] += 1  # Increase skill level by 1
        self.skills[task_type]['xp_needed'] *= 2  # Double the XP needed for the next level
        self.draw_xp_bar()
        self.update_xp_label()
        self.update_levels_text()

    def draw_xp_bar(self):
        total_xp_needed = sum(skill['xp_needed'] for skill in self.skills.values())
        filled_width = (self.xp / total_xp_needed) * 200
        self.xp_bar["value"] = filled_width

    def update_xp_label(self):
        self.xp_label.config(text=f"XP: {self.xp}")

    def update_task_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            if task.completed:
                self.tasks_listbox.insert(tk.END, f"{task.name} ({task.task_type}) - XP: {task.xp} (Completed)")
            else:
                self.tasks_listbox.insert(tk.END, f"{task.name} ({task.task_type}) - XP: {task.xp}")

    def update_levels_text(self):
        self.levels_text.delete(1.0, tk.END)
        for skill, details in self.skills.items():
            self.levels_text.insert(tk.END, f"{skill}: {details['type']} - Level {details['level']}, XP Needed: {details['xp_needed']}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = SkillTrackerApp(root)
    root.mainloop()
