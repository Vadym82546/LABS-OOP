import tkinter as tk
from tkinter import messagebox
import random

CELL_SIZE = 30
GRID_SIZE = 10
FLEET = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1] # Кораблі

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)] # Створення матриці 10х10, де зберігаються стани клітинок: 0: пусто, 1: корабель, 2: промах, 3: влучення
        self.ships = []

    def is_valid_placement(self, x, y, length, horizontal):
        if horizontal:
            if x + length > GRID_SIZE: return False
        else:
            if y + length > GRID_SIZE: return False

        for i in range(length):
            cx = x + i if horizontal else x
            cy = y if horizontal else y + i
            # Перевірка суміжних клітинок (кораблі не можуть торкатися)
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                        if self.grid[ny][nx] == 1:
                            return False
        return True

# Запам'ятовує координати кожної клітинки, де знаходиться корабель (його частини), та встановлює їх початоквий стан.
    def place_ship(self, x, y, length, horizontal):
        coords = []
        for i in range(length):
            cx = x + i if horizontal else x
            cy = y if horizontal else y + i
            self.grid[cy][cx] = 1
            coords.append((cx, cy))
        self.ships.append({"coords": coords, "hits": 0, "sunk": False})

 # Випадково ставить усі кораблі у межах ігрового поля та згідно з правилами is_valid_placement
    def auto_place_fleet(self):
        for length in FLEET:
            placed = False
            while not placed:
                x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
                horizontal = random.choice([True, False])
                if self.is_valid_placement(x, y, length, horizontal):
                    self.place_ship(x, y, length, horizontal)
                    placed = True

 # Логіка зміни стану клітинки від пострілу.
    def receive_shot(self, x, y):
        # 0: пусто, 1: корабель, 2: промах, 3: влучення
        if self.grid[y][x] in [2, 3]:
            return "invalid", None
        if self.grid[y][x] == 1:
            self.grid[y][x] = 3
            for ship in self.ships:
                if (x, y) in ship["coords"]:
                    ship["hits"] += 1
                    if ship["hits"] == len(ship["coords"]):
                        ship["sunk"] = True
                        self._mark_surrounding_as_miss(ship)
                        return "sunk", ship
            return "hit", None
        else:
            self.grid[y][x] = 2
            return "miss", None

 # Після потоплення корабля суміжні клітинки набувають стану "промах"
    def _mark_surrounding_as_miss(self, ship):
        for cx, cy in ship["coords"]:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                        if self.grid[ny][nx] == 0:
                            self.grid[ny][nx] = 2

 # Булевий вираз "Чи всі кораблі потоплені?""
    def all_sunk(self):
        return all(ship["sunk"] for ship in self.ships)

class BattleshipGame(tk.Tk):
    # Створення вікна та полей, встановлення початкових значень змінних, розташування кораблів компьютером
    def __init__(self):
        super().__init__()
        self.title("Морський бій")
        self.resizable(False, False)

        self.player_board = Board()
        self.computer_board = Board()
        self.computer_board.auto_place_fleet()

        self.setup_ui()
        
        self.state = "PLACEMENT"
        self.ships_to_place = FLEET.copy()
        self.horizontal_placement = True
        
        # Змінні AI
        self.ai_state = "HUNT"
        self.ai_targets = []
        self.ai_first_hit = None
        self.ai_current_hits = []

        self.update_status()

# Налаштування біндів та малювання сітки. Також створення напису, який буде описувати поточний стан гри
    def setup_ui(self):
        self.canvas_player = tk.Canvas(self, width=CELL_SIZE*GRID_SIZE, height=CELL_SIZE*GRID_SIZE, bg="lightblue")
        self.canvas_player.grid(row=1, column=0, padx=20, pady=20)
        self.canvas_player.bind("<Button-1>", self.on_player_click)
        self.canvas_player.bind("<Button-3>", self.toggle_orientation)
        self.canvas_player.bind("<Motion>", self.on_mouse_motion)

        self.canvas_computer = tk.Canvas(self, width=CELL_SIZE*GRID_SIZE, height=CELL_SIZE*GRID_SIZE, bg="lightblue")
        self.canvas_computer.grid(row=1, column=1, padx=20, pady=20)
        self.canvas_computer.bind("<Button-1>", self.on_computer_click)

        self.status_label = tk.Label(self, text="Розмістіть кораблі. ЛКМ - встановити, ПКМ - повернути.", font=("Arial", 12))
        self.status_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.draw_grid(self.canvas_player)
        self.draw_grid(self.canvas_computer)

