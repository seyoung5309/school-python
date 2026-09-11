import tkinter as tk
from tkinter import messagebox
import socket
import threading

SERVER_IP = 'localhost'
SERVER_PORT = 12345
SAVE_FILE = "game_data.txt"
BOARD_SIZE = 19

class Othello:
    def __init__(self, master):
        self.master = master
        self.master.title("오목 게임")

        self.board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = 'B'

        self.create_board()
        self.create_buttons()
        self.create_menu()

        self.server_socket = None
        self.client_socket = None
        self.connected = False
        self.turn = 'B'

    def create_board(self):
        self.canvas = tk.Canvas(self.master, width=BOARD_SIZE * 40, height=BOARD_SIZE * 40)
        self.canvas.pack()

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                x = i * 40
                y = j * 40
                self.canvas.create_rectangle(x, y, x + 40, y + 40, fill="white")

    def create_buttons(self):
        self.buttons = []
        for i in range(BOARD_SIZE):
            row = []
            for j in range(BOARD_SIZE):
                button = tk.Button(self.master, width=2, height=1, command=lambda x=i, y=j: self.play(x, y))
                row.append(button)
                self.canvas.create_window(j * 40 + 20, i * 40 + 20, window=button)
            self.buttons.append(row)

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save", command=self.save_game)
        file_menu.add_command(label="Load", command=self.load_game)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        connect_menu = tk.Menu(menubar, tearoff=0)
        connect_menu.add_command(label="Start Server", command=self.start_server)
        connect_menu.add_command(label="Connect to Server", command=self.connect_to_server)
        menubar.add_cascade(label="Connect", menu=connect_menu)

    def play(self, x, y):
        if self.is_valid_move(x, y):
            self.board[x][y] = self.current_player
            self.update_canvas()
            if self.check_win(x, y):
                winner = "흑돌(B)" if self.current_player == 'B' else "백돌(W)"
                messagebox.showinfo("게임 종료", f"{winner} 승리!")
                return
            self.current_player = self.get_opposite_player(self.current_player)

            def is_valid_move(self, x, y):
                # 빈 칸인 경우에만 착수 가능
                return self.board[x][y] is None

            def check_win(self, x, y):
                # 가로, 세로, 대각선 2방향 (총 4방향) 연속 5개 확인
                color = self.board[x][y]
                directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
                
                for dx, dy in directions:
                    count = 1
                    for step in (-1, 1):
                        nx, ny = x + step * dx, y + step * dy
                        while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[nx][ny] == color:
                            count += 1
                            nx += step * dx
                            ny += step * dy
                    if count >= 5:
                        return True
                return False

    def is_valid_move(self, x, y):
        if self.board[x][y] is not None:
            return False

        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            found = False
            for i in range(1, BOARD_SIZE):
                nx, ny = x + i * dx, y + i * dy
                if nx < 0 or nx >= BOARD_SIZE or ny < 0 or ny >= BOARD_SIZE:
                    break
                if self.board[nx][ny] == self.current_player:
                    found = True
                    break
                elif self.board[nx][ny] is None:
                    break

            if found:
                return True

        return False

    def update_canvas(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                color = "SystemButtonFace"
                if self.board[i][j] == 'B':
                    color = "black"
                elif self.board[i][j] == 'W':
                    color = "white"
                self.buttons[i][j].config(bg=color)

    def get_opposite_player(self, player):
        return 'W' if player == 'B' else 'B'

    def check_game_over(self):
        if self.is_board_full():
            self.end_game()

    def is_board_full(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] is None:
                    return False
        return True

    def end_game(self):
        player_counts = {'B': 0, 'W': 0}
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j]:
                    player_counts[self.board[i][j]] += 1

        winner = 'B' if player_counts['B'] > player_counts['W'] else 'W'
        messagebox.showinfo("Game Over", f"{winner} wins!")

    def save_game(self):
        with open(SAVE_FILE, 'w') as file:
            for row in self.board:
                file.write(' '.join([cell if cell else 'N' for cell in row]) + '\n')

    def load_game(self):
        try:
            with open(SAVE_FILE, 'r') as file:
                lines = file.readlines()
                for i in range(BOARD_SIZE):
                    row = lines[i].strip().split()
                    self.board[i] = [cell if cell != 'N' else None for cell in row]
            self.update_canvas()
            messagebox.showinfo("Game Loaded", "Game loaded successfully!")
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found!")

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((SERVER_IP, SERVER_PORT))
        self.server_socket.listen(1)
        self.master.title("서버 시작 - 접속 대기 중...")

        def accept_connections():
            client_socket, addr = self.server_socket.accept()
            self.connected = True
            self.client_socket = client_socket
            self.master.title(f"서버 연결됨 ({addr[0]})")

        threading.Thread(target=accept_connections, daemon=True).start()

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((SERVER_IP, SERVER_PORT))
            self.connected = True
            self.master.title("서버 연결됨")

            def receive_game_data():
                while self.connected:
                    try:
                        game_data = self.client_socket.recv(1024).decode()
                        if game_data:
                            # 데이터 수신 후 처리 로직 위치
                            pass
                    except ConnectionResetError:
                        break

            threading.Thread(target=receive_game_data, daemon=True).start()
        except ConnectionRefusedError:
            messagebox.showerror("Error", "서버에 연결할 수 없습니다.")

if __name__ == "__main__":
    root = tk.Tk()
    game = Othello(root)
    root.mainloop()