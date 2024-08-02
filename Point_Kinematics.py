from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, \
        QLabel, QMessageBox, QSpinBox, QRadioButton, QButtonGroup
from PyQt6.QtGui import QPalette, QLinearGradient, QColor, QFont
import sys
from PyQt6.QtCore import Qt
import pyqtgraph as pg
from sympy import sympify, diff, simplify, atan2, powdenest, evalf
from sympy import sqrt as symsqrt
from math import atan2 as matan2
from math import sqrt

x_axis = pg.InfiniteLine(angle=90, movable=False)
y_axis = pg.InfiniteLine(angle=0, movable=False)

px_expr = None
py_expr = None
derivative_x = None
derivative_y = None
double_derivative_x = None
double_derivative_y = None
full_speed = None
full_acceleration = None
acceleration_tau = None
acceleration_norm = None
available = False
available_point = False
coords_x = []
coords_y = []

def calculate_it():
    global coords_x, coords_y
    coords_x.clear()
    coords_y.clear()
    coords_x = []
    coords_y = []
    x_expr = root.controls.to_solve1.text()
    y_expr = root.controls.to_solve2.text()

    global px_expr, py_expr, derivative_x, derivative_y, double_derivative_x, double_derivative_y, full_speed, \
        full_acceleration, acceleration_tau, acceleration_norm
    global available

    px_expr = sympify(x_expr)
    py_expr = sympify(y_expr)

    derivative_x = simplify(diff(px_expr, 't'))
    derivative_y = simplify(diff(py_expr, 't'))

    root.controls.deriv11.setText(str(derivative_x).replace('**', '^'))
    root.controls.deriv12.setText(str(derivative_y).replace('**', '^'))

    double_derivative_x = simplify(diff(derivative_x, 't'))
    double_derivative_y = simplify(diff(derivative_y, 't'))

    full_speed = simplify(powdenest(symsqrt((derivative_x ** 2) + (derivative_y ** 2)), force=True))
    root.controls.deriv1.setText(str(full_speed).replace('**', '^'))

    root.controls.deriv21.setText(str(double_derivative_x).replace('**', '^'))
    root.controls.deriv22.setText(str(double_derivative_y).replace('**', '^'))

    full_acceleration = simplify(powdenest(symsqrt((double_derivative_x ** 2) + (double_derivative_y ** 2)),\
                                           force=True))
    root.controls.deriv2.setText(str(full_acceleration).replace('**', '^'))

    acceleration_tau = (diff(full_speed, 't'))
    root.controls.deriv2tau.setText(str(acceleration_tau).replace('**', '^'))

    acceleration_norm = simplify(full_speed * diff(atan2(derivative_y, derivative_x), 't'))
    root.controls.deriv2norm.setText(str(acceleration_norm).replace('**', '^'))

    t = 0
    while t <= root.gcontrols.cbox.value():
        coords_x.append(float(px_expr.subs('t', t)))
        coords_y.append(float(py_expr.subs('t', t)))
        t += 0.1

    root.ssplot.splot.clear()

    # Добавление графических элементов на график
    root.ssplot.splot.addItem(x_axis)
    root.ssplot.splot.addItem(y_axis)

    root.ssplot.splot.plot(coords_x, coords_y, pen='b')
    available = True

    x_min = min(coords_x)
    x_max = max(coords_x)
    y_min = min(coords_y)
    y_max = max(coords_y)

    # Вычисление центральных точек по осям X и Y
    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2

    # Вычисление половины ширины и высоты графика
    x_half_range = (x_max - x_min) / 2
    y_half_range = (y_max - y_min) / 2

    # Установка диапазонов значений по осям X и Y для центрирования графика
    root.ssplot.splot.setXRange(x_center - x_half_range, x_center + x_half_range)
    root.ssplot.splot.setYRange(y_center - y_half_range, y_center + y_half_range)


