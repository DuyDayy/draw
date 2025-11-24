import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
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






#Này là fontend
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fast Trail Animation")
        self.resize(900, 750)

        layout = QVBoxLayout(self)

        self.figure = Figure()
        self.ax_x = self.figure.add_subplot(311)
        self.ax_y = self.figure.add_subplot(312)
        self.ax_traj = self.figure.add_subplot(313)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        form = QHBoxLayout()
        self.input_a = QLineEdit(); self.input_a.setPlaceholderText("a")
        self.input_b = QLineEdit(); self.input_b.setPlaceholderText("b")
        self.input_c = QLineEdit(); self.input_c.setPlaceholderText("c°")

        form.addWidget(QLabel("a=")); form.addWidget(self.input_a)
        form.addWidget(QLabel("b=")); form.addWidget(self.input_b)
        form.addWidget(QLabel("c°=")); form.addWidget(self.input_c)

        self.btn_start = QPushButton("Start Plot")
        self.btn_start.clicked.connect(self.start_plot)
        form.addWidget(self.btn_start)
        layout.addLayout(form)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 1000)
        self.slider.valueChanged.connect(self.slider_changed)
        self.slider.setEnabled(False)
        layout.addWidget(self.slider)

        self.btn_anim = QPushButton("Start Animation")
        self.btn_anim.clicked.connect(self.toggle_animation)
        self.btn_anim.setEnabled(False)
        layout.addWidget(self.btn_anim)

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_step)

        self.state = None
        self.t_val = 0
        self.direction = 1

    def start_plot(self):
        self.timer.stop()
        self.btn_anim.setText("Start Animation")

        a = float(self.input_a.text())
        b = float(self.input_b.text())
        c = float(self.input_c.text())

        self.figure.clear()
        self.figure.subplots_adjust(hspace=0.5)
        ax_x = self.figure.add_subplot(311)
        ax_y = self.figure.add_subplot(312)
        ax_traj = self.figure.add_subplot(313)

        self.state = setup_plot(self.figure, a, b, c, ax_x, ax_y, ax_traj)

        self.t_val = self.state["t_min"]
        self.slider.setValue(0)
        self.slider.setEnabled(True)
        self.btn_anim.setEnabled(True)
        self.canvas.draw_idle()

    def slider_changed(self):
        if self.state is None:
            return
        t_ratio = self.slider.value() / 1000
        t_val = self.state["t_min"] + t_ratio * (self.state["t_max"] - self.state["t_min"])
        update_plot(self.state, t_val)
        self.canvas.draw_idle()

    def toggle_animation(self):
        if self.state is None:
            return
        if self.timer.isActive():
            self.timer.stop()
            self.btn_anim.setText("Start Animation")
        else:
            self.timer.start(15)
            self.btn_anim.setText("Stop Animation")

    def animate_step(self):
        self.t_val += 0.05 * self.direction
        if self.t_val >= self.state["t_max"]:
            self.direction = -1
        if self.t_val <= self.state["t_min"]:
            self.direction = 1

        self.slider.blockSignals(True)
        ratio = (self.t_val - self.state["t_min"])/(self.state["t_max"]-self.state["t_min"])
        self.slider.setValue(int(ratio * 1000))
        self.slider.blockSignals(False)

        update_plot(self.state, self.t_val)
        self.canvas.draw_idle()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
