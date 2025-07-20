# --- START OF FILE main.py ---

from datetime import datetime
from manager import PatientManager

def display_menu():
    """Displays the main menu to the user."""
    print("\n\n=== HOSPITAL PATIENT MANAGER ===")
    print(" 1. Add Patient         2. View All Patients")
    print(" 3. Search Patient      4. Search by Condition")
    print(" 5. Update Patient      6. Discharge Patient")
    print(" 7. Delete Patient      8. View Statistics")
    print(" 9. Bed Availability   10. Export Data to CSV")
    print(" 0. Exit")
    print("==============================")

def display_patient(patient):
    """Prints patient details to the console."""
    if isinstance(patient, list):
        if not patient:
            print("No patients found.")
            return
        print("\n--- Patient List ---")
        for p in patient:
            print(p)
        print("--------------------")
    elif patient:
        print("\n--- Patient Details ---")
        print(patient)
        if patient.discharged_date:
            print(f"Final Bill: {patient.calculate_bill()}")
        print("-----------------------")
    else:
        print("No patient found with the given term.")

# --- Input Validation Helpers ---

def get_valid_string(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")

def get_valid_int(prompt, min_val=0, max_val=130):
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return str(value)
            print(f"Age must be between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_valid_gender(prompt):
    while True:
        value = input(prompt).upper()
        if value in ['M', 'F', 'O']:
            return value
        print("Invalid input. Please enter M, F, or O.")

def get_valid_date(prompt):
    while True:
        date_str = input(prompt)
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

# --- Main Application Logic ---

def main():
    manager = PatientManager()

    while True:
        display_menu()
        choice = input("\nEnter choice (0-10): ")

        if choice == "1": # Add Patient
            print("\n--- Add New Patient ---")
            patient = manager.create_patient(
                name=get_valid_string("Name: "),
                age=get_valid_int("Age: "),
                gender=get_valid_gender("Gender (M/F/O): "),
                condition=get_valid_string("Condition: "),
                admitted_date=get_valid_date("Admitted Date (YYYY-MM-DD): ")
            )
            print(f"\nSuccess! Patient '{patient.name}' added with ID: {patient.patient_id}")

        elif choice == "2": # View All Patients
            patients = manager.list_patients()
            display_patient(patients)

        elif choice == "3": # Search Patient
            term = get_valid_string("Enter Patient ID or Name to search: ")
            # Check if the term is likely an ID (all digits)
            if term.isdigit():
                patient = manager.search_patient_by_id(term)
                display_patient(patient)
            else:
                patients = manager.search_patients_by_name(term)
                display_patient(patients)


        elif choice == "4": # Search by Condition
            condition = get_valid_string("Enter condition to search for: ")
            patients = manager.search_by_condition(condition)
            display_patient(patients)

        elif choice == "5": # Update Patient
            patient_id = get_valid_string("Enter the ID of the patient to update: ")
            patient = manager.search_patient_by_id(patient_id)
            if not patient:
                print("Patient not found.")
            else:
                print(f"\n--- Updating Patient: {patient.name} ({patient.patient_id}) ---")
                print("(Press Enter to keep current value)")

                updates = {}
                # Get new values, only add to updates if user provides input
                if new_name := input(f"New name (current: {patient.name}): ").strip():
                    updates['name'] = new_name
                if new_age_str := input(f"New age (current: {patient.age}): ").strip():
                    try:
                        # Validate that the input is a valid integer in the correct range
                        age = int(new_age_str)
                        if 0 <= age <= 130:
                            updates['age'] = str(age)
                        else:
                            print("Invalid age. Age not updated.")
                    except ValueError:
                        print("Invalid input for age. Age not updated.")

                if new_gender := input(f"New gender (current: {patient.gender}): ").strip().upper():
                    if new_gender in ['M', 'F', 'O']:
                         updates['gender'] = new_gender
                    else:
                        print("Invalid gender. Gender not updated.")

                if new_condition := input(f"New condition (current: {patient.condition}): ").strip():
                    updates['condition'] = new_condition

                if updates:
                    if manager.update_patient(patient_id, updates):
                        print("\nPatient details updated successfully!")
                else:
                    print("\nNo changes were made.")

        elif choice == "6": # Discharge Patient
            patient_id = get_valid_string("Enter Patient ID to discharge: ")
            discharge_date = get_valid_date("Enter Discharge Date (YYYY-MM-DD): ")

            if manager.discharge_patient(patient_id, discharge_date):
                print("Patient discharged successfully!")
                discharged_patient = manager.search_patient_by_id(patient_id)
                display_patient(discharged_patient)
            else:
                print("Failed to discharge patient. They may not exist or are already discharged.")

        elif choice == "7": # Delete Patient
            patient_id = get_valid_string("Enter Patient ID to DELETE: ")
            patient = manager.search_patient_by_id(patient_id)
            if not patient:
                print("Patient not found.")
            else:
                confirm = input(f"Are you sure you want to PERMANENTLY DELETE {patient.name} ({patient.patient_id})? (y/n): ").lower()
                if confirm == 'y':
                    if manager.delete_patient(patient_id):
                        print("Patient record deleted successfully.")
                    else:
                        print("Error: Could not delete patient.")
                else:
                    print("Deletion cancelled.")

        elif choice == "8": # Statistics
            stats = manager.get_statistics()
            print("\n--- HOSPITAL STATISTICS ---")
            print(f"Total Patients (All Time): {stats['total_patients']}")
            print(f"Active (Admitted) Patients: {stats['active_patients']}")
            print(f"Average Length of Stay: {stats['average_stay_days']:.2f} days")
            print("\nGender Distribution:")
            print(f"  - Male: {stats['male_patients']}, Female: {stats['female_patients']}, Other: {stats['other_gender']}")
            print("\nAge Groups:")
            for group, count in stats['age_groups'].items():
                print(f"  - {group}: {count}")
            print("\nTop 3 Most Common Conditions:")
            if stats['top_conditions']:
                for i, (condition, count) in enumerate(stats['top_conditions']):
                    print(f"  {i+1}. {condition} ({count} cases)")
            else:
                print("  - Not enough data.")
            print("---------------------------")

        elif choice == "9": # Bed Availability
            print(f"\nBed Status: {manager.bed_availability()}")

        elif choice == "10": # Export Data
            filename = input("Enter filename for the CSV export (e.g., patients_export.csv): ").strip()
            if not filename:
                filename = "patients_export.csv" # Default filename
            if not filename.lower().endswith('.csv'):
                filename += '.csv'
            print(f"\n{manager.export_data(filename)}")

        elif choice == "0": # Exit
            print("Exiting system. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 0 and 10.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()