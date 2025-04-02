import pandas as pd
import os
import tkinter as tk
from glob import glob
from tkinter import RIDGE, Label, Entry, Button
import csv

def subjectchoose(text_to_speech):
    def calculate_attendance():
        subject = tx.get().strip()
        if not subject:
            text_to_speech("Please enter the subject name.")
            return

        attendance_path = os.path.join("Attendance", subject)
        files = glob(f"{attendance_path}\\{subject}*.csv")

        if not files:
            text_to_speech("No attendance files found.")
            return

        df_list = []
        for file in files:
            try:
                df_list.append(pd.read_csv(file))
            except Exception as e:
                print(f"Error reading {file}: {e}")

        if not df_list:
            text_to_speech("No valid attendance records found.")
            return

        df = pd.concat(df_list, axis=0, join="outer").fillna(0)
        df["Attendance"] = df.iloc[:, 2:].mean(axis=1).mul(100).round().astype(str) + '%'
        df.to_csv(f"{attendance_path}/attendance.csv", index=False)

        root = tk.Tk()
        root.title(f"Attendance of {subject}")
        root.configure(background="black")

        with open(f"{attendance_path}/attendance.csv") as file:
            for r, col in enumerate(csv.reader(file)):
                for c, row in enumerate(col):
                    Label(root, text=row, width=10, height=1, fg="yellow", font=("times", 15, "bold"), bg="black", relief=RIDGE).grid(row=r, column=c)

        root.mainloop()

    subject_win = tk.Tk()
    subject_win.title("Subject Selection")
    subject_win.geometry("580x320")
    subject_win.configure(background="black")

    Label(subject_win, text="Which Subject of Attendance?", bg="black", fg="green", font=("arial", 25)).place(x=100, y=12)
    Label(subject_win, text="Enter Subject", width=10, height=2, bg="black", fg="yellow", bd=5, relief=RIDGE, font=("times new roman", 15)).place(x=50, y=100)

    tx = Entry(subject_win, width=15, bd=5, bg="black", fg="yellow", relief=RIDGE, font=("times", 30, "bold"))
    tx.place(x=190, y=100)

    Button(subject_win, text="View Attendance", command=calculate_attendance, bd=7, font=("times new roman", 15), bg="black", fg="yellow", height=2, width=12, relief=RIDGE).place(x=195, y=170)

    subject_win.mainloop()
