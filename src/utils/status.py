from enum import Enum


class Status(Enum):
    """ Status Enums for response to API."""

    ACCEPTED = 'ACCEPTED'
    CORRECTED = 'CORRECTED'
    REJECTED = 'REJECTED'
