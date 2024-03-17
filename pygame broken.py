import pygame
import sys

class SkillTask:
    def __init__(self, name, task_type, xp):
        self.name = name
        self.task_type = task_type
        self.xp = xp
        self.completed = False

class SkillTrackerApp:
    def __init__(self):
        pygame.init()
        self.screen_width = 600
        self.screen_height = 400
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Skill Tracker")
        self.clock = pygame.time.Clock()

        self.skills = {}
        self.tasks = []
        self.xp = 0

        self.font = pygame.font.SysFont(None, 24)
        self.text_color = (0, 0, 0)

        self.skill_entry = ""
        self.task_entry = ""
        self.task_type_entry = ""
        self.xp_entry = ""

        self.create_widgets()

    def create_widgets(self):
        self.skill_entry_rect = pygame.Rect(50, 50, 200, 30)
        self.task_entry_rect = pygame.Rect(50, 100, 200, 30)
        self.task_type_entry_rect = pygame.Rect(300, 100, 200, 30)
        self.xp_entry_rect = pygame.Rect(550, 100, 50, 30)
        self.add_skill_button_rect = pygame.Rect(50, 150, 100, 30)
        self.add_task_button_rect = pygame.Rect(50, 200, 100, 30)
        self.complete_task_button_rect = pygame.Rect(300, 150, 200, 30)

    def add_skill(self):
        skill = self.skill_entry.strip()
        if skill and skill not in self.skills:
            self.skills[skill] = {'type': "", 'level': 1, 'xp_needed': 10}
            self.skill_entry = ""
            self.update_levels_text()

    def add_task(self):
        task_name = self.task_entry.strip()
        task_type = self.task_type_entry.strip()
        try:
            xp = int(self.xp_entry.strip())
        except ValueError:
            xp = 0
        if task_name and task_type and xp >= 0:
            task = SkillTask(task_name, task_type, xp)
            self.tasks.append(task)
            self.task_entry = ""
            self.task_type_entry = ""
            self.xp_entry = ""

    def complete_task(self):
        pass

    def draw_text(self, text, rect):
        surface = self.font.render(text, True, self.text_color)
        self.screen.blit(surface, (rect.x + 5, rect.y + 5))

    def run(self):
        running = True
        while running:
            self.screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.add_skill_button_rect.collidepoint(mouse_pos):
                            self.add_skill()
                        elif self.add_task_button_rect.collidepoint(mouse_pos):
                            self.add_task()
                        elif self.complete_task_button_rect.collidepoint(mouse_pos):
                            self.complete_task()
                elif event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_ESCAPE:
                        running = False
                    elif self.skill_entry_rect.collidepoint(pygame.mouse.get_pos()):
                        if event.key == pygame.K_BACKSPACE:
                            self.skill_entry = self.skill_entry[:-1]
                        else:
                            self.skill_entry += event.unicode
                    elif self.task_entry_rect.collidepoint(pygame.mouse.get_pos()):
                        if event.key == pygame.K_BACKSPACE:
                            self.task_entry = self.task_entry[:-1]
                        else:
                            self.task_entry += event.unicode
                    elif self.task_type_entry_rect.collidepoint(pygame.mouse.get_pos()):
                        if event.key == pygame.K_BACKSPACE:
                            self.task_type_entry = self.task_type_entry[:-1]
                        else:
                            self.task_type_entry += event.unicode
                    elif self.xp_entry_rect.collidepoint(pygame.mouse.get_pos()):
                        if event.key == pygame.K_BACKSPACE:
                            self.xp_entry = self.xp_entry[:-1]
                        else:
                            self.xp_entry += event.unicode

            pygame.draw.rect(self.screen, (0, 0, 0), self.skill_entry_rect, 2)
            self.draw_text(self.skill_entry, self.skill_entry_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), self.task_entry_rect, 2)
            self.draw_text(self.task_entry, self.task_entry_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), self.task_type_entry_rect, 2)
            self.draw_text(self.task_type_entry, self.task_type_entry_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), self.xp_entry_rect, 2)
            self.draw_text(self.xp_entry, self.xp_entry_rect)

            pygame.draw.rect(self.screen, (0, 0, 0), self.add_skill_button_rect, 2)
            self.draw_text("Add Skill", self.add_skill_button_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), self.add_task_button_rect, 2)
            self.draw_text("Add Task", self.add_task_button_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), self.complete_task_button_rect, 2)
            self.draw_text("Complete Task", self.complete_task_button_rect)

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = SkillTrackerApp()
    app.run()
