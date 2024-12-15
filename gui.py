import tkinter as tk
from tkinter import messagebox
from typing import List
from logic import GradeCalculator


class GradeApp:
    """
    The GUI for Grade Helper App. Has frames for the main menu,
    individual grader, class grader, and ending screen.
    """

    def __init__(self, root: tk.Tk, calculator: GradeCalculator) -> None:
        """
        Starts at the main menu.
        """
        self.root = root
        self.calculator = calculator
        self.frames = {}
        self.create_main_menu()
        self.create_individual_grader()
        self.create_class_grader()
        self.create_completion_frame()
        self.frames["main_menu"].tkraise()

    def create_main_menu(self) -> None:
        """
        Creates the main menu frame with buttons to go to Individual or Class grader.
        """
        frame = tk.Frame(self.root)
        self.frames["main_menu"] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(frame, text="Grade Averager").pack()
        tk.Button(frame, text="Individual Student Grader", command=self.show_individual_grader).pack()
        tk.Button(frame, text="Class Grader", command=self.show_class_grader).pack()
    def create_individual_grader(self) -> None:
        """
        Frame for individual student Grader:
        """
        frame = tk.Frame(self.root)
        self.frames["individual_grader"] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(frame, text="Individual Student Grader").pack()

        # Enter Student Name
        self.ind_student_name_var = tk.StringVar()
        tk.Label(frame, text="Enter Student Name (No Spaces):").pack()
        self.ind_student_name_entry = tk.Entry(frame, textvariable=self.ind_student_name_var)
        self.ind_student_name_entry.pack()
        self.ind_student_name_button = tk.Button(frame, text="Enter", command=self.individual_name_entered)
        self.ind_student_name_button.pack()
        # Enter Number of Tests (Should popup after name is entered)
        self.ind_test_count_var = tk.StringVar()
        self.ind_test_count_label = tk.Label(frame, text="Number of Tests:")
        self.ind_test_count_label.pack_forget()
        self.ind_test_count_entry = tk.Entry(frame, textvariable=self.ind_test_count_var)
        self.ind_test_count_entry.pack_forget()
        self.ind_test_count_button = tk.Button(frame, text="Enter", command=self.generate_individual_inputs)
        self.ind_test_count_button.pack_forget()
        # Dynamic scores frame
        self.ind_scores_frame = tk.Frame(frame)
        self.ind_scores_frame.pack()
        # Calculate and Save
        self.ind_save_button = tk.Button(frame, text="Save", command=self.save_individual_data)
        self.ind_save_button.pack_forget()
        # Clear and Main Menu
        tk.Button(frame, text="Clear", command=self.clear_individual_inputs).pack()
        tk.Button(frame, text="Main Menu", command=self.restart_app).pack()
    def create_class_grader(self) -> None:
        """
        Frame for Class Grader
        """
        frame = tk.Frame(self.root)
        self.frames["class_grader"] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(frame, text="Class Grader").pack()

        self.class_name_var = tk.StringVar()
        tk.Label(frame, text="Enter Class Name (No Spaces):").pack()
        self.class_name_entry = tk.Entry(frame, textvariable=self.class_name_var)
        self.class_name_entry.pack()
        self.class_name_button = tk.Button(frame, text="Enter", command=self.class_name_entered)
        self.class_name_button.pack()
        self.student_count_var = tk.StringVar()
        self.student_count_label = tk.Label(frame, text="Number of Students:")
        self.student_count_label.pack_forget()
        self.student_count_entry = tk.Entry(frame, textvariable=self.student_count_var)
        self.student_count_entry.pack_forget()
        self.student_count_button = tk.Button(frame, text="Enter", command=self.generate_class_inputs)
        self.student_count_button.pack_forget()

        # Scroll feature
        container = tk.Frame(frame)
        container.pack(expand=True, fill=tk.BOTH)
        self.canvas = tk.Canvas(container, width=50, height=200)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(container, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.students_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.students_frame, anchor="nw")
        self.students_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.class_save_button = tk.Button(frame, text="Save", command=self.save_class_data)
        self.class_save_button.pack_forget()
        tk.Button(frame, text="Clear", command=self.clear_class_inputs).pack()
        tk.Button(frame, text="Main Menu", command=self.restart_app).pack()

    def create_completion_frame(self) -> None:
        """
        Frame that appears after saving for either grader.
        """
        frame = tk.Frame(self.root)
        self.frames["completion"] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(frame, text="You're all set!").pack()
        tk.Button(frame, text="Restart", command=self.restart_app).pack()
        tk.Button(frame, text="Exit", command=self.root.quit).pack()

    # INDIVIDUAL GRADER
    def individual_name_entered(self) -> None:
        """
        Validates unique name. Hides the name button and shows number of tests input.
        """
        name = self.ind_student_name_var.get().strip()
        if not self.calculator.validate_name(name):
            messagebox.showerror("Invalid Name", "Student name must be letters only(No spaces).")
            return
        success = self.calculator.add_class(name)
        if not success:
            messagebox.showerror("Duplicate", f"A record for '{name}' already exists.")
            return

        self.ind_student_name_button.pack_forget()
        self.ind_test_count_label.pack()
        self.ind_test_count_entry.pack()
        self.ind_test_count_button.pack()

    def generate_individual_inputs(self) -> None:
        """
        Reads the integer number of tests, reveals dynamic score inputs, hides the test count fields.
        """
        test_str = self.ind_test_count_var.get().strip()
        if not test_str.isdigit():
            messagebox.showerror("Invalid Input", "Number of tests must be a number(No floats)")
            return
        attempts = int(test_str)
        if attempts < 1:
            messagebox.showerror("Invalid Input", "Number of tests must be more than 0.")
            return
        self.ind_test_count_label.pack_forget()
        self.ind_test_count_entry.pack_forget()
        self.ind_test_count_button.pack_forget()
        for widget in self.ind_scores_frame.winfo_children():
            widget.destroy()
        self.ind_score_vars = []
        for i in range(attempts):
            var = tk.StringVar()
            tk.Label(self.ind_scores_frame, text=f"Score {i+1}:").pack()
            tk.Entry(self.ind_scores_frame, textvariable=var).pack()
            self.ind_score_vars.append(var)
        self.ind_save_button.pack()

    def save_individual_data(self) -> None:
        """
        Saves the single student's data into csv. Validates integer-only scores between 1-100.
        """
        name = self.ind_student_name_var.get().strip()
        scores = []

        for var in self.ind_score_vars:
            s = var.get().strip()
            if not s.isdigit():
                messagebox.showerror("Invalid Score", "Scores must be integers(No Floats).")
                return
            val = int(s)
            scores.append(val)
        if not self.calculator.validate_scores(scores):
            messagebox.showerror("Invalid Score", "Scores must be between 0 and 100.")
            return
        success = self.calculator.add_student(name, name, scores)
        if not success:
            messagebox.showerror("Duplicate Student", f"Student '{name}' already exists.")
            return
        self.calculator.save_individual_csv(name, scores)
        self.frames["completion"].tkraise()

    def clear_individual_inputs(self) -> None:
        """
        Resets the individual grader boxes.
        """
        self.ind_student_name_var.set("")
        self.ind_test_count_var.set("")
        for widget in self.ind_scores_frame.winfo_children():
            widget.destroy()
        # Re-show the name button
        self.ind_student_name_button.pack()
        # Hide the other boxes
        self.ind_test_count_label.pack_forget()
        self.ind_test_count_entry.pack_forget()
        self.ind_test_count_button.pack_forget()
        self.ind_save_button.pack_forget()

    #CLASS GRADER
    def class_name_entered(self) -> None:
        """
        Validates unique class name, hides the name button, shows number of students input.
        """
        class_name = self.class_name_var.get().strip()
        if not self.calculator.validate_name(class_name):
            messagebox.showerror("Invalid Class Name", "Make sure it is letters only (No spaces)")
            return
        success = self.calculator.add_class(class_name)
        if not success:
            messagebox.showerror("Duplicate Class", f"Class '{class_name}' already exists.")
            return
        self.class_name_button.pack_forget()
        self.student_count_label.pack()
        self.student_count_entry.pack()
        self.student_count_button.pack()

    def generate_class_inputs(self) -> None:
        """
        Reads the integer number of students, reveals dynamic name and score entries,and hides the student count boxes.
        """
        stud_count_str = self.student_count_var.get().strip()
        if not stud_count_str.isdigit():
            messagebox.showerror("Invalid Input", "Number of students must be an integer(No floats)")
            return
        count = int(stud_count_str)
        if count < 1:
            messagebox.showerror("Invalid Input", "Number of students must be more than 1.")
            return
        self.student_count_label.pack_forget()
        self.student_count_entry.pack_forget()
        self.student_count_button.pack_forget()

        for widget in self.students_frame.winfo_children():
            widget.destroy()
        self.class_entries = []
        for i in range(count):
            frame = tk.Frame(self.students_frame)
            frame.pack()
            tk.Label(frame, text=f"Student {i+1} Name:").pack()
            name_var = tk.StringVar()
            tk.Entry(frame, textvariable=name_var).pack()
            tk.Label(frame, text=f"Student {i+1} Score:").pack()
            score_var = tk.StringVar()
            tk.Entry(frame, textvariable=score_var).pack()
            self.class_entries.append((name_var, score_var))
        self.class_save_button.pack()

    def save_class_data(self) -> None:
        """
        Saves the entire class to csv. Ensures no duplicate student names.
        """
        class_name = self.class_name_var.get().strip()
        if class_name in self.calculator.classes:
            self.calculator.classes[class_name].clear()
        used_names = set()
        for name_var, score_var in self.class_entries:
            n_str = name_var.get().strip()
            if not n_str.isalpha():
                messagebox.showerror("Invalid Name", f"'{n_str}' must be letters only(No spaces)")
                return
            if n_str in used_names:
                messagebox.showerror("Duplicate Student", f"'{n_str}' duplicated in class '{class_name}'.")
                return
            used_names.add(n_str)
            s_str = score_var.get().strip()
            if not s_str.isdigit():
                messagebox.showerror("Invalid Score", f"'{s_str}' is not an integer.")
                return
            val = int(s_str)
            if not self.calculator.validate_scores([val]):
                messagebox.showerror("Invalid Score Range", f"Score '{s_str}' must be between 0 to 100.")
                return
            success = self.calculator.add_student(class_name, n_str, [val])
            if not success:
                messagebox.showerror("Duplicate Student", f"Student '{n_str}' already exists in class '{class_name}'.")
                return
        self.calculator.save_class_csv(class_name)
        self.frames["completion"].tkraise()

    def clear_class_inputs(self) -> None:
        """
        Clears the class grader boxes.
        """
        self.class_name_var.set("")
        self.student_count_var.set("")
        for widget in self.students_frame.winfo_children():
            widget.destroy()
        self.class_name_button.pack()
        self.class_save_button.pack_forget()
        self.student_count_label.pack_forget()
        self.student_count_entry.pack_forget()
        self.student_count_button.pack_forget()

    # MAIN MENU
    def restart_app(self) -> None:
        """
        Returns to main menu and clear all input boxes.
        """
        self.clear_individual_inputs()
        self.clear_class_inputs()
        self.frames["main_menu"].tkraise()
    def show_individual_grader(self) -> None:
        self.restart_app()
        self.frames["individual_grader"].tkraise()

    def show_class_grader(self) -> None:
        self.restart_app()
        self.frames["class_grader"].tkraise()