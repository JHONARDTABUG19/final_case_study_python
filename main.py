import array_operations
import analytics
import reports
import os
from termcolor import colored, cprint

# CSV file name and headers
FILENAME = "studentRecord.csv"
HEADER = [
    "student_id", "last_name", "first_name", "section",
    "quiz1", "quiz2", "quiz3", "quiz4", "quiz5",
    "midterm", "final", "attendance_percent"]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu():
    # Load CSV at program start
    valid_rows, bad_rows = array_operations.clean_ingest(FILENAME, HEADER)
    existing_records = valid_rows.copy()  # In-memory copy of valid records
    
    clear_screen()
    while True:
       
        cprint("\n=== STUDENT CSV MENU ===", "yellow",attrs=["bold"])
        cprint("1. Add Student and directly saved in CSV file", "green")
        cprint("2. Read CSV File", "green")
        cprint("3. Delete Student by ID", "green")
        cprint("4. Select Header Column", "green")
        cprint("5. Project Student Record by Student ID", "green")
        cprint("6. Sort Student Data", "green")
        cprint("7. MENU of Analytics and Reports", "blue")
        cprint("8. Choose to display Section Record", "green")
        cprint("9. Exit", "red")


        choice = input("Enter choice: ").strip()


        if choice == "1":
            # Add students and update in-memory list
            existing_records = array_operations.add_data(existing_records)


        elif choice == "2":
            # Reload from file in case of external changes
            existing_records, bad_rows = array_operations.clean_ingest(FILENAME, HEADER)
            if existing_records:
                print("\n📘 Valid rows:")
                for row in existing_records:
                    print(row)


        elif choice == "3":
            array_operations.delete_data(FILENAME)
            # Reload after deletion
            existing_records, bad_rows = array_operations.clean_ingest(FILENAME, HEADER)


        elif choice == "4":
            array_operations.select_column(FILENAME)


        elif choice == "5":
            array_operations.select_row(FILENAME)


        elif choice == "6":
            array_operations.sort_data(FILENAME)
            # Reload after sorting
            existing_records, bad_rows = array_operations.clean_ingest(FILENAME, HEADER)


        elif choice == "7":
            while True:
                cprint("\n=== ANALYTICS AND REPORTS MENU ===", "yellow", attrs=["bold"])
                cprint("a. Compute Weighted Grades", "green")
                cprint("b. Grade Distribution (A–F)", "green")
                cprint("c. Percentiles (Top/Bottom 10%)", "green")
                cprint("d. Outliers (±1.5 SD)", "green")
                cprint("e. Improvement (Final vs Midterm)", "green")
                cprint("f. Summary Reports", "green")
                cprint("g. Display at-risk Students (at_risk_students.csv)", "green")
                cprint("h. Back to Main Menu", "blue")


                sub = input("Select an option (a–h): ").lower().strip()
                if sub == "a":
                    analytics.compute_grades()
                elif sub == "b":
                    analytics.grade_distribution()
                elif sub == "c":
                    analytics.percentiles()
                elif sub == "d":
                    analytics.outliers()
                elif sub == "e":
                    analytics.improvement()
                elif sub == "f":
                    reports.summary_report()
                elif sub == "g":
                    reports.export_at_risk()
                elif sub == "h":
                    break
                else:
                    print("Invalid choice. Try again.", "red")


        elif choice == "8":
            # Show available sections first
            try:
                import csv
                sections = set()
                with open(reports.FILENAME, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        sec = row.get("section", "").strip()
                        if sec:
                            sections.add(sec)
                if sections:
                    cprint("\nAvailable Sections:", "green")
                    print(", ".join(sorted(sections)))
                else:
                    cprint("\nNo sections found in the records.", "red")
            except FileNotFoundError:
                cprint("\nNo data file found. Please add student records first.", "red")
                return
            except Exception as e:
                cprint("\nCould not read sections:", e)
                return


            # Ask for section input
            section = input("\nEnter section name: ").strip()


            # Display section data once
            reports.display_section_simple(section)


            # Silently generate section CSVs in background
            try:
                reports.export_per_section(reports.FILENAME, out_folder=reports.OUT_DIR)
            except Exception:
                try:
                    reports.summary_report(
                        filename=reports.FILENAME,
                        export_sections=True,
                        out_folder=reports.OUT_DIR
                    )
                except Exception:
                    pass




        elif choice == "9":
            cprint("Exiting program...", "blue")
            break


        else:
            cprint("Invalid choice. Try again.", "red")




if __name__ == "__main__":
    menu()

