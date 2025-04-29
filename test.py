import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSlider, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPen


class CustomSlider(QSlider):
    def __init__(self, label_left, label_right, value, color):
        super().__init__(Qt.Orientation.Horizontal)
        self.label_left = label_left
        self.label_right = label_right
        self.color = color
        self.setRange(0, 100)
        self.setValue(int(value * 100))
        self.setEnabled(False)
        self.setMinimumHeight(10)  # 紧凑显示
        self.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                height: 10px;
                background: lightgray;
                border-radius: 5px;
            }}
            QSlider::handle:horizontal {{
                background: {color};
                width: 15px;
                border-radius: 7px;
            }}
        """)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        groove_height = 10
        y_offset = (self.height() - groove_height) // 2
        groove_rect = self.rect().adjusted(0, y_offset, 0, -y_offset)
        radius = groove_height // 2
        painter.fillRect(groove_rect, QColor('white'))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(self.color))
        painter.drawRoundedRect(groove_rect, radius, radius)

        x = int((self.value() - self.minimum()) / (self.maximum() - self.minimum()) * self.width())
        y = self.height() // 2

        shadow_radius = 8
        shadow_color = QColor(0, 0, 0, 30)
        painter.setBrush(shadow_color)
        painter.drawEllipse(x - shadow_radius, y - shadow_radius, 2 * shadow_radius, 2 * shadow_radius)

        ring_radius = 6
        painter.setPen(QPen(QColor('white'), 2))
        painter.setBrush(QColor('transparent'))
        painter.drawEllipse(x - ring_radius, y - ring_radius, 2 * ring_radius, 2 * ring_radius)


class MBTI_UI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MBTI 性格测试结果")
        self.resize(900, 400)

        main_layout = QHBoxLayout()

        # 左侧人格框
        left_block = QVBoxLayout()
        left_block.addWidget(QLabel("<b>Your Personality</b>"))
        left_block.addWidget(QLabel("Advocate (INFJ-T)"))
        left_block.addWidget(QLabel("👤 [形象图占位]"))
        left_block.addWidget(QLabel(
            "Advocates are quiet visionaries,\noften serving as inspiring\nand tireless idealists."))
        left_widget = QFrame()
        left_widget.setLayout(left_block)
        left_widget.setFrameShape(QFrame.Shape.Box)
        left_widget.setFrameShadow(QFrame.Shadow.Raised)
        left_widget.setStyleSheet("border-radius: 10px; background: white;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(3, 3)
        left_widget.setGraphicsEffect(shadow)

        # 五个性格维度
        introverted_value = 0.4
        intuitive_value = 0.8
        feeling_value = 0.2
        judging_value = 0.6
        turbulent_value = 0.3

        center_block = QVBoxLayout()
        # 增大标题字体大小
        title_label = QLabel("<b>Your Traits</b>")
        title_label.setStyleSheet("font-size: 16pt;")
        center_block.addWidget(title_label)

        # 添加灰色分割线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("color: lightgray;")
        center_block.addWidget(line)

        sliders_info = [
            ("Extraverted or Introverted", introverted_value, "#2d9cdb"),
            ("Sensing or Intuitive", intuitive_value, "#f4a261"),
            ("Thinking or Feeling", feeling_value, "#2a9d8f"),
            ("Perceiving or Judging", judging_value, "#9b5de5"),
            ("Assertive or Turbulent", turbulent_value, "#ef476f")
        ]

        for label_text, value, color in sliders_info:
            slider_widget = create_trait_slider(label_text, value, color)
            center_block.addWidget(slider_widget)

        center_widget = QWidget()
        center_widget.setLayout(center_block)
        center_widget.setStyleSheet("border-radius: 10px; background: white;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(3, 3)
        center_widget.setGraphicsEffect(shadow)

        # 右侧 Identity 块
        right_block = QVBoxLayout()
        right_block.addWidget(QLabel("<b>Identity</b>"))
        right_block.addWidget(QLabel(f"{turbulent_value * 100}% Turbulent"))
        right_block.addWidget(QLabel("💻 [图标占位]"))
        identity_desc = QLabel(
            "You're likely self-conscious,\nsensitive to stress,\nsuccess-driven, perfectionistic,\nand eager to improve.")
        identity_desc.setWordWrap(True)
        right_block.addWidget(identity_desc)
        right_widget = QWidget()
        right_widget.setLayout(right_block)
        right_widget.setStyleSheet("border-radius: 10px; background: white;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(3, 3)
        right_widget.setGraphicsEffect(shadow)

        main_layout.addWidget(left_widget, 2)
        main_layout.addWidget(center_widget, 3)
        main_layout.addWidget(right_widget, 2)

        self.setLayout(main_layout)


def create_trait_slider(label_text, value, color):
    label_left = label_text.split(' or ')[0] if ' or ' in label_text else 'Extraverted'
    label_right = label_text.split(' or ')[1] if ' or ' in label_text else 'Introverted'

    # 将左右小标签字体颜色改为灰色
    left_label = QLabel(label_left)
    left_label.setStyleSheet("color: gray;")
    right_label = QLabel(label_right)
    right_label.setStyleSheet("color: gray;")

    container = QWidget()
    vbox = QVBoxLayout(container)
    vbox.setContentsMargins(0, 0, 0, 0)
    vbox.setSpacing(0)

    slider = CustomSlider(label_left, label_right, value, color)
    slider.setMinimumWidth(300)
    slider.setMaximumWidth(300) 

    label_display = QLabel(container)
    label_display.setStyleSheet("font-size: 12pt; background: transparent;")
    label_display.adjustSize()

    # 设置初始文本
    current_val = slider.value()
    if current_val >= 50:
        label_display.setText(f'<b><span style="color:{color};">{current_val}%</span> <span style="color:black;">{label_right}</span></b>')
    else:
        label_display.setText(f'<b><span style="color:{color};">{100 - current_val}%</span> <span style="color:black;">{label_left}</span></b>')
    label_display.adjustSize()

    # 监听 slider 绘制完后移动 label
    def update_label_position():
        handle_offset = 7  # 小圆环半径（你的handle宽15px，所以半径是7左右）
        available_width = slider.width() - 2 * handle_offset
        x = handle_offset + int((slider.value() - slider.minimum()) / (slider.maximum() - slider.minimum()) * available_width)
        label_display.move(x - label_display.width() // 2 + 80, 0)

    update_label_position()

    hbox = QHBoxLayout()
    # 设置布局的左右边距，这里设置为 10，可以根据需要调整
    hbox.setContentsMargins(10, 0, 10, 0) 
    # 设置标签和滑块之间的间距，这里设置为 10，可以根据需要调整
    hbox.setSpacing(10) 
    hbox.addWidget(left_label)
    hbox.addWidget(slider)
    hbox.addWidget(right_label)

    vbox.addSpacing(label_display.height())  # 给上方留空间
    vbox.addLayout(hbox)

    return container


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MBTI_UI()
    window.show()
    sys.exit(app.exec())