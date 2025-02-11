import tkinter as tk
from tkinter import ttk, messagebox

class UnitConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Unit Converter")
        self.root.geometry("500x400")

        self.conversion_factors = {
            "Distance": {
                "millimeters": 1,
                "centimeters": 10,
                "meters": 1000,
                "kilometers": 1000000,
                "inches": 25.4,
                "feet": 304.8,
                "yards": 914.4,
                "miles": 1609344,
                "lí": 500,
                "fēn": 3.333,
                "cùn": 33.333,
                "chǐ": 333.333,
                "bù": 1500,
                "zhàng": 3333.333,
                "lǐ": 500000
            },
            "Weight": {
                "milligram": 1,
                "gram": 1000,
                "kilogram": 1000000,
                "ton": 1000000000,
                "pound": 453592.37,
                "ounce": 28349.5231,
                "háo": 0.1,
                "lí": 1,
                "fēn": 10,
                "qián": 500,
                "liǎng": 5000,
                "jīn": 50000,
                "dàn": 50000000
            },
            "Area": {
                "square millimeters": 1,
                "square centimeters": 100,
                "square meters": 1000000,
                "square kilometers": 1000000000000,
                "square inches": 645.16,
                "square feet": 92903.04,
                "square yards": 836127.36,
                "square miles": 2589988110336,
                "háo": 0.1,
                "lí": 1,
                "fēn": 10,
                "mǔ": 666666.67,
                "qǐng": 666666666.67
            },
            "Volume": {
                "milliliters": 1,
                "liters": 1000,
                "gallons": 3785.41,
                "quarts": 946.353,
                "tea spoons": 4.92892,
                "table spoons": 14.7868,
                "sháo": 1,
                "gě": 30,
                "shēng": 1000,
                "dǒu": 10000,
                "hú": 100000,
                "dàn": 1000000
            }
        }

        # Setup main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)

        tk.Label(self.main_frame, text="Unit Converter", font=("Helvetica", 16)).grid(row=0, columnspan=2, pady=10)

        # Category selection
        tk.Label(self.main_frame, text="Category:").grid(row=1, column=0, padx=10, pady=10)
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.main_frame, textvariable=self.category_var, state="readonly")
        self.category_dropdown['values'] = ("Distance", "Weight", "Area", "Volume")
        self.category_dropdown.grid(row=1, column=1, padx=10, pady=10)
        self.category_dropdown.bind("<<ComboboxSelected>>", self.update_units)

        # Units selection
        tk.Label(self.main_frame, text="From Unit:").grid(row=2, column=0, padx=10, pady=10)
        self.unit_from_var = tk.StringVar()
        self.unit_from_dropdown = ttk.Combobox(self.main_frame, textvariable=self.unit_from_var, state="readonly")
        self.unit_from_dropdown.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.main_frame, text="To Unit:").grid(row=3, column=0, padx=10, pady=10)
        self.unit_to_var = tk.StringVar()
        self.unit_to_dropdown = ttk.Combobox(self.main_frame, textvariable=self.unit_to_var, state="readonly")
        self.unit_to_dropdown.grid(row=3, column=1, padx=10, pady=10)

        # Entry for value to convert
        tk.Label(self.main_frame, text="Value:").grid(row=4, column=0, padx=10, pady=10)
        self.value_entry = tk.Entry(self.main_frame)
        self.value_entry.grid(row=4, column=1, padx=10, pady=10)

        # Button to perform conversion
        self.convert_button = tk.Button(self.main_frame, text="Convert", command=self.perform_conversion, bg="green", fg="white", font=("Helvetica", 12, "bold"))
        self.convert_button.grid(row=5, columnspan=2, pady=10)

        # Label to display result
        self.result_label = tk.Label(self.main_frame, text="", font=("Helvetica", 14), fg="blue")
        self.result_label.grid(row=6, columnspan=2, pady=10)

        # Button to add new unit of measurement
        self.add_unit_button = tk.Button(self.main_frame, text="Add Unit of Measurement", command=self.open_add_unit_window)
        self.add_unit_button.grid(row=7, columnspan=2, pady=10)

    def update_units(self, event):
        category = self.category_var.get()
        if category in self.conversion_factors:
            units = list(self.conversion_factors[category].keys())
            self.unit_from_dropdown['values'] = units
            self.unit_to_dropdown['values'] = units

    def perform_conversion(self):
        try:
            value = float(self.value_entry.get())
            unit_from = self.unit_from_var.get()
            unit_to = self.unit_to_var.get()
            category = self.category_var.get()

            if category in self.conversion_factors:
                factors = self.conversion_factors[category]
                if unit_from in factors and unit_to in factors:
                    base_value = value * factors[unit_from]
                    converted_value = base_value / factors[unit_to]
                    self.result_label.config(text=f"{value} {unit_from} is {converted_value:.4f} {unit_to}")
                else:
                    messagebox.showerror("Invalid units", "Please select valid units.")
            else:
                messagebox.showerror("Invalid category", "Please select a valid category.")
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid numeric value.")

    def open_add_unit_window(self):
        self.add_unit_window = tk.Toplevel(self.root)
        self.add_unit_window.title("Add Unit of Measurement")

        tk.Label(self.add_unit_window, text="Category:").grid(row=0, column=0, padx=10, pady=10)
        self.add_category_var = tk.StringVar()
        self.add_category_dropdown = ttk.Combobox(self.add_unit_window, textvariable=self.add_category_var, state="readonly")
        self.add_category_dropdown['values'] = ("Distance", "Weight", "Area", "Volume")
        self.add_category_dropdown.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.add_unit_window, text="Unit Name:").grid(row=1, column=0, padx=10, pady=10)
        self.add_unit_name_entry = tk.Entry(self.add_unit_window)
        self.add_unit_name_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.add_unit_window, text="Conversion Factor:").grid(row=2, column=0, padx=10, pady=10)
        self.add_conversion_factor_entry = tk.Entry(self.add_unit_window)
        self.add_conversion_factor_entry.grid(row=2, column=1, padx=10, pady=10)

        self.conversion_factor_explanation = tk.Label(
            self.add_unit_window,
            text="Conversion Factor: The ratio of the new unit to the base unit (e.g., millimeters for distance, milligrams for weight)."
        )
        self.conversion_factor_explanation.grid(row=3, columnspan=2, padx=10, pady=10)

        self.add_unit_button = tk.Button(self.add_unit_window, text="Add Unit", command=self.add_unit)
        self.add_unit_button.grid(row=4, columnspan=2, pady=10)

    def add_unit(self):
        category = self.add_category_var.get()
        unit_name = self.add_unit_name_entry.get()
        conversion_factor = self.add_conversion_factor_entry.get()

        if category and unit_name and conversion_factor:
            try:
                conversion_factor = float(conversion_factor)
                if category in self.conversion_factors:
                    self.conversion_factors[category][unit_name] = conversion_factor
                    messagebox.showinfo("Success", f"Added unit {unit_name} to {category} category.")
                    self.add_unit_window.destroy()
                else:
                    messagebox.showerror("Invalid category", "Please select a valid category.")
            except ValueError:
                messagebox.showerror("Invalid input", "Please enter a valid numeric value for conversion factor.")
        else:
            messagebox.showerror("Missing information", "Please fill in all fields.")

if __name__ == "__main__":
    root = tk.Tk()
    app = UnitConverterApp(root)
    root.mainloop()