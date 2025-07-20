# --- START OF FILE manager.py ---

from datetime import datetime
from collections import Counter
from storage import PatientStorage
from models import Patient

class PatientManager:
    def __init__(self, total_beds=50):
        self.storage = PatientStorage()
        self.patients = self.storage.load_patients()
        # Find max integer ID among patients, ignore non-integer IDs
        int_ids = [int(p.patient_id) for p in self.patients if str(p.patient_id).isdigit()]
        self.last_id = max(int_ids) if int_ids else 0
        self.total_beds = total_beds

    def create_patient(self, name, age, gender, condition, admitted_date):
        self.last_id += 1
        patient_id = str(self.last_id).zfill(4)
        patient = Patient(patient_id, name, age, gender, condition, admitted_date)
        self.patients.append(patient)
        self.storage.save_patients(self.patients)
        return patient

    def list_patients(self):
        return sorted(self.patients, key=lambda p: p.patient_id)

    def search_patient_by_id(self, patient_id):
        """Finds a single patient by their unique ID."""
        return next((p for p in self.patients if p.patient_id == patient_id), None)

    def search_patients_by_name(self, name):
        """Finds all patients whose name contains the search term."""
        name_lower = name.lower()
        return [p for p in self.patients if name_lower in p.name.lower()]

    def search_by_condition(self, condition):
        condition_lower = condition.lower()
        return [p for p in self.patients if condition_lower in p.condition.lower()]

    def update_patient(self, patient_id, updates):
        patient = self.search_patient_by_id(patient_id)
        if patient:
            for attr, value in updates.items():
                if value: # Ensure value is not empty
                    setattr(patient, attr, value)
            self.storage.save_patients(self.patients)
            return True
        return False

    def discharge_patient(self, patient_id, discharge_date_str):
        patient = self.search_patient_by_id(patient_id)
        # Check if patient exists and is not already discharged
        if patient and not patient.discharged_date:
            patient.discharged_date = datetime.strptime(discharge_date_str, "%Y-%m-%d").date()
            self.storage.save_patients(self.patients)
            return True
        return False

    def delete_patient(self, patient_id):
        """Delete a patient record by ID."""
        patient = self.search_patient_by_id(patient_id)
        if patient:
            self.patients.remove(patient)
            self.storage.save_patients(self.patients)
            return True
        return False

    def get_statistics(self):
        """Enhanced with more detailed stats."""
        active_patients = [p for p in self.patients if not p.discharged_date]
        discharged_patients = [p for p in self.patients if p.discharged_date]

        # Calculate average stay
        if discharged_patients:
            total_days = sum((p.discharged_date - p.admitted_date).days for p in discharged_patients)
            avg_stay = total_days / len(discharged_patients)
        else:
            avg_stay = 0

        # Find top conditions
        if self.patients:
            condition_counts = Counter(p.condition.strip().title() for p in self.patients)
            top_3_conditions = condition_counts.most_common(3)
        else:
            top_3_conditions = []

        stats = {
            'total_patients': len(self.patients),
            'active_patients': len(active_patients),
            'male_patients': sum(1 for p in self.patients if p.gender == 'M'),
            'female_patients': sum(1 for p in self.patients if p.gender == 'F'),
            'other_gender': sum(1 for p in self.patients if p.gender == 'O'),
            'age_groups': self._get_age_groups(),
            'average_stay_days': avg_stay,
            'top_conditions': top_3_conditions
        }
        return stats

    def _get_age_groups(self):
        groups = {'0-18': 0, '19-35': 0, '36-60': 0, '61+': 0}
        for p in self.patients:
            try:
                age = int(p.age)
                if age <= 18: groups['0-18'] += 1
                elif age <= 35: groups['19-35'] += 1
                elif age <= 60: groups['36-60'] += 1
                else: groups['61+'] += 1
            except (ValueError, TypeError):
                continue
        return groups

    def bed_availability(self):
        used_beds = sum(1 for p in self.patients if not p.discharged_date)
        return f"Available: {self.total_beds - used_beds}/{self.total_beds} beds"

    def export_data(self, filename="patients_export.csv"):
        """Passes the current patient list and a filename to the storage exporter."""
        if self.storage.export_csv(self.patients, filename):
            return f"Data successfully exported to {filename}"
        return f"Error: Could not export data to {filename}"