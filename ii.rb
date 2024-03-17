require 'tk'

class SkillTask
  attr_accessor :name, :task_type, :xp, :completed

  def initialize(name, task_type, xp)
    @name = name
    @task_type = task_type
    @xp = xp
    @completed = false
  end
end

class SkillTrackerApp
  def initialize
    @skills = {}
    @tasks = []
    @xp = 0

    @root = TkRoot.new { title "Skill Tracker" }
    @root.geometry "600x400"
    @root.configure bg: "#f0f0f0"

    @style = Tk::Tile::Style.new
    @style.configure "TButton", padding: 5, relief: "flat", background: "#4CAF50", foreground: "black"
    @style.map "TButton", background: [['active', '#45a049']]

    create_widgets
  end

  def create_widgets
    create_skill_widgets
    create_task_widgets
    create_xp_widgets
  end

  def create_skill_widgets
    skill_label = Tk::Tile::Label.new(@root) { text "Add Skills:"; style "TLabel"; font "Arial 12"; foreground "black" }.grid(row: 0, column: 0, padx: 10, pady: 10)
    @skill_entry = Tk::Tile::Entry.new(@root) { width 20 }.grid(row: 0, column: 1, padx: 10, pady: 10)
    add_skill_button = Tk::Tile::Button.new(@root) { text "Add Skill"; command proc { add_skill } }.grid(row: 0, column: 2, padx: 10, pady: 10)
  end

  def create_task_widgets
    task_label = Tk::Tile::Label.new(@root) { text "Add Tasks:"; style "TLabel"; font "Arial 12"; foreground "black" }.grid(row: 1, column: 0, padx: 10, pady: 10)
    @task_entry = Tk::Tile::Entry.new(@root) { width 20 }.grid(row: 1, column: 1, padx: 10, pady: 10)
    task_type_label = Tk::Tile::Label.new(@root) { text "Task Type:"; style "TLabel"; font "Arial 12"; foreground "black" }.grid(row: 1, column: 2, padx: 10, pady: 10)
    @task_type_entry = Tk::Tile::Entry.new(@root) { width 20 }.grid(row: 1, column: 3, padx: 10, pady: 10)
    xp_label = Tk::Tile::Label.new(@root) { text "XP:"; style "TLabel"; font "Arial 12"; foreground "black" }.grid(row: 1, column: 4, padx: 10, pady: 10)
    @xp_entry = Tk::Tile::Entry.new(@root) { width 10 }.grid(row: 1, column: 5, padx: 10, pady: 10)
    add_task_button = Tk::Tile::Button.new(@root) { text "Add Task"; command proc { add_task } }.grid(row: 1, column: 6, padx: 10, pady: 10)
  end

  def create_xp_widgets
    complete_task_button = Tk::Tile::Button.new(@root) { text "Complete Task"; command proc { complete_task } }.grid(row: 3, column: 2, columnspan: 2, padx: 10, pady: 10)
    @xp_label = Tk::Tile::Label.new(@root) { text "XP: 0"; style "TLabel"; font "Arial 12"; foreground "black" }.grid(row: 3, column: 0, padx: 10, pady: 10)
    @xp_bar = Tk::Tile::Progressbar.new(@root) { orient 'horizontal'; length 200; mode 'determinate'; style "TProgressbar" }.grid(row: 3, column: 1, columnspan: 2, padx: 10, pady: 10)
    @xp_bar.value = 0
    levels_label = Tk::Tile::Label.new(@root) { text "Levels:"; style "TLabel"; font "Arial 12"; foreground "black" }.grid(row: 4, column: 0, padx: 10, pady: 10)
    @levels_text = TkText.new(@root) { height 5; width 30; background "#ffffff"; font "Arial 10" }.grid(row: 4, column: 1, columnspan: 2, padx: 10, pady: 10)
    tasks_label = Tk::Tile::Label.new(@root) { text "Tasks:"; style "TLabel"; font "Arial 12"; foreground "black" }.grid(row: 5, column: 0, padx: 10, pady: 10)
    @tasks_listbox = TkListbox.new(@root) { background "#ffffff"; font "Arial 10"; selectbackground "#4CAF50" }.grid(row: 5, column: 1, columnspan: 2, padx: 10, pady: 10)
  end

  def add_skill
    skill = @skill_entry.get
    if skill && !@skills.key?(skill)
      @skills[skill] = { type: "", level: 1, xp_needed: 10 }
      @skill_entry.delete 0, :end
      update_levels_text
    end
  end

  def add_task
    task_name = @task_entry.get
    task_type = @task_type_entry.get
    begin
      xp = Integer(@xp_entry.get)
    rescue ArgumentError
      xp = 0
    end
    if task_name && task_type && xp >= 0
      task = SkillTask.new(task_name, task_type, xp)
      @tasks << task
      @tasks_listbox.insert(:end, "#{task.name} (#{task.task_type}) - XP: #{task.xp}")
      @task_entry.delete 0, :end
      @task_type_entry.delete 0, :end
      @xp_entry.delete 0, :end
    end
  end

  def complete_task
    selected_task_index = @tasks_listbox.curselection
    if selected_task_index
      selected_task = @tasks[selected_task_index[0]]
      unless selected_task.completed
        selected_task.completed = true
        gain_xp(selected_task.task_type, selected_task.xp)
        update_task_listbox
      end
    end
  end

  def gain_xp(task_type, xp)
    @xp += xp
    @skills[task_type][:level] += 1
    @skills[task_type][:xp_needed] *= 2
    draw_xp_bar
    update_xp_label
    update_levels_text
  end

  def draw_xp_bar
    total_xp_needed = @skills.values.sum { |skill| skill[:xp_needed] }
    filled_width = (@xp.to_f / total_xp_needed) * 200
    @xp_bar.value = filled_width
  end

  def update_xp_label
    @xp_label.text = "XP: #{@xp}"
  end

  def update_task_listbox
    @tasks_listbox.delete 0, :end
    @tasks.each do |task|
      if task.completed
        @tasks_listbox.insert(:end, "#{task.name} (#{task.task_type}) - XP: #{task.xp} (Completed)")
      else
        @tasks_listbox.insert(:end, "#{task.name} (#{task.task_type}) - XP: #{task.xp}")
      end
    end
  end

  def update_levels_text
    @levels_text.delete '1.0', :end
    @skills.each do |skill, details|
      @levels_text.insert :end, "#{skill}: #{details[:type]} - Level #{details[:level]}, XP Needed: #{details[:xp_needed]}\n"
    end
  end
end

app = SkillTrackerApp.new
Tk.mainloop
