from enum import Enum

class AppointmentStatus(Enum):
  PENDING = "pending"
  CONFIRMED = "confirmed"
  CANCELLED = "cancelled"
  COMPLETED = "completed"

class Appointment:
  id: str
  customer_id: str
  date: str
  time: str
  status: AppointmentStatus
  
  def __init__(self, id: str, customer_id: str, date: str, time: str, status: AppointmentStatus):
    self.id = id
    self.customer_id = customer_id
    self.date = date
    self.time = time
    self.status = status
    
  def to_json(self):
    return {
      "id": self.id,
      "customer_id": self.customer_id,
      "date": self.date,
      "time": self.time,
      "status": self.status.value
    }

class Provider:
  appointments: list[Appointment] = []
  
  def __init__(self):
    self.appointments = []
    
  def add_appointment(self, appointment: Appointment):
    self.appointments.append(appointment)
    
    
  def get_appointments(self, customer_id: str):
    return [appointment.to_json() for appointment in self.appointments if appointment.customer_id == customer_id]
    
  def get_appointment(self, appointment_id: str):
    appointment = next((appointment for appointment in self.appointments if appointment.id == appointment_id), None)
    return appointment if appointment else None
    
  def update_appointment(self, appointment_id: str, status: AppointmentStatus):
    appointment = self.get_appointment(appointment_id)
    if appointment:
      appointment.status = status

# Initialize the provider store
providerStore = Provider()

# Add mock appointments with realistic scenarios
appointments = [
    # Special customer CUST-1000 appointments
    Appointment("APT-2024-000", "CUST-1000", "2024-03-19", "09:00", AppointmentStatus.CONFIRMED),
    Appointment("APT-2024-011", "CUST-1000", "2024-03-25", "14:00", AppointmentStatus.PENDING),
    
    # Regular checkup appointments
    Appointment("APT-2024-001", "CUST-1001", "2024-03-20", "09:00", AppointmentStatus.CONFIRMED),
    Appointment("APT-2024-002", "CUST-1002", "2024-03-20", "10:30", AppointmentStatus.CONFIRMED),
    Appointment("APT-2024-003", "CUST-1003", "2024-03-20", "14:00", AppointmentStatus.PENDING),
    
    # Follow-up appointments
    Appointment("APT-2024-004", "CUST-1001", "2024-03-25", "11:00", AppointmentStatus.PENDING),
    Appointment("APT-2024-005", "CUST-1004", "2024-03-21", "15:30", AppointmentStatus.CONFIRMED),
    
    # Cancelled appointments
    Appointment("APT-2024-006", "CUST-1005", "2024-03-22", "09:30", AppointmentStatus.CANCELLED),
    Appointment("APT-2024-007", "CUST-1002", "2024-03-23", "13:00", AppointmentStatus.CANCELLED),
    
    # Future appointments
    Appointment("APT-2024-008", "CUST-1006", "2024-03-26", "10:00", AppointmentStatus.PENDING),
    Appointment("APT-2024-009", "CUST-1007", "2024-03-27", "14:30", AppointmentStatus.PENDING),
    Appointment("APT-2024-010", "CUST-1003", "2024-03-28", "11:30", AppointmentStatus.PENDING)
]

# Add all appointments to the provider store
for appointment in appointments:
    providerStore.add_appointment(appointment)

# Function to get the provider store
def get_provider_store():
    return providerStore
    
