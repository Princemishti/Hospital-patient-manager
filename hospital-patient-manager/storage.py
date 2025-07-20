# --- START OF FILE storage.py ---

import json
import csv
from datetime import datetime
from models import Patient

class PatientStorage:
    def __init__(self, filename="patients.json"):
        self.filename = filename

    def save_patients(self, patients):
        """Saves the list of patient objects to the JSON file."""
        with open(self.filename, 'w') as f:
            json.dump([p.to_dict() for p in patients], f, indent=4)

    def load_patients(self):
        """Loads patients from the JSON file, creating Patient objects."""
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return [Patient.from_dict(p_data) for p_data in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return [] # Return an empty list if file doesn't exist or is empty/corrupt

    def export_csv(self, patients, filename="patients.csv"):
        """
        Export data to CSV using the csv module for safety.
        Accepts a list of patients to avoid re-reading from disk.
        """
        try:
            with open(filename, 'w', newline='') as f: # newline='' is important for csv
                writer = csv.writer(f)

                # Write the header row
                writer.writerow(["ID", "Name", "Age", "Gender", "Condition", "Admitted", "Discharged", "Status"])

                # Write data for each patient
                for p in patients:
                    status = "Discharged" if p.discharged_date else "Admitted"
                    writer.writerow([
                        p.patient_id,
                        p.name,
                        p.age,
                        p.gender,
                        p.condition,
                        p.admitted_date,
                        p.discharged_date or "N/A", # Use "N/A" for None
                        status
                    ])
            return True
        except IOError:
            return False