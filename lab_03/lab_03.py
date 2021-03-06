from tkinter import messagebox, ttk, colorchooser
from tkinter import *
from math import radians, cos, sin, fabs, floor, pi, sqrt
import colorutils as cu
import matplotlib.pyplot as plt
import numpy as np
import time

WIN_WIDTH = 1200
WIN_HEIGHT = 800

SIZE = 800
WIDTH = 100.0

PLUS = 1
MINUS = 0

TASK = "Алгоритмы построения отрезков.\n\n" \
       "Реализовать возможность построения " \
       "отрезков методами Брезенхема, Ву, ЦДА, " \
       "построение пучка отрезков и " \
       "сравнение времени и ступенчатости."

AUTHOR = "\n\nЕгорова Полина ИУ7-44Б"


# координаты точки из канвасовских в фактические
def to_coords(dot):
    x = (dot[0] - coord_center[0]) * m_board
    y = (-dot[1] + coord_center[1]) * m_board

    return [x, y]


# координаты точки из фактических в канвасовские
def to_canva(dot):
    x = coord_center[0] + dot[0] / m_board
    y = coord_center[1] - dot[1] / m_board

    return [x, y]


def distance(point1, point2):
    x1 = max(point1[0], point2[0])
    x2 = min(point1[0], point2[0])
    y1 = max(point1[1], point2[1])
    y2 = min(point1[1], point2[1])
    return sqrt(((y2 - y1) * (y2 - y1)) + (x2 - x1) * (x2 - x1))


def sign(diff):
    if diff < 0:
        return -1
    elif diff == 0:
        return 0
    else:
        return 1


def parse_line(opt):
    try:
        x1 = int(x1_entry.get())
        y1 = int(y1_entry.get())
        x2 = int(x2_entry.get())
        y2 = int(y2_entry.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Неверно введены координаты")
        return

    p1 = [x1, y1]
    p2 = [x2, y2]

    parse_methods(p1, p2, opt)


def parse_methods(p1, p2, opt, draw=True):
    # print("Method = ", opt)
    color = cu.Color(current_color[0])

    if opt == 0:
        dots = bresenham_int(p1, p2, color)

        if draw:
            draw_line(dots)

    elif opt == 1:
        dots = bresenham_float(p1, p2, color)

        if draw:
            draw_line(dots)

    elif opt == 2:
        dots = bresenham_smooth(p1, p2, color)

        if draw:
            draw_line(dots)

    elif opt == 3:
        dots = dda_method(p1, p2, color)

        if draw:
            draw_line(dots)

    elif opt == 4:
        dots = wu(p1, p2, color)

        if draw:
            draw_line(dots)

    elif opt == 5:
        lib_method(p1, p2, color)

    else:
        messagebox.showerror("Ошибка", "Неизвестный алгоритм")


def bresenham_int(p1, p2, color, step_count=False):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]

    if (x2 - x1 == 0) and (y2 - y1 == 0):
        return [[x1, y1, color]]

    x = x1
    y = y1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    s1 = sign(x2 - x1)
    s2 = sign(y2 - y1)

    swaped = 0
    if dy > dx:
        tmp = dx
        dx = dy
        dy = tmp
        swaped = 1

    e = 2 * dy - dx
    i = 1
    dots = []
    steps = 0

    while i <= dx + 1:
        dot = [x, y, color]
        dots.append(dot)

        x_buf = x
        y_buf = y

        while e > 0:
            if swaped:
                x = x + s1
            else:
                y = y + s2

            e = e - 2 * dx

        if swaped:
            y = y + s2
        else:
            x = x + s1

        e = e + 2 * dy

        if step_count:
            if (x_buf != x) and (y_buf != y):
                steps += 1

        i += 1

    if step_count:
        return steps
    else:
        return dots


