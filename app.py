import tkinter
import customtkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

import messages as msg
import evaluation

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # устанавливаем тему приложения
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")

        # формируем окно
        self.title(msg.APP_TITLE)
        self.geometry(f"{1100}x{580}")
        self.state("zoomed")

        # формируем макет (2x2)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # формируем сайдбар
        self.sidebar_frame = customtkinter.CTkFrame(self, width=210, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(1, weight=1)

        # формируем кнопку выбора файла
        self.sidebar_choose_file_button = customtkinter.CTkButton(self.sidebar_frame, command=self.on_choose_file_button_press)
        self.sidebar_choose_file_button.grid(row=0, column=0, padx=20, pady=10)
        self.sidebar_choose_file_button.configure(text=msg.CHOOSE_FILE_BUTTON_LABEL)

        # формируем сообщение для пустого диалога
        self.empty_dialog_text = customtkinter.CTkLabel(self, text=msg.EMPTY_DIALOG_LABEL)
        self.empty_dialog_text.grid(row=0, column=1, rowspan=2)

        # формируем макет вывода статистических данных
        self.statistic_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.statistic_frame.grid_columnconfigure(0, weight=1)
        self.statistic_frame.grid_rowconfigure(0, weight=0)
        self.statistic_frame.grid_rowconfigure(1, weight=1)

        # формируем макет вывода текстовой информации
        self.statistic_data_frame = customtkinter.CTkFrame(self.statistic_frame, corner_radius=0)
        self.statistic_data_frame.grid_columnconfigure((0, 1), weight=1)
        self.statistic_data_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.statistic_data_frame.grid(row=0, column=0, sticky="nsew")

        # формирует текстовые узлы для вывода информации
        self.statistic_data_title = customtkinter.CTkLabel(self.statistic_data_frame, font=("Arial", 24, "bold"), text=msg.RESULT_EVALUATION_LABEL)
        self.statistic_data_title.grid(row=0, column=0, padx=20, pady=12, columnspan=2, sticky="w")
        self.statistic_data_text_length = customtkinter.CTkLabel(self.statistic_data_frame)
        self.statistic_data_text_length.grid(row=1, column=0, padx=20, pady=2, sticky="w")
        self.statistic_data_alphabet_length = customtkinter.CTkLabel(self.statistic_data_frame)
        self.statistic_data_alphabet_length.grid(row=1, column=1, padx=20, pady=2, sticky="w")
        self.statistic_data_h_max = customtkinter.CTkLabel(self.statistic_data_frame)
        self.statistic_data_h_max.grid(row=2, column=0, padx=20, pady=2, sticky="w")
        self.statistic_data_h_real = customtkinter.CTkLabel(self.statistic_data_frame)
        self.statistic_data_h_real.grid(row=2, column=1, padx=20, pady=2, sticky="w")
        self.statistic_data_r_abs = customtkinter.CTkLabel(self.statistic_data_frame)
        self.statistic_data_r_abs.grid(row=3, column=0, padx=20, pady=2, sticky="w")
        self.statistic_data_r_rel = customtkinter.CTkLabel(self.statistic_data_frame)
        self.statistic_data_r_rel.grid(row=3, column=1, padx=20, pady=2, sticky="w")
        self.statistic_data_s_max = customtkinter.CTkLabel(self.statistic_data_frame)
        self.statistic_data_s_max.grid(row=4, column=0, padx=20, pady=2, sticky="w")
        self.statistic_data_s_min = customtkinter.CTkLabel(self.statistic_data_frame)
        self.statistic_data_s_min.grid(row=4, column=1, padx=20, pady=2, sticky="w")

        # формируем канвас для отрисовки графика
        self.plot_figure = Figure(figsize = (1, 1), dpi = 100)
        self.plot_ax = self.plot_figure.add_subplot(111)
        self.plot_canvas = FigureCanvasTkAgg(self.plot_figure, self.statistic_frame)
        self.plot_canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")        

    # метод отбработки нажания на кнопку выбора файла
    def on_choose_file_button_press (self):
        # получаем путь к файлу путем выбора из файловой системы
        filename = tkinter.filedialog.askopenfilename()

        # если путь был выбран
        if filename:
            # получаем оценку статистических характеристик выбранного файла 
            data = evaluation.get_statistical_characteristics(filename)

            # отображаем результат на экране
            self.render_result(data)
    
    # отрисовка результатов оценки данных на экране
    def render_result (self, data):
        # преобразуем список вероятностей для вывода в процентах
        probabilities = list(map(lambda probability: probability * 100, data["probabilities"]))

        # отрисовываем на канвасе график
        self.plot_ax.clear()
        self.plot_ax.bar(data["symbols"], probabilities)
        self.plot_ax.set_title(msg.PROBABILITY_GRAPH_TITLE)
        self.plot_ax.set_ylabel(msg.PROBABILITY_LABEL)
        self.plot_canvas.draw()

        # удаляем из разметки сообщение пустого диалога
        self.empty_dialog_text.grid_remove()

        # устанавливаем значения текстовых узлов
        self.statistic_data_text_length.configure(text = msg.MESSAGE_LENGTH_LABEL + str(data["text_length"]))
        self.statistic_data_alphabet_length.configure(text = msg.ALPHABET_LENGTH_LABEL + str(data["alphabet_length"]))
        self.statistic_data_h_max.configure(text = msg.MAX_ENTROPY_LABEL + str(data["h_max"]))
        self.statistic_data_h_real.configure(text = msg.REAL_ENTROPY_LABEL + str(data["h_real"]))
        self.statistic_data_r_abs.configure(text = msg.ABSOLUTE_REDUNDANCY + str(data["r_abs"]))
        self.statistic_data_r_rel.configure(text = msg.RELATIVE_REDUNDANCY + str(data["r_rel"]))
        self.statistic_data_s_max.configure(text = f'{msg.SYMBOL_MOST_SELF_INFO_LABEL}"{str(data["s_max"][0])}" = {str(data["s_max"][1])}')
        self.statistic_data_s_min.configure(text = f'{msg.SYMBOL_LEAST_SELF_INFO_LABEL}"{str(data["s_min"][0])}" = {str(data["s_min"][1])}')

        # монтируем макет вывода статистических данных
        self.statistic_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")
