import numpy as np

def setup_plot(fig, a, b, c, ax_x, ax_y, ax_traj):

    fig.subplots_adjust(hspace=0.5)
    fig.tight_layout(rect=[0, 0, 1, 0.97])

    # ====== dữ liệu param ======
    t = np.linspace(0, 10, 800)
    x = a * np.sin(t)
    y = b * np.sin(t + np.deg2rad(c))

    # ====== line rỗng tạo trail ======
    line_x,  = ax_x.plot([], [], lw=2)
    line_y,  = ax_y.plot([], [], lw=2)
    line_xy, = ax_traj.plot([], [], lw=2, label="(x(t);y(t)) trail")

    # điểm chạy
    point_xy, = ax_traj.plot([], [], "ro")

    # ====== hệ trục cố định ======
    ax_x.set_xlim(t[0], t[-1])
    ax_x.set_ylim(-1.2*abs(a), 1.2*abs(a))

    ax_x.set_title(f"x(t) = {a}·sin(t)")


    ax_y.set_xlim(t[0], t[-1])
    ax_y.set_ylim(-1.2*abs(b), 1.2*abs(b))
    ax_y.set_title(f"y(t) = {b}·sin(t + {c}°)")


    ax_traj.set_xlim(-1.2*abs(a), 1.2*abs(a))
    ax_traj.set_ylim(-1.2*abs(b), 1.2*abs(b))
    ax_traj.set_title("Quỹ đạo y(x)")


    # =============================
    # 🚀 THÊM ĐƯỜNG GIẢI TÍCH y(x)
    # =============================
    # x từ -a đến a
    x_grid = np.linspace(-abs(a), abs(a), 600)
    x2_grid= np.linspace(abs(a), -abs(a), 600)

    # Ví dụ công thức Lissajous:
    # y = b * sin(arcsin(x/a) + c)
    c_rad = np.deg2rad(c)
    y_grid = b * np.sin(np.arcsin(x_grid / a) + c_rad)
    y2_grid= b * np.sin(np.pi - np.arcsin(x2_grid / a) + c_rad)
    x_grid=np.concatenate([x_grid, x2_grid])
    y_grid=np.concatenate([y_grid, y2_grid])

    # Vẽ line y(x) analytic
    line_analytic, = ax_traj.plot(x_grid, y_grid, 'r--', lw=1.8, label="(x;y(x)) trail")

    ax_traj.legend()

    return {
        "t": t,
        "x": x,
        "y": y,

        "trail_t": [],
        "trail_x": [],
        "trail_y": [],

        "line_x": line_x,
        "line_y": line_y,
        "line_xy": line_xy,
        "line_analytic": line_analytic,
        "point_xy": point_xy,

        "ax_x": ax_x,
        "ax_y": ax_y,
        "ax_traj": ax_traj,

        "t_min": float(t[0]),
        "t_max": float(t[-1])
    }


def update_plot(state, t_val):
    t = state["t"]
    x = state["x"]
    y = state["y"]

    idx = np.argmin(np.abs(t - t_val))
    if idx < 2:
        idx = 2

    # Thêm 1 điểm mới vào trail
    state["trail_t"].append(t[idx])
    state["trail_x"].append(x[idx])
    state["trail_y"].append(y[idx])

    # Cập nhật trail
    state["line_x"].set_data(state["trail_t"], state["trail_x"])
    state["line_y"].set_data(state["trail_t"], state["trail_y"])
    state["line_xy"].set_data(state["trail_x"], state["trail_y"])

    # Cập nhật điểm chạy
    state["point_xy"].set_data([x[idx]], [y[idx]])
