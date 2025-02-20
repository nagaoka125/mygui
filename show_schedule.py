import sys
import json
from PySide6 import QtWidgets as qw
from PySide6.QtCore import Qt

datafile = "schedule.json"
btn_type = qw.QMessageBox.StandardButton

class ShowSchedule(qw.QWidget):
  def __init__(self):
    super().__init__()
    width, height = 400, 300
    self.resize(width, height)
    self.layout: qw.QVBoxLayout = qw.QVBoxLayout(self)
    self.setWindowTitle("予定一覧")
    self.refresh_schedule()

  def load_schedules(self):
    try:
      with open(datafile, 'r', encoding='utf-8') as f:
        schedules = json.load(f)
        return schedules
    except (FileNotFoundError, json.JSONDecodeError):
      return []

  # 前のウィジェットをクリア
  def refresh_schedule(self):
    for i in reversed(range(self.layout.count())):
      widget = self.layout.itemAt(i).widget()
      if widget is not None:
        widget.deleteLater()

    # 予定を取得して表示
    schedules = self.load_schedules()
    if not schedules:
      msg_box = qw.QMessageBox()
      msg_box.setIcon(qw.QMessageBox.Icon.Information)
      msg_box.setText("予定はありません")
      msg_box.setWindowTitle("情報")
      msg_box.setStandardButtons(btn_type.Yes | btn_type.No)
      msg_box.exec_()  # メッセージボックスを表示
      return

    else:
      for index, schedule in enumerate(schedules):
        schedule_widget = qw.QWidget(self)
        schedule_layout = qw.QHBoxLayout(schedule_widget)

        date = schedule['date']
        title = schedule['title']
        mtext = schedule['main']

        schedule_text = f"{date}\n{title}\n{mtext}"
        schedule_lab = qw.QLabel(schedule_text)
        schedule_lab.setMinimumSize(400, 75)
        schedule_lab.setMaximumSize(400, 100)

        delete_button = qw.QPushButton("完了")
        delete_button.clicked.connect(
            lambda checked, idx=index: self.delete_schedule(idx))

        schedule_layout.addWidget(schedule_lab)
        schedule_layout.addWidget(delete_button)
        self.layout.addWidget(schedule_widget)

        schedule_widget.setStyleSheet(
            "border: 1px solid; padding: 10px; margin: 5px;")

  # 指定されたインデックスの予定を削除
  def delete_schedule(self, index):
    schedules = self.load_schedules()
    if 0 <= index < len(schedules):
      del schedules[index]
      self.save_schedules(schedules)
      self.refresh_schedule()

  def save_schedules(self, schedules):
    with open(datafile, 'w', encoding='utf-8') as f:
      json.dump(schedules, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
  app = qw.QApplication(sys.argv)
  window = ShowSchedule()
  window.show()
  sys.exit(app.exec())
