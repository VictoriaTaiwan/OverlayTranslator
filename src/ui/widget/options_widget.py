
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QFormLayout, QVBoxLayout, QSizePolicy, QComboBox
from ..common.hotkey_field import HotkeyField
from util.data_keys import DATA_KEY
from src.data.translation.service import SERVICE
from data.translation.language import LANGUAGE

class OptionsWidget(QWidget):
    def __init__(self, data: dict, on_save_data: callable):
        super().__init__()
        
        self.on_save_data = on_save_data
        self.last_data = dict(data)
        self.current_data = dict(data)
        
        self.text_fields = {}
        self.combo_boxes = {}                                       
        
        main_container = QVBoxLayout(self)
        main_container.addStretch(1) # Spacer
        
        self.form_layout = QFormLayout()
        self.form_layout.setVerticalSpacing(20)
        main_container.addLayout(self.form_layout)
        
        self.add_hotkey_field_row(DATA_KEY.SELECT_AREA)
        self.add_hotkey_field_row(DATA_KEY.TOGGLE_OVERLAY)       
        
        languageNames = list(map(lambda lang:lang.language_name, list(LANGUAGE)))
        self.add_combo_box_row(DATA_KEY.TARGET_LANGUAGE, languageNames)
        
        serviceNames = list(map(lambda service:service.service_name, list(SERVICE)))
        self.add_combo_box_row(DATA_KEY.TRANSLATOR_SERVICE, serviceNames)
        
        submit_button = QPushButton("Save")
        submit_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        submit_button.clicked.connect(lambda: self.on_save_options())
        main_container.addWidget(submit_button, alignment=Qt.AlignCenter)
                
        main_container.addStretch(1) # Spacer
    
    def is_data_saved(self) -> bool:
        return list(self.last_data.values()) == list(self.current_data.values())
    
    def on_save_options(self):
        self.on_save_data(self.current_data)
        self.last_data = dict(self.current_data)    
    
    def resetData(self):
        for config_key_name, text_field in self.text_fields.items():
            text_field.setText(self.last_data[config_key_name])
        
        for config_key_name, combo_box in self.combo_boxes.items():
            data_index_str = self.last_data[config_key_name]
            combo_box.setCurrentIndex(int(data_index_str))  
    
    def add_hotkey_field_row(self, config_key: DATA_KEY):
        label = QLabel(text=config_key.visible_name, parent=self)
        
        text_field = HotkeyField(
            on_value_changed=lambda value: self.on_data_value_changed(config_key.value, value),
            initial_value=self.current_data.get(config_key.value, ""),
            parent=self
        ) 
        
        self.form_layout.addRow(label, text_field)
        
        self.text_fields[config_key.value] = text_field        
        
    def add_combo_box_row(self, config_key: DATA_KEY, list: list):
        label = QLabel(text=config_key.visible_name)
        
        combo_box = QComboBox(self)
        combo_box.setInsertPolicy(QComboBox.NoInsert)        
        
        for item in list:
            combo_box.addItem(item)       
        
        combo_box.currentIndexChanged.connect(
            lambda index:self.on_data_value_changed(config_key.value, str(index))
            )
        
        current_index_str = self.current_data[config_key.value]
        combo_box.setCurrentIndex(int(current_index_str))       
        
        self.form_layout.addRow(label, combo_box)
        
        self.combo_boxes[config_key.value] = combo_box
        
    def on_data_value_changed(self, key: str, value: str):
        print(f"key is {key} and value is {value}")
        self.current_data[key] = value

    def mousePressEvent(self, event):
        if self.focusWidget() is not None:
            self.focusWidget().clearFocus()
        super().mousePressEvent(event)