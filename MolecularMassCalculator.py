import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict
from elements import atomic_masses

class MolecularMassCalculator:
    def __init__(self):
        self.root = tk.Tk() #главное окно и его настройки
        self.root.title("Калькулятор молекулярной массы")

        self.root.geometry("550x750") #фиксированный размер окна
        self.root.resizable(False, False)

        self.root.configure(bg='#E6F2FF')
        self.elements = atomic_masses
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style() #настройка стиля
        style.theme_use('clam')

        style.configure('Title.TLabel', #для заголовка
                        background='#E6F2FF',
                        foreground='#2C3E50',
                        font=("Comic Sans MS", 16, "bold"))

        style.configure('Instruction.TLabel', #для инструкции
                        background='#E6F2FF',
                        foreground='#34495E')

        style.configure('Calculate.TButton', #для кнопки расчета
                        background='#3498DB',
                        foreground='white',
                        font=('Arial', 10, 'bold'),
                        padding=5)
        style.map('Calculate.TButton',
                  background=[('active', '#2980B9')])

        style.configure('Clear.TButton', #для кнопки очистки
                        background='#E74C3C',
                        foreground='white',
                        font=('Arial', 10, 'bold'),
                        padding=5)
        style.map('Clear.TButton',
                  background=[('active', '#C0392B')])

        title_frame = tk.Frame(self.root, bg='#2C3E50', height=60) #синяя полоска для заголовка
        title_frame.pack(fill='x', pady=(0, 10))
        title_frame.pack_propagate(False)

        title_label = ttk.Label(title_frame,
                                text="🧪 Калькулятор молекулярной массы",
                                style='Title.TLabel',
                                background='#2C3E50',
                                foreground='white')
        title_label.pack(expand=True)

        main_container = tk.Frame(self.root, bg='#E6F2FF')
        main_container.pack(fill='both', expand=True, padx=20, pady=10)

        instruction_label = ttk.Label(main_container, #подсказка в поле ввода
                                      text="Введите химическую формулу (вводить в точности как в таблице Менделеева!)",
                                      style='Instruction.TLabel',
                                      font=('Arial', 9))
        instruction_label.pack(pady=(0, 10))

        input_frame = tk.Frame(main_container, bg='#FFFFFF', bd=2, relief=tk.GROOVE)
        input_frame.pack(pady=10, fill='x', padx=5)

        self.formula_var = tk.StringVar()
        self.formula_entry = ttk.Entry(input_frame,
                                       textvariable=self.formula_var,
                                       font=("Arial", 12),
                                       width=100)
        self.formula_entry.pack(padx=10, pady=10)
        self.formula_entry.pack(padx=10, pady=10)
        self.formula_entry.bind('<Return>', lambda event: self.calculate_mass()) #чтобы работала кнопка Enter

        self.formula_entry.insert(0, "Например: H2O, CO2, C6H12O6")
        self.formula_entry.config(foreground='grey')

        def on_entry_click(event):
            if self.formula_entry.get() == "Например: H2O, CO2, C6H12O6":
                self.formula_entry.delete(0, tk.END)
                self.formula_entry.config(foreground='black')

        def on_focusout(event):
            if self.formula_entry.get() == '':
                self.formula_entry.insert(0, "Например: H2O, CO2, C6H12O6")
                self.formula_entry.config(foreground='grey')

        self.formula_entry.bind('<FocusIn>', on_entry_click)
        self.formula_entry.bind('<FocusOut>', on_focusout)

        button_frame = tk.Frame(main_container, bg='#E6F2FF')
        button_frame.pack(pady=10)

        calculate_btn = ttk.Button(button_frame, #запуск расчета
                                   text="Рассчитать массу",
                                   command=self.calculate_mass,
                                   style='Calculate.TButton',
                                   width=20)
        calculate_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = ttk.Button(button_frame, #очистка полей
                               text="Очистить",
                               command=self.clear_fields,
                               style='Clear.TButton',
                               width=20)
        clear_btn.pack(side=tk.LEFT, padx=5)

        result_frame = tk.LabelFrame(main_container,
                                     text="Результаты расчета",
                                     font=("Arial", 10, "bold"),
                                     bg='#E6F2FF',
                                     fg='#2C3E50',
                                     bd=2,
                                     relief=tk.GROOVE)
        result_frame.pack(pady=10, padx=5, fill='both', expand=True)

        self.result_text = tk.Text(result_frame,
                                   height=12,
                                   width=60,
                                   font=("Courier New", 9),
                                   bg='#F8F9FA',
                                   fg='#2C3E50',
                                   relief=tk.FLAT,
                                   bd=2,
                                   padx=5,
                                   pady=5,
                                   wrap=tk.WORD,
                                   state='disabled')

        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)

        self.result_text.pack(side=tk.LEFT, fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill='y', pady=5)

        examples_frame = ttk.LabelFrame(main_container, #список примеров формул
                                        text="Примеры формул")
        examples_frame.pack(pady=10, padx=5, fill='x')

        examples = ["H2O - вода", "CO2 - углекислый газ", "C6H12O6 - глюкоза",
                    "Ca(OH)2 - гашеная известь", "CH3COOH - уксусная кислота",
                    "H2SO4 - серная кислота", "NaCl - поваренная соль"]

        for example in examples: #чтобы примеры были кликабельными
            example_label = tk.Label(examples_frame,
                                     text=example,
                                     bg='#FFFFFF',
                                     fg='#2C3E50',
                                     font=('Arial', 9),
                                     anchor='w',
                                     padx=10,
                                     pady=2)
            example_label.pack(fill='x', padx=5, pady=1)

            example_label.bind('<Enter>', lambda e, lbl=example_label:
            lbl.config(bg='#ECF0F1'))
            example_label.bind('<Leave>', lambda e, lbl=example_label:
            lbl.config(bg='#FFFFFF'))

            example_label.bind('<Button-1>', lambda e, ex=example:
            self.insert_example(ex.split(' - ')[0]))

        status_frame = tk.Frame(self.root, bg='#2C3E50', height=25)
        status_frame.pack(side=tk.BOTTOM, fill='x')
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(status_frame,
                                     text="Готов к работе",
                                     bg='#2C3E50',
                                     fg='white',
                                     font=('Arial', 8))
        self.status_label.pack(side=tk.LEFT, padx=10)

        version_label = tk.Label(status_frame,
                                 text="v1.0",
                                 bg='#2C3E50',
                                 fg='#BDC3C7',
                                 font=('Arial', 8))
        version_label.pack(side=tk.RIGHT, padx=10)

    def insert_example(self, formula): #вставка формулы из примеров
        self.formula_var.set(formula)
        entry_widget = self.root.focus_get()
        if isinstance(entry_widget, ttk.Entry):
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, formula)
            entry_widget.config(foreground='black')
        self.update_status(f"Вставлена формула: {formula}")

    def update_status(self, message):
        self.status_label.config(text=message)

    def parse_formula(self, formula): #обработка формклы
        formula = formula.strip()
        if not formula or formula == "Например: H2O, CO2, C6H12O6":
            return None

        elements_count = defaultdict(int)
        i = 0
        n = len(formula)

        while i < n:
            if formula[i].isupper():
                element = formula[i]
                i += 1
                if i < n and formula[i].islower():
                    element += formula[i]
                    i += 1
                count_str = ""
                while i < n and formula[i].isdigit():
                    count_str += formula[i]
                    i += 1

                count = int(count_str) if count_str else 1
                if element in self.elements:
                    elements_count[element] += count
                else:
                    raise ValueError(f"Неизвестный элемент: {element}")

            elif formula[i] == '(':
                j = i + 1
                bracket_count = 1
                while j < n and bracket_count > 0:
                    if formula[j] == '(':
                        bracket_count += 1
                    elif formula[j] == ')':
                        bracket_count -= 1
                    j += 1

                if bracket_count != 0:
                    raise ValueError("Незакрытая скобка")
                inner_formula = formula[i + 1:j - 1]
                group_elements = self.parse_formula(inner_formula)
                i = j
                count_str = ""
                while i < n and formula[i].isdigit():
                    count_str += formula[i]
                    i += 1

                count = int(count_str) if count_str else 1
                if group_elements:
                    for element, element_count in group_elements.items():
                        elements_count[element] += element_count * count
            else:
                if formula[i].isspace():
                    i += 1
                else:
                    raise ValueError(f"Неожиданный символ: {formula[i]}")

        return dict(elements_count)

    def calculate_mass(self): #расчет итоглвой массы и вывод результата
        formula = self.formula_var.get()

        if not formula or formula == "Например: H2O, CO2, C6H12O6":
            messagebox.showwarning("Внимание", "Введите химическую формулу")
            return

        self.update_status("Выполняется расчет...")

        try:
            elements = self.parse_formula(formula)

            if not elements:
                messagebox.showwarning("Внимание", "Не удалось распознать формулу")
                self.update_status("Ошибка: не удалось распознать формулу")
                return

            total_mass = 0.0
            result_lines = []

            for element, count in sorted(elements.items()):
                atomic_mass = self.elements[element]
                element_mass = atomic_mass * count
                total_mass += element_mass
                result_lines.append(f"{element:<3}: {count:>3} × {atomic_mass:>7.3f} = {element_mass:>8.3f} г/моль")

            self.result_text.config(state='normal')
            self.result_text.delete(1.0, tk.END)

            self.result_text.insert(tk.END, f"Формула: {formula}\n", 'title')

            self.result_text.insert(tk.END, "═" * 50 + "\n", 'separator')

            for line in result_lines:
                self.result_text.insert(tk.END, line + "\n", 'element')

            self.result_text.insert(tk.END, "═" * 50 + "\n", 'separator')
            self.result_text.insert(tk.END, f"Молекулярная масса: {total_mass:.3f} г/моль\n", 'result')
            self.result_text.insert(tk.END, f"Округленно:         {round(total_mass, 2)} г/моль\n", 'result')

            self.result_text.tag_configure('title', foreground='#2C3E50', font=('Courier New', 10, 'bold'))
            self.result_text.tag_configure('separator', foreground='#7F8C8D')
            self.result_text.tag_configure('element', foreground='#34495E')
            self.result_text.tag_configure('result', foreground='#27AE60', font=('Courier New', 10, 'bold'))

            self.result_text.config(state='disabled')

            self.update_status(f"Расчет завершен: {total_mass:.2f} г/моль")

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
            self.update_status(f"Ошибка: {str(e)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
            self.update_status(f"Ошибка: {str(e)}")

    def clear_fields(self):
        self.formula_var.set("")

        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state='disabled')

        self.formula_entry.delete(0, tk.END)
        self.formula_entry.insert(0, "Например: H2O, CO2, C6H12O6")
        self.formula_entry.config(foreground='grey')

        self.update_status("Поля очищены")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MolecularMassCalculator()
    app.run()