def bresenham_float(p1, p2, color, step_count=False):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]

    if x2 - x1 == 0 and y2 - y1 == 0:
        return [[x1, y1, color]]

    x = x1
    y = y1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    s1 = sign(x2 - x1)
    s2 = sign(y2 - y1)

    if dy > dx:
        tmp = dx
        dx = dy
        dy = tmp
        swaped = 1
    else:
        swaped = 0

    m = dy / dx
    e = m - 0.5
    i = 1

    dots = []
    steps = 0

    while i <= dx + 1:
        dot = [x, y, color]
        dots.append(dot)

        x_buf = x
        y_buf = y

        while e >= 0:
            if swaped:
                x = x + s1
            else:
                y = y + s2

            e = e - 1

        if swaped:
            y = y + s2
        else:
            x = x + s1

        e = e + m

        if step_count:
            if not((x_buf == x and y_buf != y) or
                    (x_buf != x and y_buf == y)):
                steps += 1

        i += 1

    if step_count:
        return steps
    else:
        return dots


def choose_color(color, intens):
    return color + (intens, intens, intens)


def bresenham_smooth(p1, p2, color, step_count=False):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]

    if (x2 - x1 == 0) and (y2 - y1 == 0):
        return [[x1, y1, color]]

    x = x1
    y = y1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    s1 = sign(x2 - x1)
    s2 = sign(y2 - y1)

    swaped = 0
    if dy > dx:
        tmp = dx
        dx = dy
        dy = tmp
        swaped = 1

    intens = 255

    m = dy / dx
    e = intens / 2

    m *= intens
    w = intens - m

    dots = [[x, y, choose_color(color, round(e))]]

    i = 1

    steps = 0

    while i <= dx:
        x_buf = x
        y_buf = y

        if e < w:
            if swaped:
                y += s2
            else:
                x += s1
            e += m
        else:
            x += s1
            y += s2

            e -= w

        dot = [x, y, choose_color(color, round(e))]

        dots.append(dot)

        if step_count:
            if not ((x_buf == x and y_buf != y) or
                    (x_buf != x and y_buf == y)):
                steps += 1

        i += 1

    if step_count:
        return steps
    else:
        return dots


def dda_method(p1, p2, color, step_count=False):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]

    if (x2 - x1 == 0) and (y2 - y1 == 0):
        return [[x1, y1, color]]

    dx = x2 - x1
    dy = y2 - y1

    l = abs(dy)
    if abs(dx) >= abs(dy):
        l = abs(dx)

    dx /= l
    dy /= l

    x = round(x1)
    y = round(y1)

    dots = [[round(x), round(y), color]]

    i = 1
    steps = 0

    while i < l:
        x += dx
        y += dy

        dot = [round(x), round(y), color]

        dots.append(dot)

        if step_count:
            if not((round(x + dx) == round(x) and round(y + dy) != round(y)) or
                   (round(x + dx) != round(x) and round(y + dy) == round(y))):
                steps += 1

        i += 1

    if step_count:
        return steps
    else:
        return dots


