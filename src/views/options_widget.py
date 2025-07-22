from PyQt5.QtWidgets import QWidget, QLabel, QFormLayout, QVBoxLayout, QComboBox

from .hotkey_field import HotkeyField

class OptionsWidget(QWidget):
    def __init__(self, model, controller):
        super().__init__()
        self.model = model                                      
        self.controller = controller
        
        main_container = QVBoxLayout(self)
        main_container.addStretch(1) # Spacer
        
        self.form_layout = QFormLayout()
        self.form_layout.setVerticalSpacing(20)
        main_container.addLayout(self.form_layout)
        
        select_area_label = QLabel(text="Select area")
        self.select_area_field = self.create_hotkey_field(controller.set_area_selection_hotkey, model.area_selection_hotkey)
        self.form_layout.addRow(select_area_label, self.select_area_field) 
        
        show_app_label = QLabel(text="Show app")
        self.show_app_field = self.create_hotkey_field(controller.set_show_app_hotkey, model.show_app_hotkey)
        self.form_layout.addRow(show_app_label, self.show_app_field)
        
        target_language_label = QLabel("Target language")
        languageNames = self.controller.get_languages_names()
        self.target_language_box = self.create_combo_box(controller.set_target_language, 
                                                        self.model.target_language, languageNames)
        self.form_layout.addRow(target_language_label, self.target_language_box) 
        
        translation_service_label = QLabel("Translation service")
        serviceNames = self.controller.get_translation_services_names()
        self.service_box = self.create_combo_box(controller.set_translation_service,
                                                self.model.translation_service, serviceNames)
        self.form_layout.addRow(translation_service_label, self.service_box)  
        
        main_container.addStretch(1) # Spacer
    
    def create_hotkey_field(self, on_change, initial_value):        
        return HotkeyField(
            on_value_changed = on_change,
            on_set_focus = self.controller.set_editing_hotkey,
            initial_value = initial_value,
            parent = self
        )
        
    def create_combo_box(self, on_change, current_index, list: list):     
        combo_box = QComboBox(self)
        combo_box.setInsertPolicy(QComboBox.NoInsert)        
        combo_box.currentIndexChanged.connect(on_change)
        for item in list:
            combo_box.addItem(item)
        combo_box.setCurrentIndex(current_index)
        return combo_box

    def mousePressEvent(self, event):
        if self.focusWidget() is not None:
            self.controller.set_editing_hotkey(False)
            self.focusWidget().clearFocus()
        super().mousePressEvent(event)