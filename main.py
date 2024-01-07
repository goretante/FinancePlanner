import tkinter as tk
from tkinter import Menu, messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

'''
zadatci:
1. Unos troškova i prihoda - done
2. Pregled financijskih statistika - done
3. Kategorizacija transakcija - work in progress
4. Postavljanje ciljeva
5. Praćenje duga
6. Podsjetnici i planiranje
7. Generiranje izvješća
8. Sigurnosne značajke (možda implementiram)
9. Uvoz/izvoz podataka
10. Valutni pretvarač
'''

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Financijski planer")
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)
        
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Novi")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Izlaz", command=self.exit_program)
        self.menu_bar.add_cascade(label="Datoteka", menu=self.file_menu)

        self.tabControl = ttk.Notebook(self.frame)
        self.tabControl.pack(expand=1, fill="both")

        self.expenses_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.expenses_tab, text="Troškovi")

        self.income_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.income_tab, text="Prihodi")

        self.statistics_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.statistics_tab, text="Statistika")

        self.categories = {'Troškovi': {}, 'Prihodi': {}}

        self.create_expenses_widgets()
        self.create_income_widgets()
        self.create_statisctics_widgets()
        
    def create_expenses_widgets(self):
        tk.Label(self.expenses_tab, text="Opis troška:").grid(row=0, column=0, padx=10, pady=10)
        self.expenses_description_entry = tk.Entry(self.expenses_tab)
        self.expenses_description_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.expenses_tab, text="Iznos troška:").grid(row=1, column=0, padx=10, pady=10)
        self.expenses_amount_entry = tk.Entry(self.expenses_tab)
        self.expenses_amount_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.expenses_tab, text="Kategorija troška:").grid(row=2, column=0, padx=10, pady=10)
        self.expenses_category_entry = tk.Entry(self.expenses_tab)
        self.expenses_category_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.expenses_tab, text="Dodaj Trošak", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=10)

        self.expenses_listbox = tk.Listbox(self.expenses_tab, width=50, height=10)
        self.expenses_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def create_income_widgets(self):
        tk.Label(self.income_tab, text="Opis prihoda:").grid(row=0, column=0, padx=10, pady=10)
        self.income_description_entry = tk.Entry(self.income_tab)
        self.income_description_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.income_tab, text="Iznos prihoda:").grid(row=1, column=0, padx=10, pady=10)
        self.income_amount_entry = tk.Entry(self.income_tab)
        self.income_amount_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.income_tab, text="Kategorija prihoda:").grid(row=2, column=0, padx=10, pady=10)
        self.income_category_entry = tk.Entry(self.income_tab)
        self.income_category_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.income_tab, text="Dodaj Prihod", command=self.add_income).grid(row=3, column=0, columnspan=2, pady=10)

        self.income_listbox = tk.Listbox(self.income_tab, width=50, height=10)
        self.income_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def create_statisctics_widgets(self):
        tk.Button(self.statistics_tab, text="Prikaži statistiku", command=self.show_statistics).pack(pady=20)

    def add_expense(self):
        description = self.expenses_description_entry.get()
        amount = self.expenses_amount_entry.get()
        category = self.expenses_category_entry.get()
        if description and amount:
            expense_entry = f"{category}: {description} - {amount}€"
            self.expenses_listbox.insert(tk.END, expense_entry)

            if category in self.categories['Troškovi']:
                self.categories['Troškovi'][category].append(float(amount))
            else:
                self.categories['Troškovi'][category] = [float(amount)]
            
            self.expenses_description_entry.delete(0, tk.END)
            self.expenses_amount_entry.delete(0, tk.END)
            self.expenses_category_entry.delete(0, tk.END)

    def add_income(self):
        description = self.income_description_entry.get()
        amount = self.income_amount_entry.get()
        category = self.income_category_entry.get()
        if description and amount:
            income_entry = f"{category}: {description} - {amount}€"
            self.income_listbox.insert(tk.END, income_entry)

            if category in self.categories['Prihodi']:
                self.categories['Prihodi'][category].append(float(amount))
            else:
                self.categories['Prihodi'][category] = [float(amount)]


            self.income_description_entry.delete(0, tk.END)
            self.income_amount_entry.delete(0, tk.END)
            self.income_category_entry.delete(0, tk.END)

    def show_statistics(self):
        self.plot_category_statistics()

    def plot_category_statistics(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

        self.plot_bar_chart(ax1, 'Troškovi', self.categories['Troškovi'])
        self.plot_bar_chart(ax2, 'Prihodi', self.categories['Prihodi'])

        plt.show()

    def get_entries_from_listbox(self, listbox):
        return listbox.get(0, tk.END)
    
    def extract_amount(self, entry):
        try:
            return float(entry.split(":")[-1].strip())
        except ValueError:
            return 0.0

    def plot_bar_chart(self, ax, title, categories):
        category_names = list(categories.keys())
        values = [sum(categories[category]) for category in category_names]

        bars = ax.bar(category_names, values, color='blue')

        ax.set_ylabel('Iznos')
        ax.set_title(f'Grafikon {title}')

        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.annotate(f'{value:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

    def new_file(self):
        messagebox.showinfo("Info", "Otvorena je nova datoteka")
        
    def exit_program(self):
        if messagebox.askyesno("Izlaz", "Jeste li sigurni da želite izaći?"):
            self.master.destroy()

def main(): 
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()