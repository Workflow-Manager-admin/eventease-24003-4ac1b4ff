import datetime
from typing import List, Dict, Optional

# Simple in-memory storage for demonstration (replace with DB in production)
_events = []
_registrations = []
_event_id_counter = 1
_registration_id_counter = 1


class Event:
    """A class representing an event."""
    def __init__(self, title: str, date: str, location: str, description: str,
                 schedule: str, organizer: str):
        global _event_id_counter
        self.id = _event_id_counter
        _event_id_counter += 1
        self.title = title
        self.date = date
        self.location = location
        self.description = description
        self.schedule = schedule
        self.organizer = organizer

    # PUBLIC_INTERFACE
    def as_dict(self) -> Dict:
        """Dictionary representation of an event."""
        return {
            "id": self.id,
            "title": self.title,
            "date": self.date,
            "location": self.location,
            "description": self.description,
            "schedule": self.schedule,
            "organizer": self.organizer
        }


class Registration:
    """A class representing a user registration for an event."""
    def __init__(self, event_id: int, name: str, email: str):
        global _registration_id_counter
        self.id = _registration_id_counter
        _registration_id_counter += 1
        self.event_id = event_id
        self.name = name
        self.email = email
        self.registered_at = datetime.datetime.utcnow().isoformat()

    # PUBLIC_INTERFACE
    def as_dict(self) -> Dict:
        """Dictionary representation of a registration."""
        return {
            "id": self.id,
            "event_id": self.event_id,
            "name": self.name,
            "email": self.email,
            "registered_at": self.registered_at
        }


# PUBLIC_INTERFACE
def seed_events():
    """Populates sample events for demonstration if not already seeded."""
    if not _events:
        e1 = Event(
            "Python Bootcamp",
            "2024-08-15",
            "NYC Auditorium",
            "A hands-on Python programming bootcamp for all levels.",
            "09:00 AM - 05:00 PM",
            "Alice Johnson"
        )
        e2 = Event(
            "React Summit",
            "2024-09-10",
            "San Francisco Convention Center",
            "Annual React conference with top speakers and workshops.",
            "10:00 AM - 06:00 PM",
            "Bob Smith"
        )
        _events.extend([e1, e2])


# PUBLIC_INTERFACE
def get_all_events() -> List[Event]:
    """Returns all events."""
    return list(_events)


# PUBLIC_INTERFACE
def get_event_by_id(event_id: int) -> Optional[Event]:
    """Returns a single event by ID."""
    return next((e for e in _events if e.id == event_id), None)


# PUBLIC_INTERFACE
def register_user(event_id: int, name: str, email: str) -> Registration:
    """Registers a user for event and returns the registration object."""
    reg = Registration(event_id, name, email)
    _registrations.append(reg)
    return reg


# PUBLIC_INTERFACE
def get_registrations_for_event(event_id: int) -> List[Registration]:
    """Gets all registrations for a particular event."""
    return [r for r in _registrations if r.event_id == event_id]


# PUBLIC_INTERFACE
def remove_registration(registration_id: int) -> bool:
    """Removes a registration by registration ID (organizer feature)."""
    global _registrations
    initial_len = len(_registrations)
    _registrations = [r for r in _registrations if r.id != registration_id]
    return len(_registrations) < initial_len
