import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import json
import os

class MeasurementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Measurement Converter and Visual Comparison")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.data_file = "objects_data.json"  # File to store object details
        self.objects = self.load_objects()  # Load object details from file or initialize empty dictionary

        self.create_main_menu()

    def create_main_menu(self):
        self.main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.main_frame, text="Welcome to the Measurement and Visualizer Tool!", font=("Arial", 22)).pack(pady=20)

        ttk.Button(self.main_frame, text="Measurement Converter", command=self.open_converter, style="TButton").pack(pady=10)
        ttk.Button(self.main_frame, text="Visual Comparison Device", command=self.open_comparison_device, style="TButton").pack(pady=10)

    def open_converter(self):
        # Open UnitConverterApp in a new window
        converter_window = tk.Toplevel(self.root)
        UnitConverterApp(converter_window)

    def open_comparison_device(self):
        self.main_frame.pack_forget()  # Hide the main menu
        self.create_comparison_device()

    def create_comparison_device(self):
        self.comparison_frame = ttk.Frame(self.root, padding="20 20 20 20")
        self.comparison_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.comparison_frame, text="Visual Comparison Device", font=("Arial", 24)).pack(pady=20)

        self.object1_var = tk.StringVar()
        self.object2_var = tk.StringVar()

        ttk.Label(self.comparison_frame, text="Select the first object:", font=("Arial", 14)).pack(pady=5)
        self.object1_menu = ttk.Combobox(self.comparison_frame, textvariable=self.object1_var, font=("Arial", 12))
        self.object1_menu.pack(pady=5)

        ttk.Label(self.comparison_frame, text="Select the second object:", font=("Arial", 14)).pack(pady=5)
        self.object2_menu = ttk.Combobox(self.comparison_frame, textvariable=self.object2_var, font=("Arial", 12))
        self.object2_menu.pack(pady=5)

        self.update_object_menus()

        button_frame = ttk.Frame(self.comparison_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Compare Objects", command=self.compare_objects, style="TButton").grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Add Item", command=self.open_add_item, style="TButton").grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Remove Object", command=self.open_remove_item, style="TButton").grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Back to Main Menu", command=self.back_to_main_menu, style="TButton").grid(row=0, column=3, padx=5)

    def update_object_menus(self):
        object_names = list(self.objects.keys())
        self.object1_menu['values'] = object_names
        self.object2_menu['values'] = object_names

    def compare_objects(self):
        object1 = self.object1_var.get()
        object2 = self.object2_var.get()

        if not object1 or not object2:
            messagebox.showerror("Error", "Please select two objects to compare.")
            return

        obj1_details = self.objects.get(object1)
        obj2_details = self.objects.get(object2)

        if not obj1_details or not obj2_details:
            messagebox.showerror("Error", "Invalid object details.")
            return

        self.display_comparison(object1, obj1_details, object2, obj2_details)

    def display_comparison(self, object1, obj1_details, object2, obj2_details):
        comparison_window = tk.Toplevel(self.root)
        comparison_window.title("Comparison Result")
        comparison_window.configure(bg="#f0f0f0")

        ttk.Label(comparison_window, text=f"Comparing {object1} with {object2}", font=("Arial", 18)).pack(pady=20)

        # Calculate scaling factors
        max_dimension = 200  # Max dimension for the largest object

        obj1_area = obj1_details["width"] * obj1_details["height"]
        obj2_area = obj2_details["width"] * obj2_details["height"]

        obj1_scale = (obj1_area / max(obj1_area, obj2_area)) ** 0.5
        obj2_scale = (obj2_area / max(obj1_area, obj2_area)) ** 0.5

        # Ensure the scale factors are not zero or negative
        obj1_scale = max(obj1_scale, 0.01)
        obj2_scale = max(obj2_scale, 0.01)

        try:
            obj1_img = Image.open(obj1_details["path"])
            obj1_img = obj1_img.resize((int(max_dimension * obj1_scale), int(max_dimension * obj1_scale)), Image.Resampling.LANCZOS)
            obj1_img = ImageTk.PhotoImage(obj1_img)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image for {object1}: {e}")
            return

        try:
            obj2_img = Image.open(obj2_details["path"])
            obj2_img = obj2_img.resize((int(max_dimension * obj2_scale), int(max_dimension * obj2_scale)), Image.Resampling.LANCZOS)
            obj2_img = ImageTk.PhotoImage(obj2_img)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image for {object2}: {e}")
            return

        comparison_frame = ttk.Frame(comparison_window, padding="20 20 20 20")
        comparison_frame.pack(fill=tk.BOTH, expand=True)

        obj1_frame = ttk.Frame(comparison_frame)
        obj1_frame.pack(side="left", padx=20, pady=20)

        obj2_frame = ttk.Frame(comparison_frame)
        obj2_frame.pack(side="right", padx=20, pady=20)

        obj1_label = ttk.Label(obj1_frame, image=obj1_img)
        obj1_label.image = obj1_img  # Keep a reference to avoid garbage collection
        obj1_label.pack()

        ttk.Label(obj1_frame, text=f"{object1} - Width: {obj1_details['width']} units", font=("Arial", 14)).pack(pady=10)
        ttk.Label(obj1_frame, text=f"Height: {obj1_details['height']} units", font=("Arial", 14)).pack(pady=10)

        obj2_label = ttk.Label(obj2_frame, image=obj2_img)
        obj2_label.image = obj2_img  # Keep a reference to avoid garbage collection
        obj2_label.pack()

        ttk.Label(obj2_frame, text=f"{object2} - Width: {obj2_details['width']} units", font=("Arial", 14)).pack(pady=10)
        ttk.Label(obj2_frame, text=f"Height: {obj2_details['height']} units", font=("Arial", 14)).pack(pady=10)

    def open_add_item(self):
        self.comparison_frame.pack_forget()
        self.create_add_item()

    def create_add_item(self):
        self.add_item_frame = ttk.Frame(self.root, padding="20 20 20 20")
        self.add_item_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.add_item_frame, text="Add New Item", font=("Arial", 24)).pack(pady=20)

        ttk.Label(self.add_item_frame, text="Item Name:", font=("Arial", 14)).pack(pady=5)
        self.item_name_var = tk.StringVar()
        ttk.Entry(self.add_item_frame, textvariable=self.item_name_var, font=("Arial", 12)).pack(pady=5)

        ttk.Label(self.add_item_frame, text="Item Image:", font=("Arial", 14)).pack(pady=5)
        self.uploaded_image_path = tk.StringVar()
        ttk.Entry(self.add_item_frame, textvariable=self.uploaded_image_path, state='readonly', font=("Arial", 12)).pack(pady=5)
        ttk.Button(self.add_item_frame, text="Upload Image", command=self.upload_image, style="TButton").pack(pady=5)

        ttk.Label(self.add_item_frame, text="Item Width:", font=("Arial", 14)).pack(pady=5)
        self.item_width_var = tk.StringVar()
        ttk.Entry(self.add_item_frame, textvariable=self.item_width_var, font=("Arial", 12)).pack(pady=5)

        ttk.Label(self.add_item_frame, text="Item Height:", font=("Arial", 14)).pack(pady=5)
        self.item_height_var = tk.StringVar()
        ttk.Entry(self.add_item_frame, textvariable=self.item_height_var, font=("Arial", 12)).pack(pady=5)

        ttk.Button(self.add_item_frame, text="Upload Item", command=self.upload_item, style="TButton").pack(pady=10)
        ttk.Button(self.add_item_frame, text="Back to Comparison Device", command=self.back_to_comparison_device, style="TButton").pack(pady=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.uploaded_image_path.set(file_path)

    def upload_item(self):
        item_name = self.item_name_var.get()
        image_path = self.uploaded_image_path.get()
        item_width = self.item_width_var.get()
        item_height = self.item_height_var.get()

        try:
            item_width = float(item_width)
            item_height = float(item_height)
        except ValueError:
            messagebox.showerror("Error", "Width and Height must be valid numbers.")
            return

        if not item_name or not image_path or item_width <= 0 or item_height <= 0:
            messagebox.showerror("Error", "Please fill all fields with valid values and upload an image.")
            return

        self.objects[item_name] = {
            "path": image_path,
            "width": item_width,
            "height": item_height
        }

        self.save_objects()  # Save objects to file

        messagebox.showinfo("Success", f"Item '{item_name}' uploaded successfully.")
        self.update_object_menus()
        self.back_to_comparison_device()

    def open_remove_item(self):
        # Open a window to remove an existing object
        self.remove_window = tk.Toplevel(self.root)
        self.remove_window.title("Remove Object")
        self.remove_window.geometry("400x200")
        ttk.Label(self.remove_window, text="Select object to remove:", font=("Arial", 14)).pack(pady=20)

        self.remove_object_var = tk.StringVar()
        remove_combo = ttk.Combobox(self.remove_window, textvariable=self.remove_object_var, state="readonly", font=("Arial", 12))
        remove_combo['values'] = list(self.objects.keys())
        remove_combo.pack(pady=10)

        ttk.Button(self.remove_window, text="Remove", command=self.remove_object, style="TButton").pack(pady=10)

    def remove_object(self):
        object_to_remove = self.remove_object_var.get()
        if not object_to_remove:
            messagebox.showerror("Error", "Please select an object to remove.")
            return

        confirm = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove '{object_to_remove}'?")
        if confirm:
            if object_to_remove in self.objects:
                del self.objects[object_to_remove]
                self.save_objects()
                messagebox.showinfo("Success", f"Object '{object_to_remove}' has been removed.")
                self.remove_window.destroy()
                self.update_object_menus()
            else:
                messagebox.showerror("Error", "The selected object does not exist.")

    def load_objects(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                return json.load(file)
        return {}

    def save_objects(self):
        with open(self.data_file, "w") as file:
            json.dump(self.objects, file, indent=4)

    def back_to_main_menu(self):
        self.comparison_frame.pack_forget()
        self.create_main_menu()

    def back_to_comparison_device(self):
        self.add_item_frame.pack_forget()
        self.create_comparison_device()

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

        # Setup main frame for the unit converter
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

        # Button to add a new unit of measurement
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

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=10)
    style.configure("TLabel", background="#f0f0f0")

    app = MeasurementApp(root)
    root.mainloop()