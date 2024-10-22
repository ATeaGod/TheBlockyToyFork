import tkinter as tk, time

W, H, G = 800, 600, 10
R, C = H // G, W // G
E, S = 0, 1
Cs = {S: "yellow"}
grid, cur, dr, dm, lt, fps = [[E] * C for _ in range(R)], S, False, False, time.time(), 0

def draw(canvas):
    canvas.delete("all")
    canvas.configure(bg="black" if dm else "white")
    for y in range(R):
        for x in range(C):
            color = Cs.get(grid[y][x])
            if color:
                x1, y1 = x * G, y * G
                x2, y2 = x1 + G, y1 + G
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
    canvas.create_text(10, 10, anchor=tk.NW, text=f"FPS: {fps:.2f}, Time: {time.strftime('%H:%M:%S')}", fill="white" if dm else "black")

def update():
    global lt, fps
    fps, lt = 1 / (time.time() - lt), time.time()
    for y in range(R - 2, -1, -1):
        for x in range(C):
            if grid[y][x] == S and grid[y + 1][x] == E:
                grid[y][x], grid[y + 1][x] = E, S
    draw(c)

def add(event):
    x, y = event.x // G, event.y // G
    if 0 <= x < C and 0 <= y < R:
        grid[y][x] = cur

def clear():
    global grid
    grid = [[E] * C for _ in range(R)]

def toggle_dm():
    global dm
    dm = not dm
    root.configure(bg="black" if dm else "white")

def loop():
    update()
    root.after(50, loop)

root = tk.Tk()
root.title("The Blocky Toy DEV")
c = tk.Canvas(root, width=W, height=H)
c.pack()
c.bind("<Button-1>", add)
c.bind("<B1-Motion>", add)

frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

buttons = [("Sand", S), ("Erase", E), ("Clear", clear), ("Dark", toggle_dm)]
for text, element in buttons:
    cmd = element if text in ["Clear", "Dark"] else lambda e=element: cur.__setitem__(0, e)
    tk.Button(frame, text=text, command=cmd, width=7, bg=Cs.get(element, "white")).pack(side=tk.LEFT, pady=5)

root.after(50, loop)
root.mainloop()

