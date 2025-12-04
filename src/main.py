import math
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")  # استفاده از بک‌اند مخصوص Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def calculate_and_plot():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())
    except ValueError:
        messagebox.showerror("خطا", "لطفاً ضرایب را به صورت عددی وارد کنید.")
        return

    if a == 0:
        messagebox.showerror("خطا", "برای تابع درجه دو، ضریب a نباید صفر باشد.")
        return

    # تعریف تابع
    def f(x):
        return a * x**2 + b * x + c

    # محاسبه رأس
    x_vertex = -b / (2 * a)
    y_vertex = f(x_vertex)

    # بازه x بر اساس رأس
    x_min = x_vertex - 10
    x_max = x_vertex + 10

    # تولید نقاط
    x_values = []
    y_values = []
    step = (x_max - x_min) / 400
    cur = x_min
    while cur <= x_max:
        x_values.append(cur)
        y_values.append(f(cur))
        cur += step

    # محاسبه دلتا و ریشه‌ها
    delta = b**2 - 4*a*c
    roots_text = ""
    roots = []

    if delta > 0:
        x1 = (-b + math.sqrt(delta)) / (2*a)
        x2 = (-b - math.sqrt(delta)) / (2*a)
        roots = [x1, x2]
        roots_text = f"دو ریشه حقیقی:\n x₁ = {x1:.4f}\n x₂ = {x2:.4f}"
    elif delta == 0:
        x0 = -b / (2*a)
        roots = [x0]
        roots_text = f"یک ریشه (مضاعف):\n x = {x0:.4f}"
    else:
        roots_text = "هیچ ریشه حقیقی ندارد (دلتا < 0)"

    # به‌روزرسانی اطلاعات در لیبل‌ها
    label_vertex_value.config(
        text=f"راس: ({x_vertex:.4f} , {y_vertex:.4f})"
    )
    label_delta_value.config(
        text=f"Δ = {delta:.4f}"
    )
    label_roots_value.config(text=roots_text)

    # رسم نمودار در شکل matplotlib
    fig.clear()
    ax = fig.add_subplot(111)

    # رسم منحنی
    ax.plot(x_values, y_values, label=f"y = {a}x² + {b}x + {c}")

    # رسم محور x و y
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)

    # علامت‌گذاری راس
    ax.scatter([x_vertex], [y_vertex])
    ax.annotate(
        f"V({x_vertex:.2f},{y_vertex:.2f})",
        (x_vertex, y_vertex),
        textcoords="offset points",
        xytext=(10, 10),
    )

    # علامت‌گذاری ریشه‌ها
    for r in roots:
        ax.scatter([r], [0])
        ax.annotate(
            f"{r:.2f}",
            (r, 0),
            textcoords="offset points",
            xytext=(5, -15),
        )

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("نمودار تابع درجه دو")
    ax.grid(True)
    ax.legend()

    fig.tight_layout()
    canvas.draw()


# ------------------ ساخت رابط گرافیکی ------------------

root = tk.Tk()
root.title("رسم تابع درجه دو (y = ax² + bx + c)")

# استفاده از فونت پیش‌فرض، که تو همه سیستم‌ها کار کنه
default_font = ("Tahoma", 10)

root.option_add("*Font", default_font)

main_frame = ttk.Frame(root, padding=10)
main_frame.grid(row=0, column=0, sticky="nsew")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# بخش ورودی ضرایب
coeff_frame = ttk.LabelFrame(main_frame, text="ضرایب تابع", padding=10)
coeff_frame.grid(row=0, column=0, sticky="ew")

ttk.Label(coeff_frame, text="a:").grid(row=0, column=0, padx=5, pady=5)
entry_a = ttk.Entry(coeff_frame, width=10)
entry_a.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(coeff_frame, text="b:").grid(row=0, column=2, padx=5, pady=5)
entry_b = ttk.Entry(coeff_frame, width=10)
entry_b.grid(row=0, column=3, padx=5, pady=5)

ttk.Label(coeff_frame, text="c:").grid(row=0, column=4, padx=5, pady=5)
entry_c = ttk.Entry(coeff_frame, width=10)
entry_c.grid(row=0, column=5, padx=5, pady=5)

# مقدارهای پیش‌فرض
entry_a.insert(0, "1")
entry_b.insert(0, "0")
entry_c.insert(0, "0")

btn_plot = ttk.Button(coeff_frame, text="رسم نمودار", command=calculate_and_plot)
btn_plot.grid(row=0, column=6, padx=10, pady=5)

# بخش اطلاعات تحلیلی (راس، دلتا، ریشه‌ها)
info_frame = ttk.LabelFrame(main_frame, text="اطلاعات تابع", padding=10)
info_frame.grid(row=1, column=0, sticky="ew", pady=10)

ttk.Label(info_frame, text="راس:").grid(row=0, column=0, sticky="w")
label_vertex_value = ttk.Label(info_frame, text="-")
label_vertex_value.grid(row=0, column=1, sticky="w", padx=5)

ttk.Label(info_frame, text="دلتا:").grid(row=1, column=0, sticky="w")
label_delta_value = ttk.Label(info_frame, text="-")
label_delta_value.grid(row=1, column=1, sticky="w", padx=5)

ttk.Label(info_frame, text="ریشه‌ها:").grid(row=2, column=0, sticky="nw")
label_roots_value = ttk.Label(info_frame, text="-", justify="left")
label_roots_value.grid(row=2, column=1, sticky="w", padx=5)

# بخش نمودار
plot_frame = ttk.LabelFrame(main_frame, text="نمودار", padding=10)
plot_frame.grid(row=2, column=0, sticky="nsew")

main_frame.rowconfigure(2, weight=1)
main_frame.columnconfigure(0, weight=1)
plot_frame.rowconfigure(0, weight=1)
plot_frame.columnconfigure(0, weight=1)

fig = Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=0, sticky="nsew")

# شروع حلقه اصلی
root.mainloop()
