from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit, QComboBox, QHBoxLayout, QMessageBox
from PySide6.QtCore import QDate
import os
import re

class NamePage(QDialog):
    def __init__(self, on_data_entered_callback, parent=None):
        super().__init__(parent)
        
        try:
            os.makedirs('users')
        except:
            pass
        layout = QVBoxLayout(self)
        
        # Existing Users
        self.existing_users_label = QLabel("Usuários Existentes:")
        self.existing_users_combobox = QComboBox()
        self.existing_users_combobox.currentIndexChanged.connect(self.on_existing_user_selected)
        layout.addWidget(self.existing_users_label)
        layout.addWidget(self.existing_users_combobox)
        
        # Name
        self.name_label = QLabel("Insira seu nome:")
        self.name_input = QLineEdit()
        #self.name_input.setEditable(True)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        # self.populate_name_input()
        
        # Date of Birth
        self.dob_label = QLabel("Data de Nascimento:")
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDate(QDate.currentDate())
        layout.addWidget(self.dob_label)
        layout.addWidget(self.dob_input)
        
        # Race, Color, Ethnicity
        self.ethnicity_label = QLabel("Raça, Cor e Etnia:")
        self.ethnicity_input = QComboBox()
        self.ethnicity_input.addItems(["preto", "pardo", "branco", "indígena", "amarelo"])
        layout.addWidget(self.ethnicity_label)
        layout.addWidget(self.ethnicity_input)
        
        # Gender
        self.gender_label = QLabel("Gênero:")
        self.gender_input = QComboBox()
        self.gender_input.addItems(["masculino", "feminino", "outro"])
        layout.addWidget(self.gender_label)
        layout.addWidget(self.gender_input)
        
        # Ok Button
        self.ok_button = QPushButton("Enviar")
        layout.addWidget(self.ok_button)



        self.populate_existing_users()
        
        self.ok_button.clicked.connect(self.on_ok_clicked)
        self.on_data_entered = on_data_entered_callback
    def populate_existing_users(self):
        folder_pattern = re.compile(r"^(.+)_(\d{4}-\d{2}-\d{2})$")
        
        for folder_name in os.listdir(os.getcwd()+'/users'):
            if os.path.isdir(os.getcwd()+'/users/'+ folder_name):
                folder_match = folder_pattern.match(folder_name)
                if folder_match:
                    self.existing_users_combobox.addItem(folder_name)
    
    

    def on_existing_user_selected(self, index):
        if index == -1:
            return
        folder_name = 'users/' + self.existing_users_combobox.itemText(index)
        log_file_path = os.path.join(folder_name, "log.txt")
        if os.path.isfile(log_file_path):
            with open(log_file_path, 'r') as log_file:
                line = log_file.readlines()[1]
                name = line.split(',')[0].strip().split(': ')[1]
                dob = line.split(',')[1].strip().split(': ')[1]
                ethnicity = line.split(',')[2].strip().split(': ')[1]
                gender = line.split(',')[3].strip().split(': ')[1]

                self.name_input.setText(name)
                self.dob_input.setDate(QDate.fromString(dob, "yyyy-MM-dd"))
                index = self.ethnicity_input.findText(ethnicity)
                if index != -1:
                    self.ethnicity_input.setCurrentIndex(index)
                index = self.gender_input.findText(gender)
                if index != -1:
                    self.gender_input.setCurrentIndex(index)
    # def populate_name_input(self):
    #     pattern = re.compile(r"^(.+)_\d{4}-\d{2}-\d{2}$")
    #     for folder_name in os.listdir(os.getcwd()):
    #         match = pattern.match(folder_name)
    #         if match:
    #             username = match.group(1)
    #             qbox_items = [self.name_input.itemText(i) for i in range(self.name_input.count())]
    #             if username not in qbox_items:
    #                 self.name_input.addItem(username)


    def on_ok_clicked(self):
        name = self.name_input.text().strip()
        dob = self.dob_input.date().toString("yyyy-MM-dd")
        ethnicity = self.ethnicity_input.currentText()
        gender = self.gender_input.currentText()
        
        if name:
            self.on_data_entered(name, dob, ethnicity, gender)
            self.accept()