def wu(p1, p2, color, step_count=False):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]

    if (x2 - x1 == 0) and (y2 - y1 == 0):
        return [[x1, y1, color]]

    dx = x2 - x1
    dy = y2 - y1

    m = 1
    step = 1
    intens = 255

    dots = []
    steps = 0

    if fabs(dy) > fabs(dx):
        if dy != 0:
            m = dx / dy
        m1 = m

        if y1 > y2:
            m1 *= -1
            step *= -1

        y_end = round(y2) - 1 if (dy < dx) else (round(y2) + 1)

        for y_cur in range(round(y1), y_end, step):
            d1 = x1 - floor(x1)
            d2 = 1 - d1

            if not d1 or not d2:
                d1 = d2 = 0.5

            dot1 = [int(x1) + 1, y_cur, choose_color(color, (fabs(d2) * intens))]
            dot2 = [int(x1), y_cur, choose_color(color, (fabs(d1) * intens))]

            if step_count and y_cur < y2:
                if int(x1) != int(x1 + m):
                    steps += 1

            dots.append(dot1)
            dots.append(dot2)

            x1 += m1

    else:
        if dx != 0:
            m = dy / dx

        m1 = m
        x_end = 0

        if x1 > x2:
            step *= -1
            m1 *= -1
            if dy == dx:
                x_end -= 5

        x_end += round(x2) - 1 if (dy > dx) else (round(x2) + 1)

        for x_cur in range(round(x1), x_end, step):
            d1 = y1 - floor(y1)
            d2 = 1 - d1

            if not d1 or not d2:
                d1 = d2 = 0.5

            dot1 = [x_cur, int(y1) + 1, choose_color(color, (fabs(d2) * intens))]
            dot2 = [x_cur, int(y1), choose_color(color, (fabs(d1) * intens))]

            if step_count and x_cur < x2:
                if int(y1) != int(y1 + m):
                    steps += 1

            dots.append(dot1)
            dots.append(dot2)

            y1 += m1

    if step_count:
        return steps
    else:
        return dots


def lib_method(p1, p2, color):
    p_1 = to_canva(p1)
    p_2 = to_canva(p2)
    canvas_win.create_line(p_1[0], p_1[1], p_2[0], p_2[1], fill=color.hex, tag='line')


# нарисовать линию
def draw_line(dots):
    global xy_history, line_history
    for dot in dots:
        x, y = to_canva(dot[0:2])
        point = [x, y, dot[2]]
        canvas_win.create_polygon([x, y], [x, y + 1], [x + 1, y + 1], [x + 1, y], fill=point[2].hex, tag='line')
    xy_history.append(xy_current)
    line_history.append(dots)
    canvas_win.delete('dot1', 'dot2')


def time_go():
    spectra_win, spectra_x, spectra_y, spectra_width, spectra_angle = spectra_1_win(PLUS)
    spectra_1_but = Button(spectra_win, text="Засечь время", font="AvantGardeC 14", borderwidth=0,
                           command=lambda: time_measure(spectra_width, spectra_angle, spectra_x, spectra_y))
    spectra_1_but.place(x=35, y=206, width=170, height=26)

    spectra_win.mainloop()


