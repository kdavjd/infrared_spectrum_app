from PyQt6.QtWidgets import QVBoxLayout, QWidget
from .load_button import LoadButton
from .spectrum_table import SpectrumTable

class ButtonPanel(QWidget):
    def __init__(self, spectrum_data_frame, config, gaussian_params):
        super().__init__()

        # Создаем макет для кнопок
        button_layout = QVBoxLayout()

        # Создаем кнопки
        self.load_button = LoadButton(spectrum_data_frame)        

        # Добавляем кнопки в макет
        button_layout.addWidget(self.load_button)        

        # Создаем макет для таблицы
        table_layout = QVBoxLayout()
        self.spectrum_table = SpectrumTable(config, gaussian_params)
        table_layout.addWidget(self.spectrum_table)

        # Создаем основной макет
        main_layout = QVBoxLayout()

        # Добавляем макет кнопок и растягиваемое пространство
        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)  # Добавляет растягиваемое пространство, чтобы кнопки оставались сверху

        # Добавляем макет таблицы
        main_layout.addLayout(table_layout)

        # Устанавливаем основной макет для виджета
        self.setLayout(main_layout)

        