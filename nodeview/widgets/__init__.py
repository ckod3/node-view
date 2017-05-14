from PySide.QtCore import QRect, Qt
from PySide.QtGui import QLabel, QPainter, QColor, QBrush
from nodeview.node import Node


class PyNode(QLabel, Node):

    TEXT_PADDING = 5

    def __init__(self, name, graph, inputs=None, outputs=None, parent=None):
        self.node = Node(name, graph, inputs, outputs)
        QLabel.__init__(self, parent=parent)
        self.setFixedSize(
            self.node.geometry.bounding_rect.width,
            self.node.geometry.bounding_rect.height
        )

    def _paint_header(self, painter, rectangle):
        qrect = QRect(rectangle.x, rectangle.y, rectangle.width, rectangle.height)

        painter.setPen(QColor(125, 125, 110))
        painter.setBrush(QBrush(QColor(125, 125, 110)))
        painter.drawRect(qrect)

        painter.setBrush(Qt.NoBrush)
        painter.setPen(QColor(220, 220, 220))
        painter.drawText(
            qrect.adjusted(self.TEXT_PADDING, self.TEXT_PADDING, -self.TEXT_PADDING, -self.TEXT_PADDING),
            Qt.AlignLeft | Qt.AlignVCenter,
            self.node.name
        )

    def _paint_main(self, painter, rectangle):
        qrect = QRect(rectangle.x, rectangle.y, rectangle.width, rectangle.height)

        painter.setPen(QColor(155, 155, 140))
        painter.setBrush(QBrush(QColor(155, 155, 140)))
        painter.drawRect(qrect)

    def _paint_slot(self, painter, rectangle, slot):
        qrect = QRect(rectangle.x, rectangle.y, rectangle.width, rectangle.height)

        painter.setPen(QColor(200, 200, 180))
        painter.setBrush(QBrush(QColor(175, 175, 150)))
        painter.drawEllipse(qrect)

    def _paint_label(self, painter, rectangle, slot, is_input):
        qrect = QRect(rectangle.x, rectangle.y, rectangle.width, rectangle.height)

        align = Qt.AlignLeft if is_input else Qt.AlignRight

        painter.setBrush(Qt.NoBrush)
        painter.setPen(QColor(220, 220, 220))
        painter.drawText(
            qrect.adjusted(self.TEXT_PADDING, self.TEXT_PADDING, -self.TEXT_PADDING, -self.TEXT_PADDING),
            align | Qt.AlignVCenter,
            slot.name
        )

    def _paint(self, painter):
        self._paint_header(painter, self.node.geometry.header_rect)

        self._paint_main(painter, self.node.geometry.main_rect)

        for index, input_ in enumerate(self.node.inputs.values()):
            rectangle = self.node.geometry.input_slot_rects[index]
            self._paint_slot(painter, rectangle, input_)

            rectangle = self.node.geometry.input_label_rects[index]
            self._paint_label(painter, rectangle, input_, is_input=True)

        for index, output in enumerate(self.node.outputs.values()):
            rectangle = self.node.geometry.output_slot_rects[index]
            self._paint_slot(painter, rectangle, output)

            rectangle = self.node.geometry.output_label_rects[index]
            self._paint_label(painter, rectangle, output, is_input=False)

    def paintEvent(self, event):
        QLabel.paintEvent(self, event)
        painter = QPainter()
        painter.begin(self)
        self._paint(painter)
        painter.end()


if __name__ == '__main__':
    import sys
    from PySide.QtGui import QApplication
    from nodeview.graph import Graph

    app = QApplication(sys.argv)

    pynode = PyNode(
        "PyNode Demo",
        Graph("Graph"),
        ['Input A', 'Input B', 'Input C'],
        ['Output']
    )
    pynode.show()

    app.exec_()