def time_measure(width, angle, center_x, center_y):
    time_mes = []

    try:
        line_len = float(width.get())
        angle_spin = float(angle.get())
        center_x = int(center_x.get())
        center_y = int(center_y.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Неверно введены координаты")
        return

    if line_len <= 0:
        messagebox.showerror("Ошибка", "Длина должна быть неотрицательна")
        return

    if angle_spin <= 0:
        messagebox.showerror("Ошибка", "Угол должен быть неотрицателен")
        return

    for i in range(0, 6):
        res_time = 0

        for _ in range(20):
            time_start = 0
            time_end = 0

            p1 = [center_x, center_y]
            spin = 0

            while spin <= 2 * pi:
                x2 = p1[0] + cos(spin) * line_len
                y2 = p1[1] + sin(spin) * line_len

                p2 = [x2, y2]

                time_start += time.time()
                parse_methods(p1, p2, i, draw=False)
                time_end += time.time()

                spin += radians(angle_spin)

            res_time += (time_end - time_start)
            clean_canvas()

        time_mes.append(res_time / 20)

    plt.figure(figsize=(14, 6))

    plt.title(f"Замеры времени для различных методов\n"
              f"[длина отрезка = {line_len} и угол = {angle_spin}˚]")

    positions = np.arange(6)
    methods = ["Брезенхем (int)", "Брезенхем (float)", "Брезенхем (сглаживание)",
               "ЦДА", "Ву", "Библиотечная"]
    plt.xticks(positions, methods)

    plt.ylabel("Время")
    plt.bar(positions, time_mes, align="center", alpha=1)

    plt.show()


def steps_go():
    spectra_win, spectra_x, spectra_y, spectra_width = spectra_1_win(MINUS)
    spectra_1_but = Button(spectra_win, text="Засечь ступенчатость", font="AvantGardeC 14", borderwidth=0,
                           command=lambda: steps_measure(spectra_width, spectra_x, spectra_y))
    spectra_1_but.place(x=35, y=206, width=170, height=26)

    spectra_win.mainloop()


def steps_measure(width, center_x, center_y):
    try:
        line_len = float(width.get())
        center_x = int(center_x.get())
        center_y = int(center_y.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Неверно введены координаты")
        return

    if line_len <= 0:
        messagebox.showerror("Ошибка", "Длина линии должна быть выше нуля")
        return

    p1 = [center_x, center_y]

    spin = 0

    angle_spin = [i for i in range(0, 91, 2)]

    dda_steps = []
    wu_steps = []
    bres_int_steps = []
    bres_float_steps = []
    bres_smooth_steps = []

    while spin <= pi / 2 + 0.01:
        x2 = p1[0] + cos(spin) * line_len
        y2 = p1[1] + sin(spin) * line_len

        p2 = [x2, y2]

        dda_steps.append(dda_method(p1, p2, (255, 255, 255), step_count=True))
        wu_steps.append(wu(p1, p2, (255, 255, 255), step_count=True))
        bres_int_steps.append(bresenham_int(p1, p2, (255, 255, 255), step_count=True))
        bres_float_steps.append(bresenham_float(p1, p2, (255, 255, 255), step_count=True))
        bres_smooth_steps.append(bresenham_smooth(p1, p2, (255, 255, 255), step_count=True))

        spin += radians(2)

    plt.figure(figsize=(15, 6))

    plt.title(f"Замеры ступенчатости для различных методов\n"
              f"[длина отрезка = {line_len}]")

    plt.xlabel("Угол (в градусах)")
    plt.ylabel("Количество ступенек")

    plt.plot(angle_spin, dda_steps, label="ЦДА")
    plt.plot(angle_spin, wu_steps, label="Ву")
    plt.plot(angle_spin, bres_float_steps, "-.", label="Брезенхем (float/int)")
    plt.plot(angle_spin, bres_smooth_steps, ":", label="Брезенхем\n(сглаживание)")

    plt.xticks(np.arange(91, step=5))
    plt.legend()

    plt.show()


# построить пучок по центру, длине и углу - окошко
def spectra_1_win(angle_param):
    param_win = Tk()
    param_win.title("Построить пучок")
    param_win['bg'] = "grey"
    param_win.geometry("240x250+400+250")
    param_win.resizable(False, False)

    coord_lbl = Label(param_win, text="Координаты центра", bg="pink", font="AvantGardeC 14", fg='black')
    coord_lbl.place(x=35, y=20, width=170, height=20)

    center_x_lbl = Label(param_win, text="X", bg="lightgrey", font="AvantGardeC 14", fg='black')
    center_x_lbl.place(x=35, y=48, width=80, height=20)
    center_x = Entry(param_win, font="AvantGardeC 14", bg='white', fg='black',
                     borderwidth=0, insertbackground='black', justify='center')
    center_x.insert(END, '0')
    center_x.place(x=35, y=70, width=81, height=20)

    center_y_lbl = Label(param_win, text="Y", bg="lightgrey", font="AvantGardeC 14", fg='black')
    center_y_lbl.place(x=123, y=48, width=80, height=20)
    center_y = Entry(param_win, font="AvantGardeC 14", bg='white', fg='black',
                     borderwidth=0, insertbackground='black', justify='center')
    center_y.insert(END, '0')
    center_y.place(x=123, y=70, width=81, height=20)

    width_lbl = Label(param_win, text="Длина", bg="pink", font="AvantGardeC 14", fg='black')
    width_lbl.place(x=35, y=104, width=170, height=18)
    width_spktr = Entry(param_win, font="AvantGardeC 14", bg='white', fg='black',
                        borderwidth=0, insertbackground='black', justify='center')
    width_spktr.insert(END, '200')
    width_spktr.place(x=35, y=124, width=170, height=20)

    if angle_param:
        angle_lbl = Label(param_win, text="Угол", bg="pink", font="AvantGardeC 14", fg='black')
        angle_lbl.place(x=35, y=148, width=170, height=18)
        angle_spktr = Entry(param_win, font="AvantGardeC 14", bg='white', fg='black',
                            borderwidth=0, insertbackground='black', justify='center')
        angle_spktr.insert(END, '1')
        angle_spktr.place(x=35, y=168, width=170, height=20)

        return param_win, center_x, center_y, width_spktr, angle_spktr

    return param_win, center_x, center_y, width_spktr


# построить пучок
def build_spectra_1(width, angle, x, y, option):
    try:
        line_len = float(width.get())
        angle_spin = float(angle.get())
        center_x = int(x.get())
        center_y = int(y.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Неверно введены параметры построения")
        return

    if line_len <= 0:
        messagebox.showerror("Ошибка", "Длина должна быть неотрицательна")
        return

    if angle_spin <= 0:
        messagebox.showerror("Ошибка", "Угол должен быть неотрицателен")
        return

    p1 = [center_x, center_y]
    spin = 0
    spin_deg = 0
    points = []

    while spin_deg < 360:

        x2 = p1[0] + cos(pi * (spin_deg) / 180) * line_len
        y2 = p1[1] + sin(pi * (spin_deg) / 180) * line_len

        p2 = [x2, y2]


        if spin_deg == 45:
            pass
            # print(cos(radians(spin_deg)), sin(radians(45)))

        spin_deg += angle_spin
        parse_methods(p1, p2, option)
        spin += angle_spin

        # чтобы удалился весь пучок при undo, а не каждый луч по отдельности
        point = line_history.pop()
        points.append(point)

    line_history.append(points)


# связать кнопку и экранчик для построения пучка
def spectra_1_go(option):
    spectra_win, spectra_x, spectra_y, spectra_width, spectra_angle = spectra_1_win(PLUS)
    spectra_1_but = Button(spectra_win, text="Построить", font="AvantGardeC 14", borderwidth=0,
                           command=lambda: build_spectra_1(spectra_width, spectra_angle, spectra_x, spectra_y, option))
    spectra_1_but.place(x=35, y=206, width=170, height=26)

    spectra_win.mainloop()


def draw_point(ev_x, ev_y, point, click_):
    if len(point):
        global x1_entry, y1_entry, x2_entry, y2_entry

        if click_:
            x, y = ev_x, ev_y
        else:
            x, y = to_canva([point[0], point[1]])

        if option.get() == 1:
            x1_entry.delete(0, END)
            y1_entry.delete(0, END)
            x1_entry.insert(0, "%d" % point[0])
            y1_entry.insert(0, "%d" % point[1])
            canvas_win.delete('dot1')
            canvas_win.create_oval(x - 2, y - 2, x + 2, y + 2,
                                   outline='grey', fill='pink', activeoutline='lightgreen', width=2, tag='dot1')
        elif option.get() == 2:
            x2_entry.delete(0, END)
            y2_entry.delete(0, END)
            x2_entry.insert(0, "%d" % point[0])
            y2_entry.insert(0, "%d" % point[1])
            canvas_win.delete('dot2')
            canvas_win.create_oval(x - 2, y - 2, x + 2, y + 2,
                                   outline='grey', fill='pink', activeoutline='lightgreen', width=2, tag='dot2')


# определение и запись координат точки по клику
def click(event):
    if event.x < 0 or event.x > WIN_WIDTH * win_k or event.y < 0 or event.y > WIN_HEIGHT * win_k:
        return
    point = to_coords([event.x, event.y])
    draw_point(event.x, event.y, point, 1)


# отрисовать отрезов без сохранения в историю
def draw_without_history(dots):
    for dot in dots:
        x, y = to_canva(dot[0:2])
        point = [x, y, dot[2]]
        canvas_win.create_polygon([x, y], [x, y + 1],
                                  [x + 1, y + 1], [x + 1, y],
                                  fill=point[2].hex, tag='line')


# отрисовка всех отрезков (для undo)
def draw_all_lines(array_dots):
    for dots in array_dots:
        if isinstance(dots[0][0], int):
            draw_without_history(dots)
        else:
            draw_all_lines(dots)


# откат
def undo():
    global xy_current, xy_history, line_history

    if len(line_history) == 0 or len(xy_history) == 0:
        messagebox.showerror("Внимание", "Достигнуто исходное состояние")
        return

    canvas_win.delete('line', 'coord')

    line_history.pop()
    draw_all_lines(line_history)

    xy_current = xy_history[-1]
    draw_axes()
    xy_history.pop()


# оси координат и сетка
def draw_axes():
    canvas_win.create_line(0, size / 2, size - 2, size / 2, fill='grey',
                           width=1, arrow=LAST, activefill='lightgreen', arrowshape="10 20 6")
    canvas_win.create_line(size / 2, size, size / 2, 2, fill='grey',
                           width=1, arrow=LAST, activefill='lightgreen', arrowshape="10 20 6")

    s = int(size)
    j = 0
    for i in range(0, s, s // 16):
        canvas_win.create_line(i, s / 2 - 5, i, s / 2 + 5, fill='pink', width=2)
        canvas_win.create_line(i, 0, i, s, fill='grey', width=1, dash=(1, 9))
        canvas_win.create_text(i, s // 2 + 20, text=f'{"%.2f" % xy_current[j]}' if i - SIZE // 2 else '',
                               fill='grey', tag='coord', font="AvantGardeC 10")

        canvas_win.create_line(s / 2 - 5, i, s / 2 + 5, i, fill='pink', width=2)
        canvas_win.create_line(0, i, s, i, fill='grey', width=1, dash=(1, 9))
        canvas_win.create_text(s // 2 - 20, i, text=f'{"%.2f" % xy_current[16 - j]}' if i - SIZE // 2 else '',
                               fill='grey', tag='coord', font="AvantGardeC 10")

        j += 1

    canvas_win.create_text(s - 20, s // 2 + 20, text='X', font="AvantGardeC 14", fill='grey')
    canvas_win.create_text(s // 2 + 20, 20, text='Y', font="AvantGardeC 14", fill='grey')


# растягивание окна
def config(event):
    if event.widget == win:
        global win_x, win_y, win_k, m, size, coord_center

        win_x = win.winfo_width()/WIN_WIDTH
        win_y = (win.winfo_height() + 35)/WIN_HEIGHT
        win_k = min(win_x, win_y)

        size = SIZE * win_k
        m = size / (2 * border + ten_percent)

        canvas_win.place(x=300 * win_x, y=0 * win_y, width=size, height=size)

        # координаты
        center_lbl.place(x=33 * win_x, y=28 * win_y, width=235 * win_x, height=24 * win_y)
        x1_lbl.place(x=33 * win_x, y=58 * win_y, width=110 * win_x, height=18 * win_y)
        y1_lbl.place(x=158 * win_x, y=58 * win_y, width=110 * win_x, height=18 * win_y)
        x1_entry.place(x=33 * win_x, y=77 * win_y, width=110 * win_x, height=20 * win_y)
        y1_entry.place(x=158 * win_x, y=77 * win_y, width=110 * win_x, height=20 * win_y)
        dot1.place(x=2 * win_x, y=68 * win_y)

        x2_lbl.place(x=33 * win_x, y=103 * win_y, width=110 * win_x, height=18 * win_y)
        y2_lbl.place(x=158 * win_x, y=103 * win_y, width=110 * win_x, height=18 * win_y)
        x2_entry.place(x=33 * win_x, y=122 * win_y, width=110 * win_x, height=20 * win_y)
        y2_entry.place(x=158 * win_x, y=122 * win_y, width=110 * win_x, height=20 * win_y)
        dot2.place(x=2 * win_x, y=113 * win_y)

        # выбор метода
        method_lbl.place(x=33 * win_x, y=210 * win_y, width=235 * win_x, height=23 * win_y)
        method_combo.place(x=33 * win_x, y=236 * win_y, width=235 * win_x, height=25 * win_y)

        # цвет фона и отрезка
        clr.place(x=33 * win_x, y=273 * win_y, width=235 * win_x, height=21 * win_y)
        bgc.place(x=33 * win_x, y=298 * win_y, width=235 * win_x, height=21 * win_y)

        # построить
        bld.place(x=33 * win_x, y=336 * win_y, width=235 * win_x, height=25 * win_y)

        # построить пучки
        spectra_lbl.place(x=33 * win_x, y=440 * win_y, width=235 * win_x, height=24 * win_y)
        sp1.place(x=33 * win_x, y=467 * win_y, width=235 * win_x, height=32 * win_y)

        # сравнения
        measure_lbl.place(x=30 * win_x, y=520 * win_y, width=235 * win_x, height=24 * win_y)
        tim.place(x=30 * win_x, y=547 * win_y, width=110 * win_x, height=32 * win_y)
        grd.place(x=156 * win_x, y=547 * win_y, width=110 * win_x, height=32 * win_y)

        # условие
        con.place(x=30 * win_x, y=650 * win_y, width=235 * win_x, height=28 * win_y)
        # откат
        und.place(x=30 * win_x, y=680 * win_y, width=109 * win_x, height=28 * win_y)
        # к начальным условиям
        bgn.place(x=157 * win_x, y=680 * win_y, width=109 * win_x, height=28 * win_y)

        coord_center = [size / 2, size / 2]

        canvas_win.delete('all')
        draw_axes()


# изменение цвета фона
def change_bg_color():
    global canvas_bg
    canvas_bg = colorchooser.askcolor()
    canvas_win.configure(bg=cu.Color(canvas_bg[1]))


# изменение цвета отрезка
def choose_line_color():
    global current_color
    current_color = colorchooser.askcolor()


# при нажатии буквы q будет переключать радиобаттон (для быстрого задания концов отрезка)
def change_option_click(event):
    global option
    if option.get() == 1:
        option.set(2)
    elif option.get() == 2:
        option.set(1)


#  отчистака канваса
def clean_canvas():
    line_history.append([])
    canvas_win.delete('line', 'dot1', 'dot2')
    draw_axes()


# Окно tkinter
win = Tk()
win['bg'] = 'grey'
win.geometry("%dx%d" % (WIN_WIDTH, WIN_HEIGHT))
win.title("Лабораторная работа #3")

# переменная для радиобаттона
option = IntVar()
option.set(1)

# Канвас
canvas_bg = ((255, 255, 255), "#ffffff")
canvas_win = Canvas(win, bg=cu.Color(canvas_bg[1]))

# Подписи функционала
center_lbl = Label(text="Координаты отрезков", bg='pink', font="AvantGardeC 14", fg='black')

x1_lbl = Label(text="X1", bg='lightgrey', font="AvantGardeC 14", fg='black')
y1_lbl = Label(text="Y1", bg='lightgrey', font="AvantGardeC 14", fg='black')
x1_entry = Entry(font="AvantGardeC 14", bg='white', fg='black',
                 borderwidth=0, insertbackground='black', justify='center')
y1_entry = Entry(font="AvantGardeC 14", bg='white', fg='black',
                 borderwidth=0, insertbackground='black', justify='center')
x1_entry.insert(END, 0)
y1_entry.insert(END, 0)
dot1 = Radiobutton(variable=option, value=1, bg="grey", activebackground="grey", highlightbackground="grey")

x2_lbl = Label(text="X2", bg='lightgrey', font="AvantGardeC 14", fg='black')
y2_lbl = Label(text="Y2", bg='lightgrey', font="AvantGardeC 14", fg='black')
x2_entry = Entry(font="AvantGardeC 14", bg='white', fg='black',
                 borderwidth=0, insertbackground='black', justify='center')
y2_entry = Entry(font="AvantGardeC 14", bg='white', fg='black',
                 borderwidth=0, insertbackground='black', justify='center')
x2_entry.insert(END, 250)
y2_entry.insert(END, 250)
dot2 = Radiobutton(variable=option, value=2, bg="grey", activebackground="grey", highlightbackground="grey")

method_lbl = Label(text="Алгоритм", bg='pink', font="AvantGardeC 14", fg='black')
method_combo = ttk.Combobox(win, state='readonly', values=["Брезенхем (целые)", "Брезенхем (вещ)",
                            "Брезенхем (устран. ступ.)", "ЦДА", "Ву", "Библиотечный"])
method_combo.current(0)

spectra_lbl = Label(text="Построить пучок", bg='pink', font="AvantGardeC 14", fg='black')
measure_lbl = Label(text="Сравнить", bg='pink', font="AvantGardeC 14", fg='black')

# Список точек
line_history = []  # история координат отрезков

xy_current = [-400, -350, -300, -250, -200, -150, -100, -50,
              0, 50, 100, 150, 200, 250, 300, 350, 400]
xy_history = [xy_current]  # история координат на оси


# Кнопки
bld = Button(text="Построить отрезок", font="AvantGardeC 14",
             borderwidth=0, command=lambda: parse_line(method_combo.current()))
sct = Button(text="Построить", font="AvantGardeC 14",
             borderwidth=0)
tim = Button(text="Время", font="AvantGardeC 12",
             borderwidth=0, command=lambda: time_go())
grd = Button(text="Ступенчатость", font="AvantGardeC 12",
             borderwidth=0, command=lambda: steps_go())
con = Button(text="Условие задачи", font="AvantGardeC 14",
             borderwidth=0, command=lambda: messagebox.showinfo("Задание", TASK + AUTHOR))
bgn = Button(text="Сброс", font="AvantGardeC 14",
             borderwidth=0, command=lambda: clean_canvas())
und = Button(text="↩", font="AvantGardeC 14",
             borderwidth=0, command=lambda: undo())
sp1 = Button(text="по длине и углу", font="AvantGardeC 12",
             borderwidth=0, command=lambda: spectra_1_go(method_combo.current()))
clr = Button(text="Цвет отрезка", font="AvantGardeC 14",
             borderwidth=0, command=lambda: choose_line_color())
bgc = Button(text="Цвет фона", font="AvantGardeC 14",
             borderwidth=0, command=lambda: change_bg_color())

win_x = win_y = 1  # коэффициенты масштабирования окна по осям
win_k = 1  # коэффициент масштабирования окна (для квадратизации)
size = SIZE  # текущая длина/ширина (они равны) канваса
border = WIDTH  # граница (максимальная видимая координата на канвасе)
ten_percent = 0  # 10% от величины границы
m = size * win_k / border  # коэффициент масштабирования канваса
coord_center = [400, 400]  # центр координат (в координатах канваса)

m_board = 1  # коэффициент масштабирования при изменении масштаба канваса

current_color = (0, 0, 0)

win.bind("<Configure>", config)
win.bind("q", change_option_click)
canvas_win.bind('<1>', click)


# Меню
menu = Menu(win)
add_menu = Menu(menu)
add_menu.add_command(label='О программе и авторе',
                     command=lambda: messagebox.showinfo('О программе и авторе', TASK + AUTHOR))
add_menu.add_command(label='Выход', command=exit)
menu.add_cascade(label='Help', menu=add_menu)
win.config(menu=menu)

win.mainloop()
