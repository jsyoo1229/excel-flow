import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from main import clean_csv_files


def select_folder():
    folder = filedialog.askdirectory(
        title="Select CSV Folder"
    )

    if folder:
        folder_path.set(folder)

        if not output_path.get():
            output_path.set(
                str(Path(folder) / "cleaned_data.xlsx")
            )


def select_output_file():
    file = filedialog.asksaveasfilename(
        title="Save Cleaned Excel File",
        defaultextension=".xlsx",
        filetypes=[
            ("Excel files", "*.xlsx")
        ]
    )

    if file:
        output_path.set(file)


def clean_files():
    folder = folder_path.get()
    output = output_path.get()

    if not folder:
        messagebox.showwarning(
            "No folder selected",
            "Please select a folder containing CSV files."
        )
        return

    if not output:
        messagebox.showwarning(
            "No output file selected",
            "Please select where the cleaned Excel file should be saved."
        )
        return

    data_folder = Path(folder)
    output_file = Path(output)

    remove_missing = (
        missing_option.get() == "remove"
    )

    clean_button.config(
        text="Cleaning...",
        state="disabled"
    )
    root.update_idletasks()

    try:
        summary = clean_csv_files(
            data_folder,
            output_file,
            remove_missing
        )

    except Exception as error:
        messagebox.showerror(
            "Cleaning failed",
            str(error)
        )

    else:
        result_text = (
            f"Files processed: {summary['files_processed']}\n"
            f"Files skipped: {summary['files_skipped']}\n"
            f"Files failed: {summary['files_failed']}\n\n"
            f"Duplicates removed: "
            f"{summary['duplicate_rows_removed']}\n"
            f"Missing rows removed: "
            f"{summary['missing_rows_removed']}\n"
            f"Rows after cleaning: "
            f"{summary['rows_after_cleaning']}\n\n"
            f"Saved to:\n{output_file}"
        )

        messagebox.showinfo(
            "Cleaning complete",
            result_text
        )

    finally:
        clean_button.config(
            text="Clean CSV Files",
            state="normal"
        )


# --------------------------------------------------
# Main window
# --------------------------------------------------

root = tk.Tk()

if getattr(sys, "frozen", False):
    base_path = Path(sys._MEIPASS)
else:
    base_path = Path(__file__).parent

root.iconbitmap(
    base_path / "assets" / "excel-flow.ico"
)

root.title("Excel Flow")
root.geometry("720x650")
root.resizable(False, False)
root.configure(bg="#f5f7fa")


# --------------------------------------------------
# Variables
# --------------------------------------------------

folder_path = tk.StringVar()
output_path = tk.StringVar()

missing_option = tk.StringVar(
    value="remove"
)


# --------------------------------------------------
# Styles
# --------------------------------------------------

style = ttk.Style()

style.configure(
    "TEntry",
    padding=7
)

style.configure(
    "Secondary.TButton",
    font=("Segoe UI", 10),
    padding=(12, 7)
)

style.configure(
    "Primary.TButton",
    font=("Segoe UI", 11, "bold"),
    padding=(18, 11)
)

style.configure(
    "TRadiobutton",
    background="#ffffff",
    font=("Segoe UI", 10)
)


# --------------------------------------------------
# Header
# --------------------------------------------------

header = tk.Frame(
    root,
    bg="#f5f7fa"
)

header.pack(
    fill="x",
    padx=55,
    pady=(35, 22)
)


title_label = tk.Label(
    header,
    text="Excel Flow",
    font=("Segoe UI", 25, "bold"),
    bg="#f5f7fa",
    fg="#1f2937"
)

title_label.pack()


subtitle_label = tk.Label(
    header,
    text="Combine, clean, and export your CSV files to Excel.",
    font=("Segoe UI", 10),
    bg="#f5f7fa",
    fg="#6b7280"
)

subtitle_label.pack(
    pady=(7, 0)
)


# --------------------------------------------------
# Main card
# --------------------------------------------------

card = tk.Frame(
    root,
    bg="#ffffff",
    highlightbackground="#dfe3e8",
    highlightthickness=1
)

card.pack(
    fill="both",
    expand=True,
    padx=55,
    pady=(0, 40)
)


content = tk.Frame(
    card,
    bg="#ffffff"
)

content.pack(
    fill="both",
    expand=True,
    padx=32,
    pady=27
)


# --------------------------------------------------
# Input folder
# --------------------------------------------------

input_label = tk.Label(
    content,
    text="CSV folder",
    font=("Segoe UI", 10, "bold"),
    bg="#ffffff",
    fg="#374151"
)

input_label.pack(
    anchor="w"
)


input_help = tk.Label(
    content,
    text="Select the folder containing the CSV files you want to combine.",
    font=("Segoe UI", 9),
    bg="#ffffff",
    fg="#6b7280"
)

input_help.pack(
    anchor="w",
    pady=(2, 7)
)


input_frame = tk.Frame(
    content,
    bg="#ffffff"
)

input_frame.pack(
    fill="x",
    pady=(0, 19)
)


folder_entry = ttk.Entry(
    input_frame,
    textvariable=folder_path
)

folder_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 10)
)


browse_button = ttk.Button(
    input_frame,
    text="Browse",
    style="Secondary.TButton",
    command=select_folder
)

browse_button.pack(
    side="right"
)


# --------------------------------------------------
# Output file
# --------------------------------------------------

output_label = tk.Label(
    content,
    text="Output file",
    font=("Segoe UI", 10, "bold"),
    bg="#ffffff",
    fg="#374151"
)

output_label.pack(
    anchor="w"
)


output_help = tk.Label(
    content,
    text="Choose where the cleaned Excel file should be saved.",
    font=("Segoe UI", 9),
    bg="#ffffff",
    fg="#6b7280"
)

output_help.pack(
    anchor="w",
    pady=(2, 7)
)


output_frame = tk.Frame(
    content,
    bg="#ffffff"
)

output_frame.pack(
    fill="x",
    pady=(0, 19)
)


output_entry = ttk.Entry(
    output_frame,
    textvariable=output_path
)

output_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 10)
)


output_button = ttk.Button(
    output_frame,
    text="Save As",
    style="Secondary.TButton",
    command=select_output_file
)

output_button.pack(
    side="right"
)


# --------------------------------------------------
# Missing values
# --------------------------------------------------

missing_label = tk.Label(
    content,
    text="Missing values",
    font=("Segoe UI", 10, "bold"),
    bg="#ffffff",
    fg="#374151"
)

missing_label.pack(
    anchor="w"
)


missing_help = tk.Label(
    content,
    text="Choose how rows containing missing data should be handled.",
    font=("Segoe UI", 9),
    bg="#ffffff",
    fg="#6b7280"
)

missing_help.pack(
    anchor="w",
    pady=(2, 7)
)


remove_radio = ttk.Radiobutton(
    content,
    text="Remove rows with missing values",
    variable=missing_option,
    value="remove"
)

remove_radio.pack(
    anchor="w",
    pady=(0, 4)
)


keep_radio = ttk.Radiobutton(
    content,
    text="Keep rows with missing values",
    variable=missing_option,
    value="keep"
)

keep_radio.pack(
    anchor="w"
)


# --------------------------------------------------
# Clean button
# --------------------------------------------------

clean_button = ttk.Button(
    content,
    text="Clean CSV Files",
    style="Primary.TButton",
    command=clean_files
)

clean_button.pack(
    fill="x",
    pady=(25, 0)
)


# --------------------------------------------------
# Start GUI
# --------------------------------------------------

root.mainloop()