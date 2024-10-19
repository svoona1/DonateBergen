import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import csv
from fpdf import FPDF

# Colors and Fonts
BG_COLOR = "#f5f5f5"
FONT_NORMAL = ("Helvetica", 12)

donations = []  # Store donation rows

def validate_numeric_input(action, value):
    """Validate that only numeric input is allowed."""
    return value.isdigit() or value == ""

def add_donation_row():
    """Add a new row to the donation input window."""
    row_index = len(donations) + 1

    # Create variables for the inputs
    name_var = tk.StringVar()
    email_var = tk.StringVar()
    address_var = tk.StringVar()  # New Address Field
    city_var = tk.StringVar()  # New City Field
    quantity_var = tk.StringVar()
    condition_var = tk.StringVar(value="New")
    item_name_var = tk.StringVar()

    # Input Fields for the Row
    tk.Entry(input_frame, textvariable=name_var, width=15).grid(row=row_index, column=0, padx=5, pady=5)
    tk.Entry(input_frame, textvariable=email_var, width=25).grid(row=row_index, column=1, padx=5, pady=5)
    tk.Entry(input_frame, textvariable=address_var, width=20).grid(row=row_index, column=2, padx=5, pady=5)  # Address Field
    tk.Entry(input_frame, textvariable=city_var, width=15).grid(row=row_index, column=3, padx=5, pady=5)  # City Field

    validate_command = (root.register(validate_numeric_input), "%d", "%P")
    tk.Entry(input_frame, textvariable=quantity_var, validate="key", validatecommand=validate_command, width=10).grid(row=row_index, column=4, padx=5, pady=5)

    ttk.Combobox(input_frame, textvariable=condition_var, values=["New", "Used"], state="readonly", width=10).grid(row=row_index, column=5, padx=5, pady=5)
    tk.Entry(input_frame, textvariable=item_name_var, width=20).grid(row=row_index, column=6, padx=5, pady=5)

    # Confirm and Delete Buttons
    tk.Button(input_frame, text="✔️", command=lambda: confirm_entry(name_var, email_var)).grid(row=row_index, column=7, padx=5)
    tk.Button(input_frame, text="❌", command=lambda: delete_row(row_index)).grid(row=row_index, column=8, padx=5)

    # Store the row’s data
    donations.append({
        "name": name_var, "email": email_var, "address": address_var, "city": city_var,
        "quantity": quantity_var, "condition": condition_var, "item_name": item_name_var
    })

def confirm_entry(name_var, email_var):
    """Confirm the entry."""
    if not name_var.get() or not email_var.get():
        messagebox.showwarning("Input Error", "Please enter both name and email.")
    else:
        messagebox.showinfo("Confirmed", "Entry confirmed!")

def delete_row(row_index):
    """Delete a row."""
    donations.pop(row_index - 1)
    for widget in input_frame.grid_slaves(row=row_index):
        widget.destroy()

def save_donations():
    """Save donations to file."""
    with open("DonateBergen.txt", "a") as file:
        for donation in donations:
            file.write(f"{donation['name'].get()},{donation['email'].get()},"
                       f"{donation['address'].get()},{donation['city'].get()},"
                       f"{donation['quantity'].get()},{donation['condition'].get()},"
                       f"{donation['item_name'].get()}\n")
    messagebox.showinfo("Success", "Donations saved successfully!")
    donation_window.destroy()

def show_add_donation_window():
    """Open the Add Donations window."""
    global donation_window, input_frame

    donation_window = tk.Toplevel(root)
    donation_window.title("Add Donation Items")
    donation_window.geometry("1200x500")
    donation_window.config(bg=BG_COLOR)

    input_frame = tk.Frame(donation_window, bg=BG_COLOR)
    input_frame.pack(fill="x", padx=10, pady=10)

    # Column Labels
    headers = ["Name", "Email", "Address", "City", "Quantity", "Condition", "Item Name", "Confirm", "Delete"]
    for idx, header in enumerate(headers):
        tk.Label(input_frame, text=header, font=FONT_NORMAL, bg=BG_COLOR).grid(row=0, column=idx, padx=5, pady=5)

    add_donation_row()

    button_frame = tk.Frame(donation_window, bg=BG_COLOR)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Add Another Item", command=add_donation_row, font=FONT_NORMAL).grid(row=0, column=0, padx=10)
    tk.Button(button_frame, text="Save Donations", command=save_donations, font=FONT_NORMAL).grid(row=0, column=1, padx=10)

def view_donations():
    """Display donations in a table."""
    global donations
    donations = []

    try:
        with open("DonateBergen.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(",")
                if len(parts) == 7:
                    donations.append({"name": parts[0], "email": parts[1], "address": parts[2], "city": parts[3],
                                      "quantity": parts[4], "condition": parts[5], "item_name": parts[6]})
    except FileNotFoundError:
        messagebox.showwarning("File Error", "DonateBergen.txt not found.")
        return

    view_window = tk.Toplevel(root)
    view_window.title("View Donations")
    view_window.geometry("1000x400")
    view_window.config(bg=BG_COLOR)

    tree = ttk.Treeview(view_window, columns=("Name", "Email", "Address", "City", "Quantity", "Condition", "Item Name"), show="headings")
    for col in ("Name", "Email", "Address", "City", "Quantity", "Condition", "Item Name"):
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    for donation in donations:
        tree.insert("", "end", values=(donation["name"], donation["email"], donation["address"], donation["city"],
                                       donation["quantity"], donation["condition"], donation["item_name"]))

    button_frame = tk.Frame(view_window, bg=BG_COLOR)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Export to CSV", command=export_to_csv, font=FONT_NORMAL).grid(row=0, column=0, padx=10)
    tk.Button(button_frame, text="Export to PDF", command=export_to_pdf, font=FONT_NORMAL).grid(row=0, column=1, padx=10)

def export_to_csv():
    """Export donations to a CSV file."""
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Email", "Address", "City", "Quantity", "Condition", "Item Name"])
            for donation in donations:
                writer.writerow([donation["name"], donation["email"], donation["address"], donation["city"],
                                 donation["quantity"], donation["condition"], donation["item_name"]])
        messagebox.showinfo("Success", "Donations exported to CSV successfully!")

def export_to_pdf():
    """Export donations to a well-formatted PDF."""
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(280, 10, txt="Donations List", ln=True, align="C")
        pdf.ln(10)

        headers = ["Name", "Email", "Address", "City", "Quantity", "Condition", "Item Name"]
        for header in headers:
            pdf.cell(35, 10, header, 1, 0, 'C')
        pdf.ln()

        for donation in donations:
            for value in donation.values():
                pdf.cell(35, 10, value, 1)
            pdf.ln()

        pdf.output(file_path)
        messagebox.showinfo("Success", "Donations exported to PDF successfully!")

root = tk.Tk()
root.title("DonateBergen")
root.geometry("400x300")
root.config(bg=BG_COLOR)

tk.Label(root, text="DonateBergen", font=("Helvetica", 16, "bold"), bg=BG_COLOR).pack(pady=15)

button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=20)

tk.Button(button_frame, text="Add Donation Item", command=show_add_donation_window, font=FONT_NORMAL).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="View Donations", command=view_donations, font=FONT_NORMAL).grid(row=1, column=0, padx=10)

root.mainloop()
