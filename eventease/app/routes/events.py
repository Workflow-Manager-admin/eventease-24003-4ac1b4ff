from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import request
from ..models import (
    seed_events, get_all_events, get_event_by_id,
    register_user, get_registrations_for_event, remove_registration
)

blp = Blueprint("Events", "events", url_prefix="/events", description="Event listing, details, registration, and management routes")

@blp.before_request
def before_request():
    # Ensure sample data exists
    seed_events()

# PUBLIC_INTERFACE
@blp.route("/")
class EventList(MethodView):
    """List all events with basic info."""
    def get(self):
        events = get_all_events()
        return {"events": [e.as_dict() for e in events]}

# PUBLIC_INTERFACE
@blp.route("/<int:event_id>")
class EventDetail(MethodView):
    """Get event details by ID."""
    def get(self, event_id):
        event = get_event_by_id(event_id)
        if not event:
            abort(404, message="Event not found.")
        return event.as_dict()

# PUBLIC_INTERFACE
@blp.route("/<int:event_id>/register", methods=["POST"])
class EventRegister(MethodView):
    """Register a user for an event."""
    def post(self, event_id):
        event = get_event_by_id(event_id)
        if not event:
            abort(404, message="Event not found.")
        data = request.get_json()
        if not data or 'name' not in data or 'email' not in data:
            abort(400, message="Name and email required.")
        reg = register_user(event_id, data['name'], data['email'])
        return reg.as_dict(), 201

# PUBLIC_INTERFACE
@blp.route("/<int:event_id>/registrations")
class EventRegistrations(MethodView):
    """View registrations for an event (Organizer feature)."""
    def get(self, event_id):
        event = get_event_by_id(event_id)
        if not event:
            abort(404, message="Event not found.")
        regs = get_registrations_for_event(event_id)
        return {"registrations": [r.as_dict() for r in regs]}

# PUBLIC_INTERFACE
@blp.route("/<int:event_id>/registrations/<int:registration_id>", methods=["DELETE"])
class RemoveRegistration(MethodView):
    """Remove a registration from an event. (Organizer feature)"""
    def delete(self, event_id, registration_id):
        event = get_event_by_id(event_id)
        if not event:
            abort(404, message="Event not found.")
        success = remove_registration(registration_id)
        if not success:
            abort(404, message="Registration not found.")
        return {"message": "Registration removed."}
