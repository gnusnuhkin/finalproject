import tkinter as tk
from logic import GradeCalculator
from gui import GradeApp
def main() -> None:
    root = tk.Tk()
    root.title("Grade Helper App")
    calculator = GradeCalculator()
    app = GradeApp(root,calculator)
    root.mainloop()

if __name__ == "__main__":
    main()
