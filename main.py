import tkinter as tk
from tkinter import Menu, messagebox, ttk, filedialog, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import requests
from datetime import datetime

'''
zadatci:
1. Unos troškova i prihoda - done
2. Pregled financijskih statistika - done
3. Kategorizacija transakcija - done
4. Postavljanje ciljeva - done
5. Praćenje duga - done
6. Podsjetnici i planiranje - nepotrebno
7. Generiranje izvješća - done
8. Sigurnosne značajke (možda implementiram) - nepotrebno
9. Uvoz/izvoz podataka - done
10. Valutni pretvarač - done
'''

class CurrencyConverter:
    def __init__(self):
        self.api_url = "https://open.er-api.com/v6/latest"

    def get_exchange_rates(self):
        try:
            response = requests.get(self.api_url)
            data = response.json()
            return data.get("rates", {})
        except Exception as e:
            print(f"Greška u dohvaćanju valuta: {e}")
            return {}

    def convert_currency(self, amount, from_currency, to_currency):
        exchange_rates = self.get_exchange_rates()

        if not exchange_rates:
            return None
        
        if from_currency.upper() not in exchange_rates or to_currency.upper() not in exchange_rates:
            print("Pogrešna oznaka valute.")
            return None
        
        rate_from = exchange_rates[from_currency.upper()]
        rate_to = exchange_rates[to_currency.upper()]

        converted_amount = amount * (rate_to / rate_from)
        return converted_amount

