import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSlider, QFrame, QGraphicsDropShadowEffect
)
# 新增 QtCore 导入
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QColor, QPainter, QPen


class CustomSlider(QSlider):
    def __init__(self, label_left, label_right, value, color):
        super().__init__(Qt.Orientation.Horizontal)
        self.label_left = label_left
        self.label_right = label_right
        self.value = value * 100  # 将 0 到 1 的值转换为 0 到 100
        self.color = color
        self.setRange(0, 100)
        self.setValue(int(self.value))
        self.setEnabled(False)
        # 增加控件的最小高度，预留阴影、圆环的空间
        self.setMinimumHeight(10) 
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
    
        # 调整横条的位置，使其居中显示
        groove_height = 10
        y_offset = (self.height() - groove_height) // 2
        groove_rect = self.rect().adjusted(0, y_offset, 0, -y_offset)
        radius = groove_height // 2  # 使用横条高度的一半作为半径，形成半圆形
        painter.fillRect(groove_rect, QColor('white'))  # 背景改为白色
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(self.color))
        painter.drawRoundedRect(groove_rect, radius, radius)
    
        # 计算点的位置
        x = int((self.value - self.minimum()) / (self.maximum() - self.minimum()) * self.width())
        y = self.height() // 2

        # 绘制阴影（模拟）
        shadow_radius = 8  # 阴影半径稍大
        shadow_color = QColor(0, 0, 0, 30)  # 半透明黑色
        painter.setBrush(shadow_color)
        painter.drawEllipse(x - shadow_radius, y - shadow_radius, 2 * shadow_radius, 2 * shadow_radius)

        # 绘制白色圆环
        ring_radius = 6
        painter.setPen(QPen(QColor('white'), 2))
        painter.setBrush(QColor('transparent'))
        painter.drawEllipse(x - ring_radius, y - ring_radius, 2 * ring_radius, 2 * ring_radius)


class DynamicPositionLabel(QLabel):
    def __init__(self, slider):
        super().__init__()
        self.slider = slider

    def update_position(self):
        x = int((self.slider.value - self.slider.minimum()) / (self.slider.maximum() - self.slider.minimum()) * self.slider.width())
        # 修改为直接使用 QPoint
        slider_pos = self.slider.mapToGlobal(QPoint(0, 0))
        container_pos = self.parent().mapToGlobal(QPoint(0, 0))
        x_relative = slider_pos.x() - container_pos.x() + x - 20  # 偏左一点
        y_relative = 0  # 假设标签在滑块上方，垂直位置为 0
        self.move(x_relative, y_relative)


def create_trait_slider(label_text, value, color):
    # 创建左右标签
    label_left = QLabel(label_text.split(' or ')[0] if ' or ' in label_text else 'Extraverted')
    label_right = QLabel(label_text.split(' or ')[1] if ' or ' in label_text else 'Introverted')

    slider = CustomSlider(label_left.text(), label_right.text(), value, color)
    # 设置滑块的最小宽度，你可以根据需要调整这个值
    slider.setMinimumWidth(300)
    # 如果你想设置最大宽度，也可以使用 setMaximumWidth 方法
    slider.setMaximumWidth(300) 

    # 创建显示百分比的标签
    percentage_label = DynamicPositionLabel(slider)
    if slider.value >= 50:
        percentage_label.setText(f"{slider.value}% {label_right.text()}")
    else:
        percentage_label.setText(f"{100 - slider.value}% {label_left.text()}")

    # 创建一个垂直布局来包含标签和滑块
    vbox = QVBoxLayout()
    vbox.addWidget(percentage_label)

    hbox = QHBoxLayout()
    hbox.addWidget(label_left)
    hbox.addWidget(slider)
    hbox.addWidget(label_right)

    vbox.addLayout(hbox)

    container = QWidget()
    container.setLayout(vbox)

    # 初始更新标签位置
    percentage_label.update_position()

    return container


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
        # 设置左侧框为圆角矩形并添加阴影
        left_widget.setStyleSheet("border-radius: 10px; background: white;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(3, 3)
        left_widget.setGraphicsEffect(shadow)

        # 新增五个变量代表每个横条的结果
        introverted_value = 0.4
        intuitive_value = 0.8
        feeling_value = 0.2
        judging_value = 0.6
        turbulent_value = 0.3

        # 中间特质滑条块
        center_block = QVBoxLayout()
        center_block.addWidget(QLabel("<b>Your Traits</b>"))
        center_block.addWidget(create_trait_slider("Extraverted or Introverted", introverted_value, "#2d9cdb"))
        center_block.addWidget(create_trait_slider("Sensing or Intuitive", intuitive_value, "#f4a261"))
        center_block.addWidget(create_trait_slider("Thinking or Feeling", feeling_value, "#2a9d8f"))
        center_block.addWidget(create_trait_slider("Perceiving or Judging", judging_value, "#9b5de5"))
        center_block.addWidget(create_trait_slider("Assertive or Turbulent", turbulent_value, "#ef476f"))
        center_widget = QWidget()
        center_widget.setLayout(center_block)
        # 设置中间框为圆角矩形并添加阴影
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
        # 设置右侧框为圆角矩形并添加阴影
        right_widget.setStyleSheet("border-radius: 10px; background: white;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(3, 3)
        right_widget.setGraphicsEffect(shadow)

        # 组合三个主块
        main_layout.addWidget(left_widget, 2)
        main_layout.addWidget(center_widget, 3)
        main_layout.addWidget(right_widget, 2)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MBTI_UI()
    window.show()
    sys.exit(app.exec())