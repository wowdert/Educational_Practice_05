import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict
from elements import atomic_masses

class MolecularMassCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Калькулятор молекулярной массы")
        self.root.geometry("500x600")
        self.setup_ui()
        self.elements = atomic_masses

    def setup_ui(self):
        title_label = ttk.Label(self.root, text="Калькулятор молекулярной массы",
                                font=("Comic Sans MS", 16, "bold"))
        title_label.pack(pady=10)
        instruction_label = ttk.Label(self.root,
                                      text="Введите химическую формулу")
        instruction_label.pack(pady=5)

        self.formula_var = tk.StringVar() #поле ввода
        formula_entry = ttk.Entry(self.root, textvariable=self.formula_var,
                                  font=("Comic Sans MS", 12), width=40)
        formula_entry.pack(pady=10)
        formula_entry.bind('<Return>', lambda event: self.calculate_mass())

        calculate_btn = ttk.Button(self.root, text="Рассчитать массу",
                                   command=self.calculate_mass)
        calculate_btn.pack(pady=5)

        self.result_text = tk.Text(self.root, height=12, width=60,
                                   font=("Comic Sans MS", 10), state='disabled')
        self.result_text.pack(pady=10, padx=10)

        clear_btn = ttk.Button(self.root, text="Очистить",
                               command=self.clear_fields)
        clear_btn.pack(pady=5)

        examples_frame = ttk.LabelFrame(self.root, text="Примеры формул")
        examples_frame.pack(pady=10, padx=10, fill="x")

        examples = ["H2O - вода", "CO2 - углекислый газ", "C6H12O6 - глюкоза",
                    "Ca(OH)2 - гашеная известь", "CH3COOH - уксусная кислота"]

        for example in examples:
            example_label = ttk.Label(examples_frame, text=example)
            example_label.pack(anchor="w", padx=5)

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
        formula = self.formula_var.get()

        if not formula:
            messagebox.showwarning("Внимание", "Введите химическую формулу")
            return

        try:
            elements = self.parse_formula(formula)

            if not elements:
                messagebox.showwarning("Внимание", "Не удалось распознать формулу")
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

            self.result_text.insert(tk.END, f"Формула: {formula}\n")
            self.result_text.insert(tk.END, "=" * 45 + "\n")

            for line in result_lines:
                self.result_text.insert(tk.END, line + "\n")

            self.result_text.insert(tk.END, "=" * 45 + "\n")
            self.result_text.insert(tk.END, f"Молекулярная масса: {total_mass:.3f} г/моль\n")
            self.result_text.insert(tk.END, f"Округленно:       {round(total_mass, 2)} г/моль\n")

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
