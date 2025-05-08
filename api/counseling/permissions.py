# permissions.py
from rest_framework import permissions

class IsStudentOrPsychologist(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Student can only access their own session
        if request.method in ['GET', 'POST']:
            return obj.student == request.user
        # Psychologist can only update their own sessions
        elif request.method in ['PATCH', 'PUT']:
            return obj.psychologist == request.user
        return False
