import socket
import pickle
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QLineEdit
import cli_output
import cli_input


# Returns the result of course details query in the following form:
# (0, err_message) or (1, results)
# depending on whether it was successful
def get_details(course_num):
    request = {'type': 'details', 'info': str(course_num)}
    info_bytes = pickle.dumps(request)
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
        with socket.socket() as sock:
            sock.connect((host, port))
            sock.sendall(info_bytes) # for pickled objects?
            print('Sent command: get_details')
            in_flo = sock.recv(999999)
            response = pickle.loads(in_flo)
        return response
    except Exception as ex:
        return (0, ex)

# Returns the result of course list query in the following form:
# (0,err_message) or (1,results) depending on whether it was successful
def get_search_res(search_input):
    request = {'type': 'courses', 'info':
        {'d': search_input[0], 'n': search_input[1],
        'a': search_input[2], 't': search_input[3]}}
    info_bytes = pickle.dumps(request)
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
        with socket.socket() as sock:
            data = []
            sock.connect((host, port))
            sock.sendall(info_bytes) # for pickled objects?
            print('Sent command: get_overviews')
            while True:
                packet = sock.recv(4096)
                if not packet:
                    break
                data.append(packet)
            response = pickle.loads(b"".join(data))
            #response = pickle.loads(in_flo)
        return response
    except Exception as ex:
        print(ex, file= sys.stderr)
        return (0, ex)
        #print(ex, file= sys.stderr)
        #sys.exit(1)

# Creates registrar app
class SearchApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Princeton University Class Search")
        self.setGeometry(100, 100, 850, 540)

        # Add widgets
        dept_search_label = QtWidgets.QLabel("Dept:")
        dept_search_label.setAlignment(QtCore.Qt.AlignRight)
        self.dept_search_textbox = QtWidgets.QLineEdit()

        num_search_label = QtWidgets.QLabel("Number:")
        num_search_label.setAlignment(QtCore.Qt.AlignRight)
        self.num_search_textbox = QtWidgets.QLineEdit()

        area_search_label = QtWidgets.QLabel("Area:")
        area_search_label.setAlignment(QtCore.Qt.AlignRight)
        self.area_search_textbox = QtWidgets.QLineEdit()

        title_search_label = QtWidgets.QLabel("Title:")
        title_search_label.setAlignment(QtCore.Qt.AlignRight)
        self.title_search_textbox = QtWidgets.QLineEdit()


        self.search_button = QtWidgets.QPushButton("Submit")
        QtWidgets.QLabel("Results:")
        self.results_list = QtWidgets.QListWidget()

        font = QFont('Courier', 10)
        self.results_list.setFont(font)

        # Set up layout
        layout = QtWidgets.QGridLayout()
        layout.setRowStretch(1, 1)
        layout.addWidget(dept_search_label, 0, 0)
        layout.addWidget(self.dept_search_textbox, 0, 1)
        layout.addWidget(num_search_label, 1, 0)
        layout.addWidget(self.num_search_textbox, 1, 1)
        layout.addWidget(area_search_label, 2, 0)
        layout.addWidget(self.area_search_textbox, 2, 1)
        layout.addWidget(title_search_label, 3, 0)
        layout.addWidget(self.title_search_textbox, 3, 1)



        # layout.addWidget(self.search_button, 0, 2, 4, 1)


        layout2 = QtWidgets.QGridLayout()
        layout2.addWidget(self.results_list)

        # Set main widget and layout
        main_widget = QtWidgets.QWidget()
        #main_widget.setLayout(layout)

        parent_grid = QtWidgets.QGridLayout()
        parent_grid.addLayout(layout, 0, 0)
        parent_grid.addLayout(layout2, 1, 0)
        main_widget.setLayout(parent_grid)
        parent_grid.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(main_widget)

        # Create a QShortcut for the Enter key
        shortcut = QtWidgets.QShortcut(QKeySequence('Return'), self)
        # Connect the activated signal of the QShortcut to
        # the clicked slot of the currently selected button
        shortcut.activated.connect(self.clicked_selected_button)

        # Connect signals to slots
        # self.search_button.clicked.connect(self.search)
        self.dept_search_textbox.textChanged.connect(self.search)
        self.num_search_textbox.textChanged.connect(self.search)
        self.area_search_textbox.textChanged.connect(self.search)
        self.title_search_textbox.textChanged.connect(self.search)
        #self.results_list.itemClicked.connect(self.handle_result_click)

        self.results_list.itemDoubleClicked.connect(
            self.handle_result_click)
        self.show()

        self.search() #display all courses

    def clicked_selected_button(self):
        # Get the currently selected button
        selected_widget = self.focusWidget()
        #print("Selected button: ", selectedWidget.text())
        # Check if the selected widget is a button
        if isinstance(selected_widget, QLineEdit):
            self.search()
        else: # isinstance(selectedWidget, QPushButton):
            # Emit the clicked signal of the selected button
            # selectedWidget.clicked.emit()
            selected_item = self.results_list.currentItem()
            self.handle_result_click(selected_item)


    def error_dialog_box(self, err_message):
        # Display error message in dialog box
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Server Error")
        msg_box.setText(err_message)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec()

    def search(self):
        # Perform search and display results
        dept = self.dept_search_textbox.text()
        num = self.num_search_textbox.text()
        area = self.area_search_textbox.text()
        title = self.title_search_textbox.text()
        search_terms = [dept, num, area, title]
        # Perform search here and add results to results_list


        self.results_list.clear()
        search_results = get_search_res(search_terms)
        if not search_results[0]:
            self.error_dialog_box(sys.argv[0]+': '
                + str(search_results[1]))
            return # If query failed, then no results to display
        output = cli_output.Output()
        cur_class = output.to_cli(search_results[1])

        for result in cur_class:

            #my_button = QtWidgets.QPushButton(result)

            # Result will be a list of form [num, , , title]
            item = QtWidgets.QListWidgetItem(result)
            self.results_list.addItem(item)


    def popup_details(self, course_num):
        #details = 'These are my course details!'
        details = get_details(course_num)
        if not details[0]:
            #If error occurred when generating details in regserver
            self.error_dialog_box(sys.argv[0]+ ': ' + str(details[1]))
            return
        outputter = cli_output.Output()
        details = outputter.courseid(details[1])
        popup = QtWidgets.QMessageBox()
        popup.setText(details)
        popup.exec()

    def handle_result_click(self, item):
        # Handle result click event here
        result_text = item.text()
        course_num = int(result_text[:5].replace(' ', ''))
        self.popup_details(course_num)


def main():
    user_input = cli_input.Input()
    user_input.parse_cli(sys.argv[1:])
    app = QtWidgets.QApplication([])
    search_app = SearchApp()
    search_app.show()
    app.exec_()

if __name__ == '__main__':
    main()
