# --- START OF FILE models.py ---

from datetime import datetime

class Patient:
    def __init__(self, patient_id, name, age, gender, condition, admitted_date, discharged_date=None):
        self.patient_id = patient_id
        self.name = name
        self.age = str(age) # Ensure age is stored as a string
        self.gender = gender
        self.condition = condition

        # Convert string dates to date objects on creation
        self.admitted_date = datetime.strptime(admitted_date, "%Y-%m-%d").date() if isinstance(admitted_date, str) else admitted_date
        self.discharged_date = datetime.strptime(discharged_date, "%Y-%m-%d").date() if isinstance(discharged_date, str) else discharged_date

    def __str__(self):
        status = f"Discharged on {self.discharged_date}" if self.discharged_date else "Status: Admitted"
        return f"ID: {self.patient_id} | Name: {self.name:<20} | Gender: {self.gender} | Age: {self.age:<3} | Condition: {self.condition:<20} | {status}"

    def to_dict(self):
        """Converts the Patient object to a dictionary for JSON serialization."""
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "condition": self.condition,
            "admitted_date": self.admitted_date.strftime("%Y-%m-%d") if self.admitted_date else None,
            "discharged_date": self.discharged_date.strftime("%Y-%m-%d") if self.discharged_date else None
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Patient instance from a dictionary (e.g., loaded from JSON)."""
        return cls(
            patient_id=data['patient_id'],
            name=data['name'],
            age=data['age'],
            gender=data['gender'],
            condition=data['condition'],
            admitted_date=data['admitted_date'],
            discharged_date=data.get('discharged_date')
        )

    def calculate_bill(self, daily_rate=150):
        """Calculates the hospitalization bill based on days admitted."""
        if not self.discharged_date or not self.admitted_date:
            return "Cannot calculate bill, patient not yet discharged."

        # Ensure days are at least 1 for billing purposes
        days = max(1, (self.discharged_date - self.admitted_date).days)
        total_cost = days * daily_rate
        return f"${total_cost} ({days} days at ${daily_rate}/day)"