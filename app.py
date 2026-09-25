import os
import subprocess
import sys
import pymupdf
import pandas as pd
from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,    
    QProgressBar,
    QRadioButton,
)
from convert import (pdf_to_txt, pdf_to_xlsx, pdf_to_docx, pdf_to_jpg, pdf_to_png)
from donation import open_donation_page

# ======= PROGRAM'S RUNING BUDDY! ======= #

OUTPUT_FOLDER = r"D:\Experiment\Result-Converted-Files"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

class PDFConverter(QWidget):

    def __init__(self):
        super().__init__()
        self.pdf_file = ""
        self.setWindowTitle("PDF to All Converter")
        self.resize(700, 400)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        title = QLabel("📄 PDF to All Converter")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:20px;font-weight:bold;")
        self.setStyleSheet("background-color: #f0f0f0;")
        self.file_label = QLabel("No File Selected")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_choose = QPushButton("Choose PDF File")
        self.btn_choose.clicked.connect(self.choose_file)

        self.CB_docx = QRadioButton("DOCX")
        self.CB_xlsx = QRadioButton("XLSX")
        self.CB_txt = QRadioButton("TXT")
        self.CB_png = QRadioButton("PNG")
        self.CB_jpg = QRadioButton("JPG")

        format_layout = QHBoxLayout()

        format_layout.addWidget(self.CB_docx)
        format_layout.addWidget(self.CB_xlsx)
        format_layout.addWidget(self.CB_txt)
        format_layout.addWidget(self.CB_png)
        format_layout.addWidget(self.CB_jpg)

        self.progress = QProgressBar()

        self.btn_convert = QPushButton("Convert")
        self.btn_convert.clicked.connect(self.convert_file)
        self.btn_donate = QPushButton("For Eat & Coffee Developer <3")
        self.btn_donate.setStyleSheet("""
            QPushButton { background-color: #757D6F; color: black; border-radius: 8px; padding: 8px; font-weight: bold; }
            QPushButton:hover { background-color: #EAE2D6; }
            """)
        self.btn_donate.clicked.connect(open_donation_page)
        

        main_layout.addWidget(self.btn_donate)
        main_layout.addWidget(title)
        main_layout.addWidget(self.file_label)
        main_layout.addWidget(self.btn_choose)
        main_layout.addLayout(format_layout)
        main_layout.addWidget(self.progress)
        main_layout.addWidget(self.btn_convert)

        self.setLayout(main_layout)

    def choose_file(self):

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Choose File",
            "",
            "PDF Files (*.pdf)"
        )

        if file_name:
            self.pdf_file = file_name
            self.file_label.setText(file_name)

    def convert_file(self):
        """Convert the selected PDF into all selected supported formats."""
        if not self.pdf_file:
            QMessageBox.warning(self, "Warning", "Please select a PDF file.")
            return

        converters = []
        if self.CB_docx.isChecked():
            converters.append(("DOCX", pdf_to_docx))
        if self.CB_xlsx.isChecked():
            converters.append(("XLSX", pdf_to_xlsx))
        if self.CB_txt.isChecked():
            converters.append(("TXT", pdf_to_txt))
        if self.CB_jpg.isChecked():
            converters.append(("JPG", pdf_to_jpg))
        if self.CB_png.isChecked():
            converters.append(("PNG", pdf_to_png))

        if not converters:
            QMessageBox.warning(
                self, "Warning", "Please select at least one output format."
            )
            return

        self.progress.setRange(0, len(converters))
        self.progress.setValue(0)
        self.btn_convert.setEnabled(False)
        try:
            for index, (format_name, converter) in enumerate(converters, start=1):
                converter(self.pdf_file, OUTPUT_FOLDER)
                self.progress.setValue(index)
        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to convert to {format_name}: {error}",
            )
        else:
            QMessageBox.information(self, "Success", "Conversion completed successfully!")
        finally:
            self.btn_result = QPushButton("See the Result")
            self.btn_convert.setEnabled(True)

    def open_result_folder(self):
        folder = os.path.abspath("Result-Converted-Files")

        if not os.path.exists(folder):
            os.makedirs(folder)
        subprocess.Popen(f'explorer "{folder}')

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = PDFConverter()
    window.show()
    sys.exit(app.exec())