def calculate_in_timepoint():
    global available, available_point
    if root.controls.t1.text() == "":
        QMessageBox.warning(None, "Нет данных", "Вы не ввели искомую точку времени.")
    elif not available:
        QMessageBox.warning(None, "Нет данных", "Вы не провели анализ траектории движения точки.")
    else:
        value = float(root.controls.t1.text())
        root.controls.xt.setText("{:.3f}".format(px_expr.subs('t', value).evalf(), 3))
        root.controls.yt.setText("{:.3f}".format(py_expr.subs('t', value).evalf(), 3))
        root.controls.derivt11.setText("{:.3f}".format(derivative_x.subs('t', value).evalf(), 3))
        root.controls.derivt12.setText("{:.3f}".format(derivative_y.subs('t', value).evalf(), 3))
        root.controls.derivt21.setText("{:.3f}".format(double_derivative_x.subs('t', value).evalf(), 3))
        root.controls.derivt22.setText("{:.3f}".format(double_derivative_y.subs('t', value).evalf(), 3))
        root.controls.derivt2.setText("{:.3f}".format(full_acceleration.subs('t', value).evalf(), 3))
        root.controls.derivt1.setText("{:.3f}".format(full_speed.subs('t', value).evalf(), 3))
        root.controls.derivt2taut.setText("{:.3f}".format(acceleration_tau.subs('t', value).evalf(), 3))
        acc_norm = acceleration_norm.subs('t', value).evalf()
        root.controls.derivt2normt.setText("{:.3f}".format(acc_norm, 3))
        if acc_norm != 0:
            radius_R = abs((full_speed.subs('t', value) ** 2) / acceleration_norm.subs('t', value).evalf())
            root.controls.radius.setText("{:.3f}".format(radius_R, 3))
        else:
            root.controls.radius.setText("Infinity")
        available_point = True
        make_arrows()


def clear_all():
    root.controls.xt.setText("")
    root.controls.yt.setText("")
    root.controls.derivt11.setText("")
    root.controls.derivt12.setText("")
    root.controls.derivt21.setText("")
    root.controls.derivt22.setText("")
    root.controls.derivt2.setText("")
    root.controls.derivt1.setText("")
    root.controls.derivt2taut.setText("")
    root.controls.derivt2normt.setText("")
    root.controls.radius.setText("")
    root.controls.deriv1.setText("")
    root.controls.deriv2.setText("")
    root.controls.deriv11.setText("")
    root.controls.deriv12.setText("")
    root.controls.deriv21.setText("")
    root.controls.deriv22.setText("")
    root.controls.deriv2tau.setText("")
    root.controls.deriv2norm.setText("")
    root.controls.t1.setText("")
    root.ssplot.splot.clear()
    root.ssplot.splot.addItem(x_axis)
    root.ssplot.splot.addItem(y_axis)
    global available, available_point
    available = False
    available_point = False


def clear_point():
    global available_point
    available_point = False
    root.controls.xt.setText("")
    root.controls.yt.setText("")
    root.controls.derivt11.setText("")
    root.controls.derivt12.setText("")
    root.controls.derivt21.setText("")
    root.controls.derivt22.setText("")
    root.controls.derivt2.setText("")
    root.controls.derivt1.setText("")
    root.controls.derivt2taut.setText("")
    root.controls.derivt2normt.setText("")
    root.controls.radius.setText("")
    root.ssplot.splot.clear()
    root.ssplot.splot.addItem(x_axis)
    root.ssplot.splot.addItem(y_axis)
    global coords_x, coords_y
    root.ssplot.splot.plot(coords_x, coords_y, pen='b')


