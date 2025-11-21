import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from plot import setup_plot, update_plot
import numpy as np










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
