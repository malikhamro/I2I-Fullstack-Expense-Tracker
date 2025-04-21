# File: dashboard/ui_elements.py

import tkinter as tk
from tkinter import ttk
import logging


logging.basicConfig(level=logging.INFO)


def setup_ui_elements():
    """
    Sets up various UI elements required for the dashboard such as buttons, progress bars, and status displays.
    """
    try:
        root = tk.Tk()
        root.title("Migration Dashboard")
        
        # Configure the grid layout
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Frame for Progress Bar
        progress_frame = ttk.Frame(root, padding="10")
        progress_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Progress Bar
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(progress_frame, length=200, variable=progress_var, maximum=100.0)
        progress_bar.grid(row=0, column=0, columnspan=3, pady=5)

        # Buttons
        start_button = ttk.Button(progress_frame, text="Start Migration", command=lambda: logging.info("Migration Started"))
        start_button.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        pause_button = ttk.Button(progress_frame, text="Pause Migration", command=lambda: logging.info("Migration Paused"))
        pause_button.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        stop_button = ttk.Button(progress_frame, text="Stop Migration", command=lambda: logging.info("Migration Stopped"))
        stop_button.grid(row=1, column=2, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Status Display
        status_label = ttk.Label(progress_frame, text="Status: Waiting to start...")
        status_label.grid(row=2, column=0, columnspan=3, pady=5)

        # Return root widget for further manipulation if needed
        return root

    except Exception as e:
        logging.error(f"An error occurred while setting up UI elements: {e}")
        raise


# Example usage
if __name__ == "__main__":
    dashboard_root = setup_ui_elements()
    dashboard_root.mainloop()