def make_arrows():
    global available, available_point
    if available_point and available:
        root.ssplot.splot.clear()
        root.ssplot.splot.addItem(x_axis)
        root.ssplot.splot.addItem(y_axis)
        global coords_x, coords_y
        root.ssplot.splot.plot(coords_x, coords_y, pen='b')

        point = pg.ScatterPlotItem(size=7, pen=pg.mkPen(None), brush=pg.mkBrush('r'))
        root.ssplot.splot.addItem(point)
        x, y = float(root.controls.xt.text()), float(root.controls.yt.text())
        point.setData(x=[x], y=[y])

        if root.gcontrols.btn1.isChecked():
            Vxt = float(root.controls.derivt11.text())
            Vyt = float(root.controls.derivt12.text())
            if Vxt and Vyt:
                make_arrow(x, x + Vxt, y, y, 'g')
                make_arrow(x, x, y, y + Vyt, 'g')
                make_arrow(x, x + Vxt, y, y + Vyt, '#00db6a')
            elif Vxt:
                make_arrow(x, x + Vxt, y, y, '#00db6a')
            elif Vyt:
                make_arrow(x, x, y, y + Vyt, '#00db6a')

        if root.gcontrols.btn2.isChecked():
            axt = float(root.controls.derivt21.text())
            ayt = float(root.controls.derivt22.text())
            if axt and ayt:
                make_arrow(x, x + axt, y, y, 'y')
                make_arrow(x, x, y, y + ayt, 'y')
                make_arrow(x, x + axt, y, y + ayt, '#ffa500')
            elif axt:
                make_arrow(x, x + axt, y, y, '#ffa500')
            elif ayt:
                make_arrow(x, x, y, y + ayt, '#ffa500')

        if root.gcontrols.btn3.isChecked():
            global px_expr, py_expr
            # (-3f(x) + 4f(x + h) - f(x + 2h)) / (2h)
            h = 0.05
            fxh = float(px_expr.subs('t', float(root.controls.t1.text()) + h).evalf())
            fx2h = float(px_expr.subs('t', float(root.controls.t1.text()) + 2 * h).evalf())
            fyh = float(py_expr.subs('t', float(root.controls.t1.text()) + h).evalf())
            fy2h = float(py_expr.subs('t', float(root.controls.t1.text()) + 2 * h).evalf())
            dx = (-3 * x + 4 * fxh - fx2h) / 2 * h
            dy = (-3 * y + 4 * fyh - fy2h) / 2 * h
            hypo = sqrt(dx ** 2 + dy ** 2)
            atau = float(root.controls.derivt2taut.text())
            anorm = float(root.controls.derivt2normt.text())
            if atau:
                make_arrow(x, x + atau * (dx / hypo), y, y + atau * (dy / hypo), '#e5be01')
            if anorm:
                make_arrow(x, x - anorm * (dy / hypo), y, y + anorm * (dx / hypo), '#964b00')


def make_arrow(x, xt, y, yt, color):
    root.ssplot.splot.plot([x, xt], [y, yt], pen={'color': color, 'width': 2})


