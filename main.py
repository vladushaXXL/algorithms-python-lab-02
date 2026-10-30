import sys
from PySide6.QtCore import Qt  # <-- Добавлен импорт Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QComboBox, QPushButton, 
                               QTextEdit, QMessageBox, QLineEdit, QFormLayout, QGroupBox)
from particles.models import Particle, REFERENCE_PARTICLES
from particles.calculations import calculate_specific_charge, calculate_compton_wavelength
from particles.exporter import save_results_to_excel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор элементарных частиц")
        self.resize(600, 500)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # --- Блок ввода параметров ---
        input_group = QGroupBox("Ввод параметров частицы")
        form_layout = QFormLayout()

        # Выбор частицы
        self.combo_box = QComboBox()
        self.combo_box.addItem("-- Пользовательская частица --")
        self.combo_box.addItems(REFERENCE_PARTICLES.keys())
        self.combo_box.currentTextChanged.connect(self.fill_reference_data)
        form_layout.addRow("Выбрать из справочника:", self.combo_box)

        # Поля ввода массы и заряда
        self.mass_input = QLineEdit()
        self.mass_input.setPlaceholderText("Например: 9.109e-31 (кг)")
        
        self.charge_input = QLineEdit()
        self.charge_input.setPlaceholderText("Например: -1.602e-19 (Кл)")

        form_layout.addRow("Масса (кг):", self.mass_input)
        form_layout.addRow("Заряд (Кл):", self.charge_input)
        
        input_group.setLayout(form_layout)
        main_layout.addWidget(input_group)

        # --- Блок вывода результатов ---
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("Здесь появятся результаты расчетов...")
        main_layout.addWidget(self.result_text)

        # --- Кнопки ---
        btn_layout = QHBoxLayout()
        
        self.btn_help = QPushButton("Справка")
        self.btn_help.clicked.connect(self.show_help)
        
        self.btn_calc = QPushButton("Рассчитать")
        self.btn_calc.clicked.connect(self.calculate)
        
        self.btn_save = QPushButton("Сохранить в Excel")
        self.btn_save.clicked.connect(self.save_to_excel)
        self.btn_save.setEnabled(False) # Доступна только после расчета

        btn_layout.addWidget(self.btn_help)
        btn_layout.addStretch() # Раздвигает кнопки для красоты
        btn_layout.addWidget(self.btn_calc)
        btn_layout.addWidget(self.btn_save)
        
        main_layout.addLayout(btn_layout)

    def fill_reference_data(self, text):
        """Автозаполнение полей при выборе стандартной частицы."""
        if text in REFERENCE_PARTICLES:
            data = REFERENCE_PARTICLES[text]
            self.mass_input.setText(str(data["mass"]))
            self.charge_input.setText(str(data["charge"]))
        elif text == "-- Пользовательская частица --":
            self.mass_input.clear()
            self.charge_input.clear()

    def calculate(self):
        # Получаем данные из полей ввода
        name = self.combo_box.currentText()
        if name == "-- Пользовательская частица --":
            name = "Пользовательская частица"
        
        mass_str = self.mass_input.text().strip().replace(',', '.')
        charge_str = self.charge_input.text().strip().replace(',', '.')

        # 1. Проверка на пустые поля
        if not mass_str or not charge_str:
            QMessageBox.warning(self, "Ошибка ввода", 
                                "Пожалуйста, заполните поля 'Масса' и 'Заряд'.\n"
                                "Вы можете выбрать частицу из справочника или ввести свои значения.")
            return

        # 2. Проверка на то, что введены именно числа
        try:
            mass = float(mass_str)
            charge = float(charge_str)
        except ValueError:
            QMessageBox.warning(self, "Ошибка ввода", 
                                "Некорректные данные!\n\n"
                                "Масса и заряд должны быть числами.\n"
                                "Используйте точку для разделения дробной части.\n"
                                "Пример: 9.109e-31 или -1.6")
            return

        # 3. Проверка физического смысла
        if mass <= 0:
            QMessageBox.warning(self, "Ошибка ввода", 
                                "Масса частицы должна быть строго больше нуля!")
            return

        # Создаем объект (ООП)
        particle = Particle(name, mass, charge)
        
        # Вызовы из модуля calculations
        spec_charge = calculate_specific_charge(particle)
        compton_wl = calculate_compton_wavelength(particle)

        # Сохранение результатов для экспорта
        self.current_results = (particle.name, spec_charge, compton_wl)

        # Вывод на экран
        text = (f"--- Результаты для: {particle.name} ---\n\n"
                f"Масса: {particle.mass:.4e} кг\n"
                f"Заряд: {particle.charge:.4e} Кл\n\n"
                f"Удельный заряд (q/m):\n{spec_charge:.4e} Кл/кг\n\n"
                f"Комптоновская длина волны (λ):\n{compton_wl:.4e} м")
        self.result_text.setText(text)
        self.btn_save.setEnabled(True)

    def save_to_excel(self):
        if hasattr(self, 'current_results'):
            try:
                name, spec_charge, compton_wl = self.current_results
                filename = save_results_to_excel(name, spec_charge, compton_wl)
                QMessageBox.information(self, "Успех", f"Результаты успешно сохранены в файл {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{e}")

    def show_help(self):
        """Отображение окна со справкой."""
        help_text = (
            "<h3>О программе</h3>"
            "<p>Данное приложение предназначено для расчёта параметров элементарных частиц.</p>"
            
            "<h3>Как пользоваться</h3>"
            "<ol>"
            "<li>Выберите частицу из выпадающего списка (Электрон, Протон, Нейтрон) или оставьте «Пользовательская частица».</li>"
            "<li>В поля «Масса» и «Заряд» введите значения в системе СИ (килограммы и Кулоны). "
            "Можно использовать экспоненциальную запись, например: <i>9.109e-31</i>.</li>"
            "<li>Нажмите кнопку <b>«Рассчитать»</b>, чтобы получить результаты.</li>"
            "<li>Нажмите <b>«Сохранить в Excel»</b>, чтобы выгрузить отчет в файл <i>report.xlsx</i>.</li>"
            "</ol>"
            
            "<h3>Используемые формулы</h3>"
            "<ul>"
            "<li><b>Удельный заряд:</b> q / m (Кл/кг)</li>"
            "<li><b>Комптоновская длина волны:</b> &lambda; = h / (m &middot; c) (м)</li>"
            "</ul>"
            
            "<h3>Физические константы</h3>"
            "<ul>"
            "<li>Постоянная Планка (h) = 6.62607015 &middot; 10<sup>-34</sup> Дж&middot;с</li>"
            "<li>Скорость света (c) = 299 792 458 м/с</li>"
            "</ul>"
        )
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Справка")
        
        # Исправленная строка:
        msg_box.setTextFormat(Qt.TextFormat.RichText) 
        
        msg_box.setText(help_text)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())