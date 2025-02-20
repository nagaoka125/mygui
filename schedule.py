import sys
import json
import os
from PySide6 import QtWidgets as qw
from PySide6 import QtCore as qc
from PySide6.QtCore import QDate as qd
from PySide6.QtWidgets import QLineEdit as ql
from PySide6.QtWidgets import QCalendarWidget as qca
from PySide6.QtWidgets import QToolButton as qtb
from PySide6.QtWidgets import QStyle


datafile = "schedule.json"
btn_type = qw.QMessageBox.StandardButton

# カレンダーの取得データの設定
class date(ql):

  def __init__(self):
    super().__init__()
    self.qdate: qd | None = None
    self.setEnabled(False)

  def getDate(self) -> qd | None:
    return self.qdate

  def setDate(self, qdate: qd):
    self.qdate = qdate
    self.setText('{:0=4}-{:0=2}-{:0=2}'.format(qdate.year(),
                 qdate.month(), qdate.day()))

class sc_window(qw.QWidget):
  def __init__(self):
    super().__init__()
    self.load_schedule()

    # ウィンドウの設定
    self.setWindowTitle("予定設定")
    width, height = 800, 600
    self.resize(width, height)

    # グリッドレイアウトの設定
    self.layout: qw.QGridLayout = qw.QGridLayout(self)

    self.limit_date = ""
    self.title_text = ""
    self.main_text = ""

    self.btn_1 = qw.QPushButton("日付設定", self)
    self.btn_1.clicked.connect(self.click_set_date)
    self.btn_1.setMinimumSize(120, 50)
    self.btn_1.setMaximumSize(120, 50)
    self.layout.addWidget(self.btn_1, 0, 0)

    self.date_lab = qw.QLabel("", self)
    self.layout.addWidget(self.date_lab, 1, 0)

    self.btn_2 = qw.QPushButton("文章を設定", self)
    self.btn_2.clicked.connect(self.click_set_title)
    self.btn_2.setEnabled(False)
    self.btn_2.setMinimumSize(120, 50)
    self.btn_2.setMaximumSize(120, 50)
    self.layout.addWidget(self.btn_2, 0, 1)

    self.title_lab = qw.QLabel("タイトル設定", self)
    self.layout.addWidget(self.title_lab, 1, 1)

    self.tx_box = qw.QTextEdit("", self)
    self.tx_box.setPlaceholderText("ここにタイトルを入力")
    self.tx_box.textChanged.connect(self.change_text_box)
    self.tx_box.setMinimumSize(100, 50)
    self.tx_box.setMaximumSize(400, 100)
    self.layout.addWidget(self.tx_box, 2, 1)

    self.mtx_lab = qw.QLabel("本文設定", self)
    self.layout.addWidget(self.mtx_lab, 3, 1)

    self.mtx_box = qw.QTextEdit("", self)
    self.mtx_box.setPlaceholderText("ここに本文を入力")
    self.mtx_box.textChanged.connect(self.change_text_box)
    self.mtx_box.setMinimumSize(100, 50)
    self.mtx_box.setMaximumSize(400, 100)
    self.layout.addWidget(self.mtx_box, 4, 1)

    self.pre_btn = qw.QPushButton("プレビュー", self)
    self.pre_btn.clicked.connect(self.click_preview)
    self.pre_btn.setMinimumSize(120, 50)
    self.pre_btn.setMaximumSize(120, 50)
    self.layout.addWidget(self.pre_btn, 4, 0)

    self.pre_lab = qw.QLabel("どちらか設定して表示", self)
    self.layout.addWidget(self.pre_lab, 5, 0, 2, 1)  # 2列にまたがる

    self.reset_btn = qw.QPushButton("リセット", self)
    self.reset_btn.clicked.connect(self.click_reset)
    self.reset_btn.setMinimumSize(120, 50)
    self.reset_btn.setMaximumSize(120, 50)
    self.layout.addWidget(self.reset_btn, 7, 0)

    self.set_btn = qw.QPushButton("設定", self)
    self.set_btn.clicked.connect(self.click_set)
    self.set_btn.setMinimumSize(120, 50)
    self.set_btn.setMaximumSize(120, 50)
    self.layout.addWidget(self.set_btn, 7, 1)

    # カレンダーの設定
    self.entry = date()
    self.calendar: qca | None = None
    but_calendar = qtb()
    icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton)
    but_calendar.setIcon(icon)
    but_calendar.clicked.connect(self.click_set_date)

  # 日付設定ボタン

  def click_set_date(self):
    self.calendar = qca()
    qdate = self.entry.getDate()
    if qdate is not None:
      self.calendar.setSelectedDate(qdate)
    self.calendar.activated.connect(self.serect_date)
    self.calendar.show()

  def serect_date(self, qdate: qd):
    self.entry.setDate(qdate)
    if self.calendar is not None:
      self.calendar.hide()
      self.calendar.deleteLater()
    qdate_str = qdate.toString("yyyy年MM月dd日")
    self.limit_date = qdate_str
    self.date_lab.setText(qdate_str)

  # 文章設定
  def change_text_box(self):
    if self.tx_box.toPlainText().strip():
      self.btn_2.setEnabled(True)
    else: self.btn_2.setEnabled(False)

  def click_set_title(self):
    self.title_text = self.tx_box.toPlainText()
    self.main_text = self.mtx_box.toPlainText()

  # プレビュー
  def click_preview(self):
    text1 = self.limit_date
    text2 = self.title_text
    text3 = self.main_text
    pre_text = f"{text1}\n{text2}\n{text3}"
    self.pre_lab.setText(pre_text)

  # リセット
  def click_reset(self):
    self.limit_date = ""
    self.date_lab.setText(self.limit_date)
    self.title_text = ""
    self.tx_box.clear()
    self.mtx_box.clear()
    self.main_text = ""
    self.pre_lab.setText("どちらか設定して表示")

  def load_schedule(self):
    if os.path.exists(datafile):
      with open(datafile, 'r', encoding='utf-8') as file:
        self.schedule = json.load(file)
    else:
      self.schedule = []

  def add_schedule(self, date, title, mtext):
    self.schedule.append({
        'date': date,
        'title': title,
        'main': mtext
    })

  def click_set(self):
    date = self.limit_date
    title = self.title_text
    mtext = self.main_text

    # 日付、タイトルが設定されているか確認
    if not date or not title:
      msg_box = qw.QMessageBox()
      msg_box.setIcon(qw.QMessageBox.Icon.Warning)
      msg_box.setText("日付またはタイトルが設定されていません。")
      msg_box.setWindowTitle("警告")
      msg_box.setStandardButtons(btn_type.Yes | btn_type.No)
      msg_box.exec_()  # メッセージボックスを表示
      return  # 日付またはタイトルが空であれば終了

    else:
      try:
        with open(datafile, 'r', encoding='utf-8') as f:
          self.schedules = json.load(f)
      except (FileNotFoundError, json.JSONDecodeError):
        pass  # ファイルが存在しないか、空の場合は新しく作成
      self.add_schedule(date, title, mtext)
      self.click_reset()  # 入力フィールドをリセット
      with open(datafile, 'w') as file:
        json.dump(self.schedule, file)


if __name__ == "__main__":
  app = qw.QApplication(sys.argv)
  window = sc_window()
  window.show()
  sys.exit(app.exec())