# Малює сітку по клітинками
    def draw_grid(self, canvas):
        for i in range(GRID_SIZE + 1):
            canvas.create_line(0, i*CELL_SIZE, GRID_SIZE*CELL_SIZE, i*CELL_SIZE, fill="blue")
            canvas.create_line(i*CELL_SIZE, 0, i*CELL_SIZE, GRID_SIZE*CELL_SIZE, fill="blue")

    def toggle_orientation(self, event):
        if self.state == "PLACEMENT":
            self.horizontal_placement = not self.horizontal_placement
            self.on_mouse_motion(event)

 # Прев'ю розташування поточного корабля (відображення прямокутника та кольору "(не)можна")
    def on_mouse_motion(self, event):
        if self.state != "PLACEMENT" or not self.ships_to_place:
            return
        self.canvas_player.delete("preview")
        # Така конструкція дозволяє визначити, на якій клітинці знаходиться курсор (надалі також використовується для кліку мишею)
        x, y = event.x // CELL_SIZE, event.y // CELL_SIZE
        length = self.ships_to_place[0]
        
        valid = self.player_board.is_valid_placement(x, y, length, self.horizontal_placement)
        color = "green" if valid else "red"
        
        for i in range(length):
            cx = x + i if self.horizontal_placement else x
            cy = y if self.horizontal_placement else y + i
            if 0 <= cx < GRID_SIZE and 0 <= cy < GRID_SIZE:
                self.canvas_player.create_rectangle(
                    cx*CELL_SIZE, cy*CELL_SIZE, (cx+1)*CELL_SIZE, (cy+1)*CELL_SIZE,
                    fill=color, stipple="gray50", tags="preview"
                )

 # Розташування кораблів кліком мишки
    def on_player_click(self, event):
        if self.state != "PLACEMENT": return
        
        x, y = event.x // CELL_SIZE, event.y // CELL_SIZE
        length = self.ships_to_place[0]
        
        if self.player_board.is_valid_placement(x, y, length, self.horizontal_placement):
            self.player_board.place_ship(x, y, length, self.horizontal_placement)
            self.ships_to_place.pop(0)
            self.redraw_board(self.canvas_player, self.player_board, hide_ships=False)
            
            if not self.ships_to_place:
                self.state = "PLAYING"
                self.canvas_player.delete("preview")
                self.update_status("Ваш хід! Атакуйте поле противника.")
            else:
                self.on_mouse_motion(event)

 # Перевірка стану гри та надання ходу компьютеру
    def on_computer_click(self, event):
        if self.state != "PLAYING": return
        x, y = event.x // CELL_SIZE, event.y // CELL_SIZE
        
        result, _ = self.computer_board.receive_shot(x, y)
        if result == "invalid": return
        
        self.redraw_board(self.canvas_computer, self.computer_board, hide_ships=True)
        
        if self.computer_board.all_sunk():
            self.state = "GAME_OVER"
            self.update_status("Гравець переміг!")
            self.redraw_board(self.canvas_computer, self.computer_board, hide_ships=False)
            return

        if result == "miss":
            self.update_status("Промах. Хід комп'ютера...")
            self.after(500, self.computer_turn)
        else:
            self.update_status("Влучання! Ваш хід.")

 # Хід компьютера. Виконання пострілу, потім визначення нових клітинок-таргетів та поведінки компьютера. Перевірка стану гри.
    def computer_turn(self):
        if self.state != "PLAYING": return

        x, y = self.get_ai_target()
        result, ship = self.player_board.receive_shot(x, y)

        if result == "hit":
            self.ai_current_hits.append((x, y))
            if self.ai_state == "HUNT":
                self.ai_state = "TARGET"
                self.ai_first_hit = (x, y)
                self._generate_cross_targets(x, y)
            elif self.ai_state == "TARGET":
                self.ai_state = "DESTROY"
                self._refine_targets_to_line()
            elif self.ai_state == "DESTROY":
                self._extend_line_targets()
                
        elif result == "sunk":
            self.ai_state = "HUNT"
            self.ai_targets.clear()
            self.ai_current_hits.clear()
            self.ai_first_hit = None

        self.redraw_board(self.canvas_player, self.player_board, hide_ships=False)

        if self.player_board.all_sunk():
            self.state = "GAME_OVER"
            self.update_status("Комп'ютер переміг.")
            return

        if result in ["hit", "sunk"]:
            self.after(500, self.computer_turn)
        else:
            self.update_status("Ваш хід.")

 # Повертає клітинку, в яку буде зроблено постріл. Вилучення цієї клітинки з списку клітинок-таргетів.
    def get_ai_target(self):
        while self.ai_targets:
            tx, ty = self.ai_targets.pop(0)
            if self.player_board.grid[ty][tx] in [0, 1]:
                return tx, ty

        # Поведінка стрільби навмання
        while True:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if self.player_board.grid[y][x] in [0, 1]:
                return x, y

