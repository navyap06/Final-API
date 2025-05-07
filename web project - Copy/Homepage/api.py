from flask import request
from flask_restful import Resource
from models import db, User, LeaveRequest


class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }


class LeaveRequestListResource(Resource):
    def get(self):
    
        leave_requests = LeaveRequest.query.all()
        return [
            {
                "id": lr.id,
                "employee_name": lr.employee_name,
                "leave_type": lr.leave_type,
                "start_date": lr.start_date,
                "end_date": lr.end_date,
                "status": lr.status
            } for lr in leave_requests
        ]
    
    def post(self):
        if request.content_type != 'application/json':
         return {"message": "Content-Type must be application/json"}, 415

        data = request.get_json(silent=True)
        if not data:
         return {"message": "No JSON data provided or bad JSON format."}, 400

        required_fields = ['employee_name', 'leave_type', 'start_date', 'end_date']
        missing = [field for field in required_fields if not data.get(field)]
        if missing:
         return {"message": f"Missing required fields: {', '.join(missing)}"}, 400

        new_request = LeaveRequest(
          employee_name=data['employee_name'],
          leave_type=data['leave_type'],
          start_date=data['start_date'],
          end_date=data['end_date'],
          status=data.get('status', 'Pending')
        )
        db.session.add(new_request)
        db.session.commit()
        return {"message": "Request added successfully."}, 201



class LeaveRequestResource(Resource):
    def get(self, leave_id):
        leave = LeaveRequest.query.get_or_404(leave_id)
        return {
            "id": leave.id,
            "employee_name": leave.employee_name,
            "leave_type": leave.leave_type,
            "start_date": leave.start_date,
            "end_date": leave.end_date,
            "status": leave.status
        }

    def put(self, leave_id):
        leave = LeaveRequest.query.get_or_404(leave_id)
        data = request.get_json()  # This reads the JSON from the request body

        if 'action' in data:
            action = data['action']
            if action == "approve":
                leave.status = "Approved"
            elif action == "reject":
                leave.status = "Rejected"
            else:
                return {"error": "Invalid action"}, 400

            db.session.commit()
            return {"message": f"Leave request {action}d successfully."}, 200
        else:
            return {"error": "Action not provided."}, 400
    
    def delete(self, leave_id):
        leave = LeaveRequest.query.get_or_404(leave_id)
        db.session.delete(leave)
        db.session.commit()
        return {"message": "Leave request deleted successfully."}, 200