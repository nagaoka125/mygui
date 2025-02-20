import sys
from PySide6 import QtWidgets as qw
from schedule import sc_window
from show_schedule import ShowSchedule

datafile = "schedule.json"

class mainapp(qw.QWidget):
  def __init__(self):
    super().__init__()

    width = 800
    height = 600
    self.setWindowTitle("予定確認アプリ")
    # ウィンドウサイズを固定
    self.setFixedSize(width, height)

    self.app_lab = qw.QLabel("", self)
    self.lab_style = """QLabel {
            color:            #000000;
            font-size:        60px;     
        }"""
    self.app_lab.setStyleSheet(self.lab_style)
    self.app_lab.setText("予定確認アプリ")
    self.app_lab.setGeometry(width // 2 - 185, height // 10, 400, 70)

    self.check_sch_btn = qw.QPushButton("予定確認", self)
    self.check_sch_btn.clicked.connect(self.click_check_sch)
    self.check_sch_btn.setGeometry(width // 2 - 125, height // 2, 250, 75)

    self.add_sch_btn = qw.QPushButton("予定追加", self)
    self.add_sch_btn.clicked.connect(self.click_add_sch)
    self.add_sch_btn.setGeometry(width // 2 - 125, height // 2 + 100, 250, 75)

  def click_check_sch(self):
    try:
      schedule_window = ShowSchedule()
      schedule_window.show()
    except Exception as e:
      print(f"Error opening schedule window: {e}")

  def click_add_sch(self):
    try:
      self.schedule_window = sc_window()  # sc_windowのインスタンスを作成
      self.schedule_window.show()
    except Exception as e:
      print(f"Error opening schedule window: {e}")  # エラーハンドリング


if __name__ == "__main__":
  app = qw.QApplication(sys.argv)
  app_window = mainapp()
  app_window.show()
  sys.exit(app.exec())