converter = CurrencyConverter()

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
        self.file_menu.add_command(label="Uvezi podatke", command=self.import_data)
        self.file_menu.add_command(label="Izvezi podatke", command=self.export_data)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Generiraj izvješće", command=self.generate_report)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Izlaz", command=self.exit_program)
        self.menu_bar.add_cascade(label="Datoteka", menu=self.file_menu)

        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Pomoć", command=self.show_help)
        self.menu_bar.add_cascade(label="Pomoć", menu=self.help_menu)

        self.tabControl = ttk.Notebook(self.frame)
        self.tabControl.pack(expand=1, fill="both")

        self.expenses_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.expenses_tab, text="Troškovi")

        self.income_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.income_tab, text="Prihodi")

        self.statistics_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.statistics_tab, text="Statistika")

        self.goals_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.goals_tab, text="Ciljevi")

        self.debts_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.debts_tab, text="Dugovi")

        self.currency_converter_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.currency_converter_tab, text="Valutni pretvarač")

        self.categories = {'Troškovi': {}, 'Prihodi': {}}
        self.goals = {}
        self.debts = []

        self.create_expenses_widgets()
        self.create_income_widgets()
        self.create_statisctics_widgets()
        self.create_goals_widgets()
        self.create_debt_widgets()
        self.create_currency_converter_widgets()
        
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

    def create_goals_widgets(self):
        tk.Label(self.goals_tab, text="Naziv cilja:").grid(row=0, column=0, padx=10, pady=10)
        self.goal_name_entry = tk.Entry(self.goals_tab)
        self.goal_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.goals_tab, text="Iznos cilja:").grid(row=1, column=0, padx=10, pady=10)
        self.goal_amount_entry = tk.Entry(self.goals_tab)
        self.goal_amount_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.goals_tab, text="Dodaj cilj", command=self.add_goal).grid(row=2, column=0, columnspan=2, pady=10)

        self.goals_listbox = tk.Listbox(self.goals_tab, width=50, height=10)
        self.goals_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def create_debt_widgets(self):
        tk.Label(self.debts_tab, text="Opis duga:").grid(row=0, column=0, padx=10, pady=10)
        self.debt_description_entry = tk.Entry(self.debts_tab)
        self.debt_description_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.debts_tab, text="Ukupan iznos duga:").grid(row=1, column=0, padx=10, pady=10)
        self.debt_amount_entry = tk.Entry(self.debts_tab)
        self.debt_amount_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.debts_tab, text="Dodaj dug", command=self.add_debt).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Label(self.debts_tab, text="Indeks duga:").grid(row=3, column=0, padx=10, pady=10)
        self.debt_index_entry = tk.Entry(self.debts_tab)
        self.debt_index_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self.debts_tab, text="Iznos smanjenja:").grid(row=4, column=0, padx=10, pady=10)
        self.debt_reduction_amount_entry = tk.Entry(self.debts_tab)
        self.debt_reduction_amount_entry.grid(row=4, column=1, padx=10, pady=10)

        tk.Button(self.debts_tab, text="Smanji dug", command=self.reduce_debt).grid(row=5, column=0, columnspan=2, pady=10)

        self.debt_listbox = tk.Listbox(self.debts_tab, width=50, height=10)
        self.debt_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10)


    def create_currency_converter_widgets(self):
        tk.Label(self.currency_converter_tab, text="Iznos:").grid(row=0, column=0, padx=10, pady=10)
        self.currency_amount_entry = tk.Entry(self.currency_converter_tab)
        self.currency_amount_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.currency_converter_tab, text="Od valute (kȏd):").grid(row=1, column=0, padx=10, pady=10)
        self.from_currency_entry = tk.Entry(self.currency_converter_tab)
        self.from_currency_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.currency_converter_tab, text="U valutu (kȏd):").grid(row=2, column=0, padx=10, pady=10)
        self.to_currency_entry = tk.Entry(self.currency_converter_tab)
        self.to_currency_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.currency_converter_tab, text="Pretvori", command=self.convert_currency).grid(row=3, column=0, columnspan=2, pady=10)

        self.converted_result_label = tk.Label(self.currency_converter_tab, text="")
        self.converted_result_label.grid(row=4, column=0, columnspan=2, pady=10)

    def convert_currency(self):
        amount_str = self.currency_amount_entry.get()
        from_currency = self.from_currency_entry.get()
        to_currency = self.to_currency_entry.get()

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showwarning("Upozorenje", "Unesite ispravan iznos (samo brojevi!).")

        converted_amount = converter.convert_currency(amount, from_currency, to_currency)

        if converted_amount is not None:
            result_text = f"{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}"
            self.converted_result_label.config(text=result_text)
        else:
            messagebox.showwarning("Upozorenje", "Pretvorba nije uspjela!")        

    def add_goal(self):
        name = self.goal_name_entry.get()
        amount = self.goal_amount_entry.get()

        if name and amount:
            goal_entry = f"{name}: {amount}€"

            for i in range(self.goals_listbox.size()):
                if name in self.goals_listbox.get(i):
                    self.goals_listbox.delete(i)
                    break
            
            self.goals_listbox.insert(tk.END, goal_entry)

            self.goals[name] = float(amount)

            self.goal_name_entry.delete(0, tk.END)
            self.goal_amount_entry.delete(0, tk.END)

    def add_expense(self):
        description = self.expenses_description_entry.get()
        amount = self.expenses_amount_entry.get()
        category = self.expenses_category_entry.get()
        if description and amount:
            expense_entry = f"{category}: {description} - {amount}€"
            self.expenses_listbox.insert(tk.END, expense_entry)

            if category in self.categories['Troškovi']:
                self.categories['Troškovi'][category].append({'description': description, 'amount': float(amount)})
            else:
                self.categories['Troškovi'][category] = [{'description': description, 'amount': float(amount)}]

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
                self.categories['Prihodi'][category].append({'description': description, 'amount': float(amount)})
            else:
                self.categories['Prihodi'][category] = [{'description': description, 'amount': float(amount)}]

            self.income_description_entry.delete(0, tk.END)
            self.income_amount_entry.delete(0, tk.END)
            self.income_category_entry.delete(0, tk.END)

    def show_statistics(self):
        self.plot_category_statistics()

    def add_goal_category(self):
        category = tk.simpledialog.askstring("Dodaj kategoriju ciljeva", "Unesite naziv nove kategorije ciljeva:")
        if category:
            self.goals[category] = 0
            self.goals_listbox.insert(tk.END, category)

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

        values = [sum(transaction['amount'] for transaction in categories[category]) for category in category_names]

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
        if messagebox.askyesno("Nova datoteka", "Jeste li sigurni da želite započeti novu datoteku?"):
            self.categories = {'Troškovi': {}, 'Prihodi': {}}
            self.goals = {}
            self.debts = []

            self.update_interface()

            messagebox.showinfo("Nova datoteka", "Nova datoteka je uspješno otvorena.")
        
    def exit_program(self):
        if messagebox.askyesno("Izlaz", "Jeste li sigurni da želite izaći?"):
            self.master.destroy()

    def import_data(self):
        try:
            file_path = filedialog.askopenfilename(title="Odaberi datoteku", filetypes=[("JSON files", "*.json")])
            if file_path:
                with open(file_path, "r") as file:
                    data = json.load(file)
            
            # uvoz troškova
            imported_categories_expenses = data.get("categories", {}).get("Troškovi", {})
            for category, amounts in imported_categories_expenses.items():
                if category in self.categories['Troškovi']:
                    self.categories['Troškovi'][category].extend(amounts)
                else:
                    self.categories['Troškovi'][category] = amounts

            # uvoz prihoda
            imported_categories_income = data.get("categories", {}).get("Prihodi", {})
            for category, amounts in imported_categories_income.items():
                if category in self.categories['Prihodi']:
                    self.categories['Prihodi'][category].extend(amounts)
                else:
                    self.categories['Prihodi'][category] = amounts
            
            # uvoz ciljeva
            imported_goals = data.get("goals", {})
            for goal, amount in imported_goals.items():
                if goal in self.goals:
                    self.goals[goal] += amount
                else:
                    self.goals[goal] = amount

            # uvoz dugova
            imported_debts = data.get("debts", [])
            self.debts = imported_debts

            self.update_interface()

            messagebox.showinfo("Uvoz podataka", "Podatci su uspješno uvezeni.")

        except FileNotFoundError:
            messagebox.showwarning("Upozorenje", "Datoteka s podatcima nije pronađena.")
        except json.JSONDecodeError:
            messagebox.showerror("Greška", "Pogreška prilikom dekodiranja JSON formata.")
        except Exception as e:
            messagebox.showerror("Greška", f"Neočekivana greška prilikom uvoza podataka: {str(e)}")

    def export_data(self):
        try:
            file_path = filedialog.asksaveasfilename(title="Spremi datoteku", filetypes=[("JSON files", "*.json")])
            if file_path:
                data_to_export = {
                    "categories": self.categories,
                    "goals": self.goals,
                    "debts": self.debts
                }
            
            with open(file_path, "w") as file:
                json.dump(data_to_export, file, indent=2)

            messagebox.showinfo("Izvoz podataka", "Podatci su uspješno izvezeni.")

        except Exception as e:
            messagebox.showerror("Greška", f"Neočekivana greška prilikom izvoza podataka: {str(e)}")

    def update_interface(self):
        self.expenses_listbox.delete(0, tk.END)
        for category, transactions in self.categories['Troškovi'].items():
            for transaction in transactions:
                entry = f"{category}: {transaction['description']} - {transaction['amount']}€"
                self.expenses_listbox.insert(tk.END, entry)

        self.income_listbox.delete(0, tk.END)
        for category, transactions in self.categories['Prihodi'].items():
            for transaction in transactions:
                entry = f"{category}: {transaction['description']} - {transaction['amount']}€"
                self.income_listbox.insert(tk.END, entry)

        self.goals_listbox.delete(0, tk.END)
        for goal, amount in self.goals.items():
            entry = f"{goal}: {amount}€"
            self.goals_listbox.insert(tk.END, entry)

        self.debt_listbox.delete(0, tk.END)
        for debt in self.debts:
            entry = f"{debt['description']} - {debt['amount']}€"
            self.debt_listbox.insert(tk.END, entry)

    def generate_report(self):

        file_path = filedialog.asksaveasfilename(title="Spremi izvješće", defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(f"Izvješće - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                    file.write("Troškovi:\n")
                    for category, expenses in self.categories['Troškovi'].items():
                        for expense in expenses:
                            file.write(f"{category}: {expense['description']} - {expense['amount']}€\n")

                    file.write("\n")

                    file.write("Prihodi:\n")
                    for category, incomes in self.categories['Prihodi'].items():
                        for income in incomes:
                            file.write(f"{category}: {income['description']} - {income['amount']}€\n")

                    file.write("\n")

                    file.write("Ciljevi:\n")
                    for goal, amount in self.goals.items():
                        file.write(f"{goal}: {amount}€\n")

                    file.write("\n")

                    file.write("Dugovi:\n")
                    for debt in self.debts:
                        file.write(f"{debt['description']} - {debt['amount']}€\n")

                messagebox.showinfo("Generiraj izvješće", "Izvješće je uspješno generirano.")
            except Exception as e:
                messagebox.showerror("Greška", f"Neočekivana greška prilikom generacije izvješća: {str(e)}")

    def add_debt(self):
        description = self.debt_description_entry.get()
        total_amount = self.debt_amount_entry.get()

        if description and total_amount:
            debt_entry = f"{description} - {total_amount}€"
            self.debt_listbox.insert(tk.END, debt_entry)

            debt = {'description': description, 'amount': float(total_amount)}
            self.debts.append(debt)

            self.debt_description_entry.delete(0, tk.END)
            self.debt_amount_entry.delete(0, tk.END)

    def reduce_debt(self):
        try:
            index = int(self.debt_index_entry.get())
            if 0 <= index < len(self.debts):
                amount_str = self.debt_reduction_amount_entry.get()
                try:
                    reduction_amount = float(amount_str)
                    if 0 < reduction_amount <= self.debts[index]['amount']:
                        self.debts[index]['amount'] -= reduction_amount
                        self.update_interface()
                    else:
                        messagebox.showwarning("Upozorenje", "Unesite ispravan iznos smanjnja duga.")
                except ValueError:
                    messagebox.showwarning("Upozorenje", "Unesite ispravan iznos smanjenja duga (unose se samo brojevi!).")
            else:
                messagebox.showwarning("Upozorenje", "Unesite ispravan index duga koji želite smanjiti.")
        except ValueError:
            messagebox.showwarning("Upozorenje", "Unesite ispravan index duga koji želite smanjiti (samo cijeli broj!).")

    def show_help(self):
        messagebox.showinfo("Pomoć", "")

def main(): 
    root = tk.Tk()
    root.iconbitmap('fp_logo.ico')
    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()