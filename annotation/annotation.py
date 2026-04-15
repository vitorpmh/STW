from datetime import datetime
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QLabel, QSizePolicy,QSpacerItem,QDialog, QMessageBox
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, QTime, QTimer
import os 
import pandas as pd
import numpy as np

from zoom_class import ZoomableLabel
# DATASET_PATH = ("/home/vitorpmatias/Documentos/MESTRADO/TESE/TESE/"
#                 "paper_benchmark/data_manipulation/all_data_available.csv")
# DATASET_PATH = ('/home/vitorpmatias/Documentos/MESTRADO/TESE/TESE/annotation'
#                 '/non_annotated.csv')
# fair face
DATASET_PATH = ('/home/vitorpmatias/Documentos/MESTRADO/TESE/TESE/data/OpenData/FairFace.csv')

# LIST_OF_DATASETS = ['Faces 95']
MIN_NUM_PHOTOS = 1 # can be equal if =5 then persons with 5 photos will appear


from name_page import NamePage
from mw_ui import Ui_mw
class MainWindow(QMainWindow, Ui_mw):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app 
        self.name_page = NamePage(self.on_data_entered)
        if self.name_page.exec() == QDialog.Accepted:
            self.pb_class_1.clicked.connect(self.give_class)
            self.pb_class_2.clicked.connect(self.give_class)
            self.pb_class_3.clicked.connect(self.give_class)
            self.pb_class_4.clicked.connect(self.give_class)
            self.pb_class_5.clicked.connect(self.give_class)
            self.pb_class_6.clicked.connect(self.give_class)
            self.pb_class_7.clicked.connect(self.give_class)
            self.pb_class_8.clicked.connect(self.give_class)
            self.pb_class_9.clicked.connect(self.give_class)
            self.pb_class_10.clicked.connect(self.give_class)
            self.pb_erro.clicked.connect(self.give_class)
            self.pb_incerto.clicked.connect(self.give_class)

            for sa in [self.scrollArea,self.scrollArea_2]:
                sa.setStyleSheet("""
                    QScrollBar:horizontal {
                        background: #ffffff;
                        height: 15px;
                        margin: 0px 30px 0 30px;
                    }
                    QScrollBar::handle:horizontal {
                        background: orange;
                        min-width: 20px;
                    }
                    QScrollBar::add-line:horizontal {
                        background: #ffffff;
                        width: 30px;
                        subcontrol-position: right;
                        subcontrol-origin: margin;
                    }
                    QScrollBar::sub-line:horizontal {
                        background: #ffffff;
                        width: 30px;
                        subcontrol-position: left;
                        subcontrol-origin: margin;
                    }
                    QScrollBar:vertical {
                        background: #ffffff;
                        width: 15px;
                        margin: 30px 0px 30px 0px;
                    }
                    QScrollBar::handle:vertical {
                        background: orange;
                        min-height: 20px;
                    }
                    QScrollBar::add-line:vertical {
                        background: #ffffff;
                        height: 30px;
                        subcontrol-position: bottom;
                        subcontrol-origin: margin;
                    }
                    QScrollBar::sub-line:vertical {
                        background: #ffffff;
                        height: 30px;
                        subcontrol-position: top;
                        subcontrol-origin: margin;
                    }
                    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical,
                    QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                        background: none;
                    }
                    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
                    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                        background: none;
                    }
                """)
            
            self.scrollArea.setWidgetResizable(True)
            
            # Create a widget to contain the layout
            self.scroll_widget = QWidget()
            self.scrollArea.setWidget(self.scroll_widget)
            self.scroll_widget_2 = QWidget()
            self.scrollArea_2.setWidget(self.scroll_widget_2)
            # Set the scroll bar policies
            self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.scrollArea_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.scrollArea_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            
            self.pb_next.clicked.connect(self.next)
            self.h_layout_2 = QHBoxLayout(self.scroll_widget_2)
            self.v_layouts = [QVBoxLayout(),QVBoxLayout(),QVBoxLayout(),QVBoxLayout(),QVBoxLayout()]
            
            for layout in self.v_layouts: 
                self.h_layout_2.addLayout(layout)

            self.paths = os.listdir('golden')

            self.h_layout = QHBoxLayout(self.scroll_widget)
            for j in range(1,11):
                images_paths = [file for file in self.paths  if file.startswith(f"_{j}_")]
                images_paths = sorted(images_paths, key=lambda x: (x.split('_')[3],x.split('_')[4]))
                self.v_layout = QVBoxLayout()   
                label = QLabel(f'Classe {j}')
                self.v_layout.addWidget(label) 
                for i in range(len(images_paths)):
                    
                    label = ZoomableLabel()
                    image = QImage('golden/' + images_paths[i])
                    label.setPixmap(QPixmap.fromImage(image).scaled(700, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                    self.v_layout.addWidget(label)
                
                if len(images_paths) < 9:
                    spacer = QSpacerItem(20, 40,QSizePolicy.Fixed, QSizePolicy.Expanding)
                    self.v_layout.addItem(spacer)
                

                self.h_layout.addLayout(self.v_layout)
            
            
            self.values = self.data[self.data.new_tokens == self.data.loc[self.initial_index,'new_tokens']]['paths'].values
            self.class_chosen = True
            #self.next_value = 0
            self.next()
            self.class_chosen = False

    def show_warning(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()
        
    def update_timer(self):
        self.time_elapsed = self.time_elapsed.addSecs(1)
    def on_data_entered(self, name, dob, ethnicity, gender):
        print(f"Name: {name}, Date of Birth: {dob}, Ethnicity: {ethnicity}, Gender: {gender}")
        

        self.username = name
        self.dob = dob
        folder_name = f"/users/{self.username}_{self.dob}"
        folder_path = os.getcwd() + folder_name
        
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # Append to the log file
        self.log_file_path = os.path.join(folder_path, "log.txt")
        with open(self.log_file_path, 'a') as self.log_file:
            self.log_file.write(f"Log entry on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            self.log_file.write(f"Name: {name}, Date of Birth: {dob}, Ethnicity: {ethnicity}, Gender: {gender}\n")
        
        # Path to the CSV file
        self.filename = folder_path + f"/sessao_{self.username}.csv"
        
        # Read the content of the dataset's folder
        dataset_path = DATASET_PATH
        df = pd.read_csv(dataset_path,index_col=0,dtype = {'tokens': str,'new_tokens': str})
        # df = df[df['dataset'].isin(LIST_OF_DATASETS)]
        df = df[df['number_of_photos']>=MIN_NUM_PHOTOS]
        #folder_content = os.listdir(dataset_path)
        #folder_content = df['paths'].tolist()
        
        # # Remove the "desktop.ini" file if it exists (Windows)
        # if "desktop.ini" in folder_content:
        #     folder_content.remove("desktop.ini")
        
        # number_of_files = len(folder_content)
        
        # If the CSV file for the current user does not exist (new session)
        if not os.path.isfile(self.filename):
            # with open(self.filename, 'w') as new_csv:
            #     new_csv.write("ID,tokens,image,class\n")
            #     for i in range(number_of_files):
            #         new_csv.write(f"{i},{folder_content[i][:4]},{folder_content[i]},-10\n")

            ################
            ################
            # if face africa
            # df['class'] = -10
            # after='331_Casia Face Africa'
            # dic = {'331_Casia Face Africa':8}
            # with open('annotated data/log.txt', 'r') as file:
            #     lines = file.readlines()
            #     for idx,line in enumerate(lines):
            #         if idx == 5 : continue
            #         #if idx == 12 : continue
            #         if "[" in line:
            #             before = after
            #             dic[before] = class_chosen
            #             after = str(int(line[2:6])) + '_Casia Face Africa'
            #         if "Button Text:" in line:
            #             class_chosen = int(line[len("Button Text:"):])
            # df = df[df['dataset']=='Casia Face Africa']
            # df.loc[df['dataset']=='Casia Face Africa','class'] = df.loc[df['dataset']=='Casia Face Africa','new_tokens'].map(dic)
            # df['class'] = df['class'].fillna(-10).astype(int)
            #################
            #################
            df['class'] = -10
            df.to_csv(self.filename)
        
        # Load the existing CSV file (continue labeling from where it stopped)
        self.data = pd.read_csv(self.filename)
        
        # Identify the next unlabeled image to continue from where it stopped
        try:
            self.initial_index = self.data.index[self.data['class'] == -10][0]
        except Exception as e:
            if len(self.data[self.data['class'] == -10]) == 0:
                self.show_warning("Erro", f"O usuário {self.username} já anotou todas as imagens")
                sys.exit()
            else:
                self.show_warning("Erro", 'Um erro aconteceu\n' + str(e))
                sys.exit()
        
        self.new_tokens = self.data.new_tokens.unique()
        

        # Timer initialization
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer_running = False
        self.time_elapsed = QTime(0, 0)
        if os.path.exists(self.log_file_path):
            with open(self.log_file_path, 'r') as log_file:
                lines = log_file.readlines()
                for line in reversed(lines):
                    if line.startswith("Timer:"):
                        last_timer_value = line.split(": ")[1].strip()
                        self.time_elapsed = QTime.fromString(last_timer_value, "hh:mm:ss")
                        break
        
        self.timer.start(1000)
        with open(self.log_file_path, 'a') as self.log_file:
            self.log_file.write(f"Timer: {self.time_elapsed.toString('hh:mm:ss')}\n")
    
    def give_class(self):
        self.class_chosen = True
        self.pb_next.setText('Próxima Foto')
        # Retrieve the text of the button
        if hasattr(self,'class_btn'):
            self.class_btn.setEnabled(True)
            self.class_btn.setStyleSheet(self.class_btn_original_stylesheet)
        self.class_btn = self.sender()
        self.class_btn_original_stylesheet = self.class_btn.styleSheet()
        
        self.class_btn.setDisabled(True)
        self.class_btn.setStyleSheet("background-color: gray; color: white;")
        try:
            self.selected_class = int(self.class_btn.text())
        except:
            self.selected_class = self.class_btn.text()
            if self.selected_class == 'ERRO':
                self.selected_class = -1
            if self.selected_class == 'Incerto':
                self.selected_class = -2    
        
        
        print("Button Text:", self.selected_class)
        with open(self.log_file_path, 'a') as self.log_file:
            self.log_file.write(f"Button Text: {self.selected_class}\n")

    def next(self):
        

        if hasattr(self, 'selected_class'): 
                #print('oi')
                self.data.loc[self.data.paths.isin(self.values), 'class'] = self.selected_class
                self.data.to_csv(self.filename,index=False)


        print('old initial index',self.initial_index)
        with open(self.log_file_path, 'a') as self.log_file:
            self.log_file.write(f'old initial index {self.initial_index}\n')


        try:
            self.initial_index = self.data.index[self.data['class'] == -10][0]
            print('new initial index',self.initial_index)
        except Exception as e:
            if len(self.data[self.data['class'] == -10]) == 0:
                self.show_warning("Finalizado", f"O usuário {self.username} já anotou todas as imagens")
                sys.exit()
            else:
                self.show_warning("Erro", 'Um erro aconteceu\n' + str(e))
                sys.exit()    
        with open(self.log_file_path, 'a') as self.log_file:
            self.log_file.write(f'new initial index {self.initial_index}\n')


        if hasattr(self,'class_btn_original_stylesheet'):
            if hasattr(self,'class_btn'):
                self.class_btn.setEnabled(True)
                self.class_btn.setStyleSheet(self.class_btn_original_stylesheet)
        
        if self.class_chosen:
            # Remove all widgets from the main layout
            if hasattr(self,'v_layouts'):
                for layout in self.v_layouts:
                    while layout.count():
                        item = layout.takeAt(0)
                        widget = item.widget()
                        if widget:
                            widget.deleteLater()


            self.values = self.data[self.data.new_tokens == self.data.loc[self.initial_index,'new_tokens']]['paths'].values
            print_vals = self.data[self.data.new_tokens == self.data.loc[self.initial_index,'new_tokens']]['new_tokens'].values
            
            print(print_vals)
            with open(self.log_file_path, 'a') as self.log_file:
                self.log_file.write(f'{print_vals}\n')
            row = 0
            for i in range(len(self.values)):
                if i >= 20: break
                
                label = ZoomableLabel()
                image = QImage(self.values[i] )
                label.setPixmap(QPixmap.fromImage(image).scaled(850, 850, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                self.v_layouts[i - 5 * row].addWidget(label)    
                if (i+1) % 5 == 0:
                    row += 1

            for p in range(5):
                spacer = QSpacerItem(20, 40,QSizePolicy.Fixed, QSizePolicy.Expanding)
                self.v_layouts[p].addItem(spacer)
            
            remaining = len(self.data[self.data['class']== -10])
            
            error = len(self.data[self.data['class'] == -1])
            uncertain = len(self.data[self.data['class'] == -2])
            remaining_people = len(self.data[self.data['class']== -10]['new_tokens'].unique())
            already_done = len(self.data[self.data['class']>=0])
            self.statusBar().showMessage(f"Faltam {remaining} imagens de {remaining_people} pessoas à serem rotuladas. Contendo {error} erros e {uncertain} incertezas. Já rotulado {already_done}")

            
            self.class_chosen = False
            with open(self.log_file_path, 'a') as log_file:
                log_file.write(f"Timer: {self.time_elapsed.toString('hh:mm:ss')}\n")
        else:
            self.pb_next.setText('Selecione uma classe')
            with open(self.log_file_path, 'a') as log_file:
                log_file.write(f"Timer: {self.time_elapsed.toString('hh:mm:ss')}\n")