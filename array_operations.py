import csv
import os
import re
from ingest import clean_ingest  # Function to read and validate CSV data

FILENAME = "studentRecord.csv"
HEADER = [
    "student_id",
    "last_name",
    "first_name",
    "section",
    "quiz1",
    "quiz2",
    "quiz3",
    "quiz4",
    "quiz5",
    "midterm",
    "final",
    "attendance_percent"
]

# ---------------------- SAVE FUNCTIONS ----------------------

def save_to_csv(data, filename=FILENAME):
    """Appends new student data to CSV (adds header if file is new)."""
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(HEADER)
        writer.writerows(data)
    print(f"Data saved to {filename}")


def save_cleaned_csv(valid_rows, filename=FILENAME):
    """Overwrites CSV file with cleaned/updated data."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        writer.writerows(valid_rows)
    print(f"Cleaned data saved to {filename}")


# ---------------------- ADD DATA ----------------------

def add_data(existing_records):
    new_rows = []
    while True:
        n_input = input("How many students you need to add? ").strip()
        if n_input == "":
            print("Invalid input. Please enter a number.")
            continue
        try:
            n = int(n_input)
            if n <= 0:
                print("Please enter a number greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            continue
    

    for i in range(n):
        print(f"\n--- Student #{i + 1} ---")
        print("Reminders: Enter '-' if last and first name are none. Enter '0' if scores are none, \n")
        

        student = []

        for idx, field in enumerate(HEADER):
            while True:
                val = input(f"Enter {field}: ").strip()

                # STUDENT ID
                if idx == 0:
                    if val == "":
                        print("Student ID cannot be empty. Try again.")
                        continue
                    if not re.fullmatch(r"[A-Za-z0-9-]+", val):
                        print("Student ID must contain only letters, numbers, or hyphens (e.g., A-123). Try again.")
                        continue
                    existing_ids = [row[0] for row in existing_records]
                    if val in existing_ids:
                        print("This Student ID already exists. Please enter a unique ID.")
                        continue
                    student.append(val)
                    break

                # LAST NAME
                elif idx == 1:
                    if val == "":
                        print("Last name cannot be empty. Try again.")
                        continue
                    if not re.fullmatch(r"[A-Za-z\s-]+", val):
                        print("Last name can only contain letters, spaces, or hyphens. Try again.")
                        continue
                    student.append(val)
                    break

                # FIRST NAME
                elif idx == 2:
                    if val == "":
                        print("First name cannot be empty. Try again.")
                        continue
                    if not re.fullmatch(r"[A-Za-z\s-]+", val):
                        print("First name can only contain letters, spaces, or hyphens. Try again.")
                        continue
                    student.append(val)
                    break

                # SECTION
                elif idx == 3:
                    if val == "":
                        print("Section cannot be empty. Try again.")
                        continue
                    if not re.fullmatch(r"[A-Za-z0-9-]+", val):
                        print("Section must contain only letters, numbers, or hyphens (e.g., A1, B-2). Try again.")
                        continue
                    student.append(val)
                    break

                # SCORES / ATTENDANCE
                else:
                    if val == "":
                        print("Scores cannot be empty. Try again.")
                        continue
                    try:
                        num = float(val)
                        if num < 0 or num > 100:
                            print("Scores must be between 0 and 100.")
                            continue
                        student.append(num)
                        break
                    except ValueError:
                        print("Please enter a valid numeric value.")
                        continue

        new_rows.append(student)

    save_to_csv(new_rows)
    return existing_records + new_rows



# ---------------------- DELETE DATA ----------------------

def delete_data(existing_records):
    student_id = input("Enter Student ID to delete: ")
    updated_rows = [row for row in existing_records if row[0] != student_id]

    if len(updated_rows) == len(existing_records):
        print("No student found with that ID.")
        return existing_records

    save_cleaned_csv(updated_rows)
    print(f"Deleted Student ID: {student_id} successfully.")
    return updated_rows


# ---------------------- SELECT COLUMN ----------------------

def select_column(existing_records):
    if not existing_records:
        print("No valid data.")
        return

    print("\nAvailable columns:")
    for i, col in enumerate(HEADER):
        print(f"{i+1}. {col}")

    col_name = input("Enter column name to view: ").strip()
    if col_name not in HEADER:
        print("Invalid column name.")
        return

    index = HEADER.index(col_name)
    print(f"\nValues under '{col_name}':")
    for row in existing_records:
        print(row[index])


# ---------------------- SELECT ROW ----------------------

def select_row(existing_records):
    if not existing_records:
        print("No valid data.")
        return

    student_id = input("Enter Student ID to view: ")
    for row in existing_records:
        if row[0] == student_id:
            print("\nStudent Information:")
            for h, v in zip(HEADER, row):
                print(f"{h}: {v}")
            return

    print("No student found with that ID.")


# ---------------------- SORT DATA ----------------------

def sort_data(existing_records):
    if not existing_records:
        print("No valid data to sort.")
        return existing_records

    print("\nAvailable columns to sort by:")
    for i, col in enumerate(HEADER):
        print(f"{i+1}. {col}")

    col_name = input("\nEnter column name to sort by: ").strip()
    if col_name not in HEADER:
        print("Invalid column name.")
        return existing_records

    col_index = HEADER.index(col_name)

    print("\nSort order:")
    print("1. Ascending (A→Z, 0→100)")
    print("2. Descending (Z→A, 100→0)")
    order = input("Enter choice (1 or 2): ").strip()
    reverse = True if order == "2" else False

    is_numeric = col_index in range(4, 12)

    def sort_key(row):
        value = row[col_index]
        if is_numeric:
            return float(value) if value is not None else float('-inf')
        else:
            return str(value).lower() if value is not None else ""

    try:
        sorted_rows = sorted(existing_records, key=sort_key, reverse=reverse)
        save_cleaned_csv(sorted_rows)
        print(f"\nData sorted by '{col_name}' ({'descending' if reverse else 'ascending'})")
        return sorted_rows
    except Exception as e:
        print(f"Error during sorting: {e}")
        return existing_records
