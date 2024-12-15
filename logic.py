import csv
from typing import List, Dict

class GradeCalculator:
    """
    Stores in a dictionary of classes, each class has a list of student dictionaries containing name and scores. Validates inputs and saves results to CSV files.
    """
    def __init__(self) -> None:
        """
        Sets the classes dictionary.
        """
        self.classes: Dict[str, List[Dict[str, List[int]]]] = {}
    def add_class(self, class_name: str) -> bool:
        """
        Creates a new class record if it doesn't already exist.
        """
        if class_name in self.classes:
            return False
        self.classes[class_name] = []
        return True
    def add_student(self, class_name: str, student_name: str, scores: List[int]) -> bool:
        """
        Adds a student record with scores to an existing class.Ensures no two students in the same class share the same name.
        """
        if class_name not in self.classes:
            return False
        for student in self.classes[class_name]:
            if student["name"] == student_name:
                return False
        self.classes[class_name].append({"name": student_name, "scores": scores})
        return True
    def validate_name(self, name: str) -> bool:
        """
        Checks that the name is valid and not empty.
        """
        name = name.strip()
        if not name:
            return False
        for ch in name:
            if not (('A' <= ch <= 'Z') or ('a' <= ch <= 'z')):
                return False
        return True
    def validate_scores(self, scores: List[int]) -> bool:
        """
        Ensures all scores are in the range from 0 to 100.
        """
        return all(0 <= score <= 100 for score in scores)
    def calculate_scores(self, scores: List[int]) -> Dict[str, float]:
        """
        Calculates the highest, lowest, and average from a list of scores.
        """
        return {
            "highest": max(scores),
            "lowest": min(scores),
            "average": sum(scores) / len(scores) if scores else 0.0
        }
    def save_individual_csv(self, student_name: str, scores: List[int]) -> None:
        """
        Saves student data to a CSV file.
        """
        filename = f"{student_name}_grades.csv"
        stats = self.calculate_scores(scores)
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Highest", "Lowest", "Average"])
            writer.writerow([
                student_name,
                int(stats["highest"]),
                int(stats["lowest"]),
                f"{stats['average']:.2f}"])
            writer.writerow([f"All grades: {', '.join(map(str, scores))}"
            ])
    def save_class_csv(self, class_name: str) -> None:
        """
        Saves a student class to a CSV file.
        """
        if class_name not in self.classes:
            return
        filename = f"{class_name}_grades.csv"
        records = self.classes[class_name]

        all_scores = []
        for record in records:
            all_scores.extend(record["scores"])
        stats = self.calculate_scores(all_scores)
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Class", "Student", "Score"])
            for student in records:
                name = student["name"]
                score = student["scores"][0] if student["scores"] else 0
                writer.writerow([class_name, name, score])
            writer.writerow([f"Highest: {int(stats['highest'])}"])
            writer.writerow([f"Lowest: {int(stats['lowest'])}"])
            writer.writerow([f"Average: {stats['average']:.2f}"])
