from dataclasses import dataclass
from typing import List
from dataclasses_json import dataclass_json
import fly_dubai_api_passenger_detail.py

@dataclass_json
@dataclass
class ChargesDetail:
    Amount: float
    CodeType: str
    CurrencyCode: str
    TaxCode: str

@dataclass_json
@dataclass
class FlyDubaiPassengerDetail:
    Title: str
    FirstName: str
    LastName: str
    PTCID: str
    TicketNumber: str
    Passport: str
    PersonOrgID: str
    MarketingCode: str
    OperatingRBD: str
    Charges: List[ChargesDetail]
    DOB: str = None
    PassportExpiryDate: str = None
