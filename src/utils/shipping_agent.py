from enum import Enum


class ShippingAgent(Enum):
    """
    Status Enums for response to API.
    """
    POSTNORD = 'PostNord'
    SCHENKER = 'Schenker'
    DHL = 'DHL'
    ROYALMAIL = 'Royal Mail'
    BRING = 'Bring'
    DEUTSCHEPOST = 'Deutsche Post'
    DPD = 'DPD'
    GLS = 'GLS'
    UPS = 'UPS'
    HERMES = 'Hermes'
