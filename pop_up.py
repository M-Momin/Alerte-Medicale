import tkinter as tk

def show_alert():
    alert = tk.Toplevel()
    alert.title("Alerte")
    alert.geometry("200x100")
    alert_label = tk.Label(alert, text="Alerte !", font=("Arial", 20))
    alert_label.pack(pady=20)
    alert.mainloop()