# Коли підбито першу частину корабля, компьютер генерує клітинки-таргети, в які буде зроблено наступні постріли (форма "+")
    def _generate_cross_targets(self, x, y):
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if self.player_board.grid[ny][nx] in [0, 1]:
                    self.ai_targets.append((nx, ny))

 # Коли компьютер робить другий постріл, то клітинки-таргети забуваються, та відбувається виклик _extend_line_targets
    def _refine_targets_to_line(self):
        if len(self.ai_current_hits) < 2: return
        self.ai_targets.clear()
        self._extend_line_targets()

 # За допомогою двох відомих станів клітинок, компьютер знаходить орієнтацію корабля та оновлює список клітинок-таргети
    def _extend_line_targets(self):
        self.ai_targets.clear()
        hits = sorted(self.ai_current_hits)
        is_horizontal = hits[0][1] == hits[1][1]
        
        if is_horizontal:
            min_x, max_x = hits[0][0], hits[-1][0]
            y = hits[0][1]
            candidates = [(min_x - 1, y), (max_x + 1, y)]
        else:
            min_y, max_y = hits[0][1], hits[-1][1]
            x = hits[0][0]
            candidates = [(x, min_y - 1), (x, max_y + 1)]
            
        for cx, cy in candidates:
            if 0 <= cx < GRID_SIZE and 0 <= cy < GRID_SIZE:
                if self.player_board.grid[cy][cx] in [0, 1]:
                    self.ai_targets.append((cx, cy))

# Оновлення відображення ігрових полів згідно з станами клітинок
    def redraw_board(self, canvas, board, hide_ships):
        canvas.delete("all")
        self.draw_grid(canvas)
        
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                # 0: пусто, 1: корабель, 2: промах, 3: влучення
                cell = board.grid[y][x]
                if cell == 1 and not hide_ships:
                    canvas.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, outline="yellow", width=2)
                elif cell == 2:
                    canvas.create_oval(x*CELL_SIZE+10, y*CELL_SIZE+10, (x+1)*CELL_SIZE-10, (y+1)*CELL_SIZE-10, fill="black")
                elif cell == 3:
                    canvas.create_line(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill="red", width=2)
                    canvas.create_line(x*CELL_SIZE, (y+1)*CELL_SIZE, (x+1)*CELL_SIZE, y*CELL_SIZE, fill="red", width=2)

 # Оновлення напису згідно з станом гри
    def update_status(self, text=None):
        if text:
            self.status_label.config(text=text)
        elif self.state == "PLACEMENT":
            self.status_label.config(text=f"Розмістіть кораблі ({len(self.ships_to_place)} залиш.). ЛКМ - встановити, ПКМ - повернути.")

if __name__ == "__main__":
    app = BattleshipGame()
    app.mainloop()