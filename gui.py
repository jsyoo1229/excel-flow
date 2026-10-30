import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

from main import clean_csv_files


def select_folder():
    folder = filedialog.askdirectory(
        title="Select CSV Folder"
    )

    if folder:
        folder_path.set(folder)

        # Automatically suggest an output file
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
        return


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


# Create the main window
root = tk.Tk()

root.title("Excel Flow")
root.geometry("620x390")
root.resizable(False, False)


# GUI variables
folder_path = tk.StringVar()
output_path = tk.StringVar()

missing_option = tk.StringVar(
    value="remove"
)


# Title
title_label = tk.Label(
    root,
    text="Excel Flow",
    font=("Arial", 22, "bold")
)

title_label.pack(
    pady=(25, 20)
)


# Input folder section
input_label = tk.Label(
    root,
    text="Input folder"
)

input_label.pack()


input_frame = tk.Frame(root)

input_frame.pack(
    pady=(5, 15)
)


folder_entry = tk.Entry(
    input_frame,
    textvariable=folder_path,
    width=55
)

folder_entry.pack(
    side="left",
    padx=(0, 8)
)


browse_button = tk.Button(
    input_frame,
    text="Browse",
    width=10,
    command=select_folder
)

browse_button.pack(
    side="left"
)


# Output file section
output_label = tk.Label(
    root,
    text="Output file"
)

output_label.pack()


output_frame = tk.Frame(root)

output_frame.pack(
    pady=(5, 15)
)


output_entry = tk.Entry(
    output_frame,
    textvariable=output_path,
    width=55
)

output_entry.pack(
    side="left",
    padx=(0, 8)
)


output_button = tk.Button(
    output_frame,
    text="Save As",
    width=10,
    command=select_output_file
)

output_button.pack(
    side="left"
)


# Missing value options
missing_label = tk.Label(
    root,
    text="Missing values"
)

missing_label.pack(
    pady=(5, 5)
)


remove_radio = tk.Radiobutton(
    root,
    text="Remove rows with missing values",
    variable=missing_option,
    value="remove"
)

remove_radio.pack()


keep_radio = tk.Radiobutton(
    root,
    text="Keep rows with missing values",
    variable=missing_option,
    value="keep"
)

keep_radio.pack()


# Clean button
clean_button = tk.Button(
    root,
    text="Clean Files",
    width=25,
    height=2,
    command=clean_files
)

clean_button.pack(
    pady=25
)


# Start the GUI
root.mainloop()