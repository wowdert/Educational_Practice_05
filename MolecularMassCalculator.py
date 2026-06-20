import tkinter as tk
from tkinter import ttk
from collections import defaultdict
from elements import atomic_masses

class MolecularMassCalculatorMVP:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Калькулятор массы (Краткий)")
        self.root.geometry("400x250")
        self.elements = atomic_masses
        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text="Введите химическую формулу:").pack(anchor='w', pady=(0, 5))

        self.formula_var = tk.StringVar()
        self.formula_entry = ttk.Entry(main_frame, textvariable=self.formula_var, font=("Arial", 12))
        self.formula_entry.pack(fill='x', pady=(0, 15))
        self.formula_entry.bind('<Return>', lambda event: self.calculate_mass())

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(0, 15))

        ttk.Button(button_frame, text="Рассчитать", command=self.calculate_mass).pack(side='left', padx=(0, 5),
                                                                                      expand=True, fill='x')
        ttk.Button(button_frame, text="Очистить", command=self.clear_fields).pack(side='left', expand=True, fill='x')

        result_frame = ttk.LabelFrame(main_frame, text="Результат")
        result_frame.pack(fill='both', expand=True)

        self.result_text = tk.Text(result_frame, font=("Arial", 11, "bold"), height=2, state='disabled', wrap='word')
        self.result_text.pack(fill='both', expand=True, padx=5, pady=5)

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
                elements_count[element] += count

            elif formula[i] == '(':
                j = i + 1
                bracket_count = 1
                while j < n and bracket_count > 0:
                    if formula[j] == '(':
                        bracket_count += 1
                    elif formula[j] == ')':
                        bracket_count -= 1
                    j += 1

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
                i += 1

        return dict(elements_count)

    def calculate_mass(self):
        formula = self.formula_var.get().strip()
        if not formula:
            return

        elements = self.parse_formula(formula)
        if not elements:
            return

        total_mass = 0.0
        for element, count in elements.items():
            atomic_mass = self.elements.get(element, 0.0) 
            total_mass += atomic_mass * count

        result_string = f"Молекулярная масса {formula} = {total_mass:.3f} г/моль"

        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_string)
        self.result_text.config(state='disabled')

    def clear_fields(self):
        self.formula_var.set("")
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state='disabled')

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MolecularMassCalculatorMVP()
    app.run()
