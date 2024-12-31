
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QFormLayout, QVBoxLayout, QSizePolicy, QComboBox
from ..common.hotkey_field import HotkeyField
from functools import partial
from util.data_keys import DATA_KEY
from src.data.translation.service import SERVICE
from data.translation.language import LANGUAGE

class OptionsWidget(QWidget):
    def __init__(self, data: dict, on_save_data: callable):
        super().__init__()
        self.data = data                                       
        
        main_container = QVBoxLayout(self)
        main_container.addStretch(1) # Spacer
        
        self.form_layout = QFormLayout()
        self.form_layout.setVerticalSpacing(20)
        main_container.addLayout(self.form_layout)
        
        for key in [DATA_KEY.SELECT_AREA, DATA_KEY.TOGGLE_OVERLAY]:
            self.add_hotkey_field(key)       
        
        self.add_languages_box()
        self.add_services_box()
        
        submit_button = QPushButton("Save")
        submit_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        submit_button.clicked.connect(lambda: on_save_data(self.data))
        main_container.addWidget(submit_button, alignment=Qt.AlignCenter)
                
        main_container.addStretch(1) # Spacer

    def add_hotkey_field(self, key: str):
        label = QLabel(text=key, parent=self)
        text_field = HotkeyField(
            on_value_changed=partial(self.on_data_value_changed, key),
            initial_value=self.data.get(key, ""),
            parent=self
        ) 
        self.form_layout.addRow(label, text_field)
        
    def add_languages_box(self):
        language_label = QLabel(text="Target language")
        languages_box = QComboBox(self)        
        for language in LANGUAGE:
            languages_box.addItem(language.language_name)
        languages_box.setInsertPolicy(QComboBox.NoInsert)
        
        languages_box.currentIndexChanged.connect(
            lambda index:self.on_data_value_changed(DATA_KEY.TARGET_LANGUAGE, index)
            )
        current_index_str = self.data[DATA_KEY.TARGET_LANGUAGE]
        languages_box.setCurrentIndex(int(current_index_str))       
        self.form_layout.addRow(language_label, languages_box)
        
    def add_services_box(self):      
        services_label = QLabel(text="Translation service")
        services_box = QComboBox(self)
        for service in SERVICE:
            services_box.addItem(service.service_name)
        services_box.setInsertPolicy(QComboBox.NoInsert)
        
        services_box.currentIndexChanged.connect(
            lambda index:self.on_data_value_changed(DATA_KEY.TRANSLATOR_SERVICE, index)
            )
        current_index_str = self.data[DATA_KEY.TRANSLATOR_SERVICE]
        services_box.setCurrentIndex(int(current_index_str))
        self.form_layout.addRow(services_label, services_box)
        
    def on_data_value_changed(self, key: str, value: str):
        print(f"key is {key} and value is {value}")
        self.data[key] = value

    def mousePressEvent(self, event):
        if self.focusWidget() is not None:
            self.focusWidget().clearFocus()
        super().mousePressEvent(event)