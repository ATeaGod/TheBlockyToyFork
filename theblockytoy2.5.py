import tkinter as tk, os, json, time
from tkinter import messagebox, filedialog

W, H, G, L = 800, 600, 10, 1024
R, C = H // G, W // G
E, S, Wt, Wa, V, Cn, Wd = range(7)
Cs = {S: "yellow", Wt: "blue", Wa: "gray", V: "red", Cn: "green", Wd: "brown"}
Bcs = {S: "#FFFF99", Wt: "#99CCFF", Wa: "#CCCCCC", V: "#FF9999", Cn: "#99FF99", Wd: "#CC9966"}
grid, cur, dr, dm, lt, fps, pc = [[E] * C for _ in range(R)], S, False, False, time.time(), 0, 0

def draw(canvas, scale=1, off=(0, 0)):
    canvas.delete("all")
    canvas.configure(bg="black" if dm else "white")
    for row in range(R):
        for col in range(C):
            color = Cs.get(grid[row][col])
            if color:
                x1, y1 = (col * G - off[0]) * scale, (row * G - off[1]) * scale
                x2, y2 = x1 + G * scale, y1 + G * scale
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
    canvas.create_text(10, 10, anchor=tk.NW, text=f"FPS: {fps:.2f}, Particles: {pc}", fill="white" if dm else "black")

def update():
    global lt, fps, pc
    fps, lt = 1 / (time.time() - lt), time.time()
    pc = sum(row.count(S) + row.count(Wt) + row.count(Cn) + row.count(Wd) for row in grid)
    for row in range(R - 2, -1, -1):
        for col in range(C):
            if grid[row][col] == S and grid[row + 1][col] in [E, Wt]:
                grid[row][col], grid[row + 1][col] = (Wt, S) if grid[row + 1][col] == Wt else (E, S)
            elif grid[row][col] == Wt:
                for dx, dy in [(0, 1), (-1, 1), (1, 1), (-1, 0), (1, 0)]:
                    if 0 <= col + dx < C and 0 <= row + dy < R and grid[row + dy][col + dx] == E:
                        grid[row][col], grid[row + dy][col + dx] = E, Wt
                        break
            elif grid[row][col] == V:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if 0 <= col + dx < C and 0 <= row + dy < R:
                        grid[row + dy][col + dx] = E
            elif grid[row][col] == Cn:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if 0 <= col + dx < C and 0 <= row + dy < R and grid[row + dy][col + dx] not in (E, Cn):
                        grid[row][col] = grid[row + dy][col + dx]
                        break

def add(x, y):
    global pc
    col, row = x // G, y // G
    if grid[row][col] == E or cur == E:
        grid[row][col] = cur
        pc += 1 if cur != E else 0

def clear():
    global grid, pc
    grid, pc = [[E] * C for _ in range(R)], 0

def toggle_dm():
    global dm
    dm = not dm
    root.configure(bg="black" if dm else "white")

def on_mouse(event, down):
    global dr
    dr = down
    if down:
        add(event.x, event.y)

def set_elem(element):
    global cur
    cur = element

def zoom(event):
    if event.char == 'z':
        canvas.delete("all")
        draw(canvas, scale=2, off=(event.x, event.y))

def save_sim():
    path = os.path.join(os.path.expanduser('~'), 'Downloads', 'falling_sand_sim')
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'simulation.json'), 'w') as f:
        json.dump(grid, f)

def load_sim():
    path = os.path.join(os.path.expanduser('~'), 'Downloads', 'falling_sand_sim')
    file_path = filedialog.askopenfilename(initialdir=path, title="Select Simulation", filetypes=(("JSON Files", "*.json"),))
    if file_path:
        with open(file_path, 'r') as f:
            global grid
            grid = json.load(f)

def ask_exit():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        save_sim()
        root.destroy()

def loop(canvas):
    update()
    draw(canvas)
    root.after(50, loop, canvas)

root = tk.Tk()
root.title("Falling Sand Game")
canvas = tk.Canvas(root, width=W, height=H)
canvas.pack(side=tk.TOP)
canvas.bind("<Button-1>", lambda e: on_mouse(e, True))
canvas.bind("<B1-Motion>", lambda e: on_mouse(e, dr))
canvas.bind("<ButtonRelease-1>", lambda e: on_mouse(e, False))
root.bind("<Key>", zoom)
root.bind("<q>", lambda e: ask_exit())

frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

buttons = [
    ("Sand", S), ("Water", Wt), ("Wall", Wa), ("Void", V), ("Clone", Cn), ("Wood", Wd),
    ("Erase", E), ("Clear", clear), ("Dark", toggle_dm), ("Save", save_sim), ("Load", load_sim)
]

for text, element in buttons:
    cmd = element if text in ["Clear", "Dark", "Save", "Load"] else lambda e=element: set_elem(e)
    tk.Button(frame, text=text, command=cmd, width=7, bg=Bcs.get(element, "white")).pack(side=tk.LEFT, pady=5)

root.after(50, loop, canvas)
root.mainloop()


