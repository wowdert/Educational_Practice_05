import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict
from elements import atomic_masses

class MolecularMassCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Калькулятор молекулярных масс")
        self.root.geometry("450x400")
        self.elements = atomic_masses
        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text="Введите химическую формулу (например, H2O или Ca(OH)2):").pack(anchor='w',
                                                                                                   pady=(0, 5))

        self.formula_var = tk.StringVar()
        self.formula_entry = ttk.Entry(main_frame, textvariable=self.formula_var, font=("Arial", 12))
        self.formula_entry.pack(fill='x', pady=(0, 10))
        self.formula_entry.bind('<Return>', lambda event: self.calculate_mass())

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(0, 10))

        ttk.Button(button_frame, text="Рассчитать", command=self.calculate_mass).pack(side='left', padx=(0, 5),
                                                                                      expand=True, fill='x')
        ttk.Button(button_frame, text="Очистить", command=self.clear_fields).pack(side='left', expand=True, fill='x')

        result_frame = ttk.LabelFrame(main_frame, text="Результаты")
        result_frame.pack(fill='both', expand=True)

        self.result_text = tk.Text(result_frame, font=("Courier New", 10), state='disabled', wrap='word')
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)

        self.result_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y', pady=5)

    def parse_formula(self, formula):
        formula = formula.strip()
        if not formula:
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

    def calculate_mass(self):
        formula = self.formula_var.get().strip()

        if not formula:
            messagebox.showwarning("Внимание", "Поле ввода пустое")
            return

        try:
            elements = self.parse_formula(formula)

            if not elements:
                messagebox.showwarning("Внимание", "Не удалось распознать формулу")
                return

            total_mass = 0.0
            result_lines = [f"Формула: {formula}", "═" * 40]

            for element, count in sorted(elements.items()):
                atomic_mass = self.elements[element]
                element_mass = atomic_mass * count
                total_mass += element_mass
                result_lines.append(f"{element:<3}: {count:>3} × {atomic_mass:>7.3f} = {element_mass:>8.3f}")

            result_lines.append("═" * 40)
            result_lines.append(f"Масса: {total_mass:.3f} г/моль")

            self.result_text.config(state='normal')
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "\n".join(result_lines))
            self.result_text.config(state='disabled')

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

    def clear_fields(self):
        self.formula_var.set("")
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state='disabled')

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MolecularMassCalculator()
    app.run()
