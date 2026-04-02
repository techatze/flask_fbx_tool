from pathlib import Path
import requests
from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QMainWindow, QTextEdit, QWidget, QFileDialog, QLabel, QTableWidget,
                               QTableWidgetItem, QApplication, QVBoxLayout, QHBoxLayout,
                               QPushButton, QListWidget, QComboBox, QTreeWidget, QTreeWidgetItem, QAbstractItemView)


BASE_URL = "http://127.0.0.1:5000"
PROCESS_MAP ={
    'Analyze FBX':'analyze',
    'Find Meshes':'find_meshes'
}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('FBX Processing Tool')

        self.completed_jobs = set()

        self.jobs = {}
        self.job_rows = {}
        self.job_status = {}
        self.job_results = {}
        self.row_to_job = {}

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)

        #layouts
        main_layout = QHBoxLayout()
        second_layout = QVBoxLayout()
        third_layout = QVBoxLayout()


        #widgets
        self.fbx_list = QListWidget()

        self.choose_process = QComboBox()
        self.choose_process.addItems(['','Analyze FBX','Find Meshes'])

        self.submit_all = QPushButton('Submit All')
        self.submit_all.clicked.connect(self.submit_all_button)

        self.submit_selected = QPushButton('Submit Selected')
        self.submit_selected.clicked.connect(self.submit_one_button)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabel('Scene Hierarchy')

        self.job_table = QTableWidget()
        self.job_table.setColumnCount(3)
        self.job_table.setHorizontalHeaderLabels(['File','Status','Result'])
        self.job_table.cellDoubleClicked.connect(self.on_row_double_click)
        self.job_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.clear_table = QPushButton('Clear Table')
        self.clear_table.clicked.connect(self.delete_table)

        self.clear_tree = QPushButton('Clear Tree Log')
        self.clear_tree.clicked.connect(self.delete_tree)

        #menu
        file_open = QAction('&Open',self)
        file_open.setStatusTip('Open new file')
        file_open.triggered.connect(self.show_dialog)

        menubar = self.menuBar()
        menu_file = menubar.addMenu('&File')
        menu_file.addAction(file_open)

        #GUI/Layout formatting
        second_layout.addWidget(self.fbx_list)
        second_layout.addWidget(self.choose_process)
        second_layout.addWidget(self.submit_all)
        second_layout.addWidget(self.submit_selected)

        third_layout.addWidget(self.job_table)
        third_layout.addWidget(self.clear_table)
        third_layout.addWidget(self.tree)
        third_layout.addWidget(self.clear_tree)

        main_layout.addLayout(second_layout)
        main_layout.addLayout(third_layout)


        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)


    def show_dialog(self):
        """Opens file browser and adds all .fbx files of a folder in QListWidget(self.fbx_list)."""
        self.fbx_list.clear()
        self.fbx_path = QFileDialog.getExistingDirectory(self,'Open File')
        self.assets_to_import = list(Path(self.fbx_path).glob('*.fbx'))

        if self.fbx_path:
            for fbx in self.assets_to_import:
                self.fbx_list.addItem(fbx.stem)



    def submit_all_button(self):
        process = PROCESS_MAP.get(self.choose_process.currentText())

        if not process:
            return

        for i in range(self.fbx_list.count()):
            file_name = self.assets_to_import[i]

            response = submit_job(str(file_name),process)

            job_id = response['job_id']

            row = self.job_table.rowCount()
            self.job_table.insertRow(row)

            self.job_rows[job_id] = row
            self.row_to_job[row] = job_id

            self.job_table.setItem(row,0,QTableWidgetItem(file_name.name))
            self.job_table.setItem(row,1,QTableWidgetItem('submitted'))
            self.job_table.setItem(row,2,QTableWidgetItem(""))

            self.jobs[job_id] = file_name.name


            if not self.timer.isActive():
                self.timer.start(2000)


    def submit_one_button(self):
        process = PROCESS_MAP.get(self.choose_process.currentText())

        if not process:
            return


        selected_file = self.fbx_list.currentRow()
        file_path=self.assets_to_import[selected_file]

        response = submit_job(str(file_path), process)

        job_id = response['job_id']

        row = self.job_table.rowCount()
        self.job_table.insertRow(row)

        self.job_rows[job_id] = row
        self.row_to_job[row] = job_id

        self.job_table.setItem(row, 0, QTableWidgetItem(file_path.name))
        self.job_table.setItem(row, 1, QTableWidgetItem('submitted'))
        self.job_table.setItem(row, 2, QTableWidgetItem(""))

        self.jobs[job_id] = file_path.name

        if not self.timer.isActive():
            self.timer.start(2000)


    def update_status(self):
        for job_id, file_name in self.jobs.items():
            data = get_status(job_id)
            status = data['status']

            if self.job_status.get(job_id) != status:
                self.job_status[job_id] = status

                row = self.job_rows[job_id]
                self.job_table.setItem(row, 1, QTableWidgetItem(status))

                if status == 'done':
                    result = data.get('result')

                    self.job_results[job_id] = result

                    if isinstance(result, list):
                        result_text = f"{len(result)} items"
                    else:
                        result_text = str(result)

                    self.job_table.setItem(row, 2, QTableWidgetItem(result_text))


    def populate_tree(self, lines):
        self.tree.clear()

        parents = {0: self.tree.invisibleRootItem()}

        for line in lines:
            depth = len(line) - len(line.lstrip(" "))

            text = line.strip()

            item = QTreeWidgetItem([text])

            parent = parents.get(depth -1, self.tree.invisibleRootItem())
            parent.addChild(item)

            parents[depth] = item

        self.tree.expandAll()


    def on_row_double_click(self,row,column):
        if column != 2:
            return

        job_id = self.row_to_job.get(row)

        if not job_id:
            return

        result = self.job_results.get(job_id)

        if not result:
            return

        self.populate_tree(result)


    def delete_table(self):
        self.timer.stop()
        self.job_table.setRowCount(0)



    def delete_tree(self):
        self.tree.clear()


def submit_job(file_path,process):
    response = requests.post(f'{BASE_URL}/submit',json={
        "file":file_path,
        "process":process
    })
    return response.json()


def get_status(job_id):
    response = requests.get(f'{BASE_URL}/status/{job_id}')
    return response.json()


app = QApplication([])
window = MainWindow()
window.show()
app.exec()