class SamPlot(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.splot = pg.PlotWidget()
        self.splot.setBackground('w')

        self.splot.setMouseEnabled(x=True, y=True)
        self.splot.setMenuEnabled(False)
        self.splot.showGrid(True, True)

        self.setStyleSheet("border: 1px solid orange")

        self.splot.setLabel('left', 'Y Axis')
        self.splot.setLabel('bottom', 'X Axis')
        self.splot.setAspectLocked()

        # Добавление графических элементов на график
        self.splot.addItem(x_axis)
        self.splot.addItem(y_axis)

        layout = QHBoxLayout()
        layout.addWidget(self.splot)
        self.setLayout(layout)
        self.setMinimumWidth(775)


class SamControls(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        layout = QGridLayout()

        self.lbl_options = QLabel("Параметры траектории движения")
        self.lbl_options.setFont(QFont("Times new roman", 10))
        self.lbl_options.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_options.setMaximumHeight(30)

        lbl_solve1 = QLabel("x")
        lbl_solve1.setMaximumHeight(15)
        lbl_solve1.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        lbl_solve2 = QLabel("y")
        lbl_solve2.setMaximumHeight(15)
        lbl_solve2.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.to_solve1 = QLineEdit()
        self.to_solve2 = QLineEdit()

        self.to_solve1.textChanged.connect(clear_all)
        self.to_solve2.textChanged.connect(clear_all)

        lbl_deriv11 = QLabel("Vx")
        lbl_deriv11.setMaximumHeight(15)
        lbl_deriv11.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        lbl_deriv12 = QLabel("Vy")
        lbl_deriv12.setMaximumHeight(15)
        lbl_deriv12.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.deriv11 = QLineEdit()
        self.deriv12 = QLineEdit()

        self.deriv11.setReadOnly(True)
        self.deriv12.setReadOnly(True)

        lbl_deriv1 = QLabel("V")
        lbl_deriv1.setMaximumHeight(15)
        lbl_deriv1.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.deriv1 = QLineEdit()

        self.deriv1.setReadOnly(True)

        lbl_deriv21 = QLabel("ax")
        lbl_deriv21.setMaximumHeight(15)
        lbl_deriv21.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        lbl_deriv22 = QLabel("ay")
        lbl_deriv22.setMaximumHeight(15)
        lbl_deriv22.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.deriv21 = QLineEdit()
        self.deriv22 = QLineEdit()

        self.deriv21.setReadOnly(True)
        self.deriv22.setReadOnly(True)

        lbl_deriv2 = QLabel("a")
        lbl_deriv2.setMaximumHeight(15)
        lbl_deriv2.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.deriv2 = QLineEdit()

        self.deriv2.setReadOnly(True)

        lbl_derivtau = QLabel("a𝜏")
        lbl_derivtau.setMaximumHeight(15)
        lbl_derivtau.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        lbl_derivnorm = QLabel("an")
        lbl_derivnorm.setMaximumHeight(15)
        lbl_derivnorm.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.deriv2tau = QLineEdit()
        self.deriv2norm = QLineEdit()

        self.deriv2tau.setReadOnly(True)
        self.deriv2norm.setReadOnly(True)

        self.do_it = QPushButton("Рассчитать уравнения")
        self.do_it.setFont(QFont("Times new roman", 14))
        self.do_it.setMaximumHeight(50)
        self.do_it.clicked.connect(calculate_it)

        self.t1_form = QWidget()
        self.lbl_t1 = QLabel("t = ")
        self.lbl_t1.setFont(QFont("Times new roman"))
        self.t1 = QLineEdit()
        self.t1.textChanged.connect(clear_point)
        self.t1.setMaximumWidth(50)
        micro_layout = QHBoxLayout()
        micro_layout.addWidget(self.lbl_t1)
        micro_layout.addWidget(self.t1)
        self.t1_form.setLayout(micro_layout)
        self.t1_form.setMaximumSize(100, 75)

        self.solve_point = QPushButton("Рассчитать для точки")
        self.solve_point.setFont(QFont("Times new roman"))
        self.solve_point.setMaximumHeight(50)
        self.solve_point.clicked.connect(calculate_in_timepoint)

        lbl_xt = QLabel("x(t)")
        lbl_xt.setMaximumHeight(15)
        lbl_xt.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        lbl_yt = QLabel("y(t)")
        lbl_yt.setMaximumHeight(15)
        lbl_yt.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.xt = QLineEdit()
        self.yt = QLineEdit()

        self.xt.setReadOnly(True)
        self.yt.setReadOnly(True)

        lbl_drivt11 = QLabel("Vx(t)")
        lbl_drivt11.setMaximumHeight(15)
        lbl_drivt11.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        lbl_drivt12 = QLabel("Vy(t)")
        lbl_drivt12.setMaximumHeight(15)
        lbl_drivt12.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.derivt11 = QLineEdit()
        self.derivt12 = QLineEdit()

        self.derivt11.setReadOnly(True)
        self.derivt12.setReadOnly(True)

        lbl_derivt1 = QLabel("V(t)")
        lbl_derivt1.setMaximumHeight(15)
        lbl_derivt1.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.derivt1 = QLineEdit()

        self.derivt1.setReadOnly(True)

        lbl_drivt21 = QLabel("ax(t)")
        lbl_drivt21.setMaximumHeight(15)
        lbl_drivt21.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        lbl_drivt22 = QLabel("ay(t)")
        lbl_drivt21.setMaximumHeight(15)
        lbl_drivt22.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.derivt21 = QLineEdit()
        self.derivt22 = QLineEdit()

        self.derivt21.setReadOnly(True)
        self.derivt22.setReadOnly(True)

        lbl_derivt2 = QLabel("a(t)")
        lbl_derivt2.setMaximumHeight(15)
        lbl_derivt2.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.derivt2 = QLineEdit()

        self.derivt2.setReadOnly(True)

        lbl_derivtaut = QLabel("a𝜏(t)")
        lbl_derivtaut.setMaximumHeight(15)
        lbl_derivtaut.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        lbl_derivnormt = QLabel("an(t)")
        lbl_derivnormt.setMaximumHeight(15)
        lbl_derivnormt.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.derivt2taut = QLineEdit()
        self.derivt2normt = QLineEdit()

        self.derivt2taut.setReadOnly(True)
        self.derivt2normt.setReadOnly(True)

        self.rad_form = QWidget()
        self.radius = QLineEdit()
        self.radius.setReadOnly(True)
        self.radius.setMinimumHeight(20)
        micro_layout2 = QHBoxLayout()
        lbl_radius = QLabel("ρ = ")
        lbl_radius.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        micro_layout2.addWidget(lbl_radius)
        micro_layout2.addWidget(self.radius)
        self.rad_form.setLayout(micro_layout2)
        self.rad_form.setMaximumWidth(100)

        layout.addWidget(self.lbl_options, 0, 0, 1, 2)
        layout.addWidget(lbl_solve1, 1, 0)
        layout.addWidget(lbl_solve2, 1, 1)
        layout.addWidget(self.to_solve1, 2, 0)
        layout.addWidget(self.to_solve2, 2, 1)
        layout.addWidget(lbl_deriv11, 3, 0)
        layout.addWidget(lbl_deriv12, 3, 1)
        layout.addWidget(self.deriv11, 4, 0)
        layout.addWidget(self.deriv12, 4, 1)
        layout.addWidget(lbl_deriv1, 5, 0, 1, 2)
        layout.addWidget(self.deriv1, 6, 0, 1, 2)
        layout.addWidget(lbl_deriv21, 7, 0)
        layout.addWidget(lbl_deriv22, 7, 1)
        layout.addWidget(self.deriv21, 8, 0)
        layout.addWidget(self.deriv22, 8, 1)
        layout.addWidget(lbl_deriv2, 9, 0, 1, 2)
        layout.addWidget(self.deriv2, 10, 0, 1, 2)
        layout.addWidget(lbl_derivtau, 11, 0)
        layout.addWidget(lbl_derivnorm, 11, 1)
        layout.addWidget(self.deriv2tau, 12, 0)
        layout.addWidget(self.deriv2norm, 12, 1)
        layout.addWidget(self.do_it, 13, 0, 1, 2)
        layout.addWidget(self.t1_form, 14, 0)
        layout.addWidget(self.solve_point, 14, 1)
        layout.addWidget(lbl_xt, 15, 0)
        layout.addWidget(lbl_yt, 15, 1)
        layout.addWidget(self.xt, 16, 0)
        layout.addWidget(self.yt, 16, 1)
        layout.addWidget(lbl_drivt11, 17, 0)
        layout.addWidget(lbl_drivt12, 17, 1)
        layout.addWidget(self.derivt11, 18, 0)
        layout.addWidget(self.derivt12, 18, 1)
        layout.addWidget(lbl_drivt21, 19, 0)
        layout.addWidget(lbl_drivt22, 19, 1)
        layout.addWidget(self.derivt21, 20, 0)
        layout.addWidget(self.derivt22, 20, 1)
        layout.addWidget(lbl_derivt1, 21, 0)
        layout.addWidget(lbl_derivt2, 21, 1)
        layout.addWidget(self.derivt1, 22, 0)
        layout.addWidget(self.derivt2, 22, 1)
        layout.addWidget(lbl_derivtaut, 23, 0)
        layout.addWidget(lbl_derivnormt, 23, 1)
        layout.addWidget(self.derivt2taut, 24, 0)
        layout.addWidget(self.derivt2normt, 24, 1)
        layout.addWidget(self.rad_form, 25, 0, 1, 2)

        self.setLayout(layout)
        self.setMinimumSize(240, 450)
        self.setMaximumWidth(310)


class SamGraphicsControls(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()

        self.btn1 = QRadioButton("Скорость")
        self.btn2 = QRadioButton("Ускорение")
        self.btn3 = QRadioButton("Ускорение 𝜏 и n")

        self.btn1.setChecked(True)

        self.btn_group = QButtonGroup()
        self.btn_group.addButton(self.btn1)
        self.btn_group.addButton(self.btn2)
        self.btn_group.addButton(self.btn3)
        self.btn_group.buttonToggled.connect(make_arrows)

        self.lbl_time = QLabel("Рассчётное время (в секундах): ")
        self.lbl_time.setMaximumWidth(175)

        self.cbox = QSpinBox()
        self.cbox.setMaximumWidth(40)
        self.cbox.setValue(15)

        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.btn3)
        layout.addWidget(self.lbl_time)
        layout.addWidget(self.cbox)
        self.setLayout(layout)

        self.setMinimumHeight(40)
        self.setMaximumHeight(45)


class SamRoot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Кинематика точки")
        layout = QGridLayout()

        self.controls = SamControls()
        self.ssplot = SamPlot()
        self.gcontrols = SamGraphicsControls()

        # Создаем градиентный фон
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(215, 150, 150))  # Начальный цвет градиента
        gradient.setColorAt(1, QColor(150, 150, 215))  # Конечный цвет градиента

        # Устанавливаем градиентный фон для окна
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), gradient)
        self.setPalette(palette)

        layout.addWidget(self.controls, 0, 0, 2, 1)
        layout.addWidget(self.ssplot, 0, 1)
        layout.addWidget(self.gcontrols, 1, 1)
        self.center = QWidget()
        self.center.setLayout(layout)
        self.setCentralWidget(self.center)
        self.resize(1200, 650)
        self.setMinimumHeight(450)
        self.setMinimumWidth(1150)
        self.showMaximized()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    root = SamRoot()
    root.show()

    sys.exit(app.exec())