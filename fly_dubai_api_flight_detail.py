from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json

#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#ag_flight_refund_response.py
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from dataclasses_json import dataclass_json, config
from datetime import datetime
from marshmallow import fields
from decimal import Decimal
#AGAmountCurrencyCovert
@dataclass_json
@dataclass
class AGAmountCurrencyCovert:
    # value: decimal = None
    value: Decimal = field(
        metadata=config(
            encoder=lambda val: float(val) if val else val,
            decoder=lambda val: Decimal(val) if val else val,
            mm_field=fields.Decimal()
        ),
        default=None
    )
    currency: str = "PKR"
    
@dataclass_json
@dataclass
class RefundTaxInfoDetails:
    tax_code: str
    amount: AGAmountCurrencyCovert = None


@dataclass_json
@dataclass
class AGSegmentDetails:
    departure_city_code: str
    arrival_city_code: str
    departure_date_time: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )
    arrival_date_time: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )
    airline_code: str
    flight_number: str
    flight_segment_number: str
    segment_status: str = None


@dataclass_json
@dataclass
class RefundCharges:
    base_refund: AGAmountCurrencyCovert = None
    other_charges: AGAmountCurrencyCovert = None


@dataclass_json
@dataclass
class RefundFeesDetails:
    fee_code: str
    amount: AGAmountCurrencyCovert


@dataclass_json
@dataclass
class AGFareInfoDetails:
    currency_code: str = None
    tax_details: Optional[List[RefundTaxInfoDetails]] = field(default_factory=list)
    fee_details: Optional[List[RefundFeesDetails]] = field(default_factory=list)
    total_fare: AGAmountCurrencyCovert = None
    base_fare: AGAmountCurrencyCovert = None
    taxes: AGAmountCurrencyCovert = None
    fees: AGAmountCurrencyCovert = None
    others: AGAmountCurrencyCovert = None


@dataclass_json
@dataclass
class AGPassengerFareDetails:
    public_id: str
    fare_info: AGFareInfoDetails = None
    refund_charges: Optional[RefundCharges] = None
    status: str = None


@dataclass_json
@dataclass
class AGLegDetails:
    leg_public_id: str
    segment_details: List[AGSegmentDetails] = field(default_factory=list)
    fare_detail: AGPassengerFareDetails = field(default_factory=list)
    fare_basis: str = None


@dataclass_json
@dataclass
class AGPassengerDetails:
    first_name: str
    last_name: str
    passenger_type: str
    passenger_public_id: str
    title: str
    ticket_number: str = None
    leg_details: List[AGLegDetails] = field(default_factory=list)


@dataclass_json
@dataclass
class AGFlightRefundResponse:
    penalties: Optional[List[Dict[str, str]]] = field(default_factory=dict)
    passenger_details: List[AGPassengerDetails] = field(default_factory=list)
    refund_reference_id: str = None
    refund_status: str = None
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#fly_dubai_api_passenger_detail.py
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
    
    
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#fly_dubai_api_flight_detail.py
@dataclass_json
@dataclass
class Customers:
    AirlinePersons: List[FlyDubaiPassengerDetail]


@dataclass_json
@dataclass
class FlyDubaiFlightDetail:
    FlightNumber: str  # JSON key: "FlightNumber"
    CarrierCode: str  # JSON key: "OperatingCarrier"
    DepartureTime: str  # Assuming flight.get('DepartureTime') returns ISO format
    Arrivaltime: str  # Assuming flight.get('ArrivalTime') returns ISO format
    DestinationName: str  # JSON key: "DestinationName"
    OriginName: str  # JSON key: "OriginName"
    Destination: str  # JSON key: "Destination"
    Origin: str  # JSON key: "Origin"
    Customers: List[Customers]


@dataclass_json
@dataclass
class LogicalFlight:
    PhysicalFlights: List[FlyDubaiFlightDetail]


@dataclass_json
@dataclass
class Airlines:
    LogicalFlight: List[LogicalFlight]


@dataclass_json
@dataclass
class FlyDubaiPNRResponse:
    Airlines: List[Airlines]
    Cabin: str


#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
# FlyDubaiFlightService.py
class FlyDubaiFlightService:
     #Constructor to read the file and deserialize it.
    def __init__(self, file):
        self.file = file
        try:
            with open(file, "r") as read_file:
                json_data = read_file.read()
                self.pnr_response = FlyDubaiPNRResponse.from_json(json_data)
        except Exception as e:
            print(f"Error reading or deserializing JSON data: {e}")
    
      #Map passenger details to AGPassengerDetails format.
    def get_passenger_details(self, passenger):
       
        return AGPassengerDetails(
            first_name=passenger.FirstName,
            last_name=passenger.LastName,
            passenger_type=passenger.PTCID,
            passenger_public_id=passenger.PersonOrgID,
            title=passenger.Title,
            ticket_number=passenger.TicketNumber,
        )

    # Map refund charges to RefundCharges format.
    def get_refund_charges(self, charge):
       
       
        return RefundCharges(
            base_refund=AGAmountCurrencyCovert(value=charge.Amount, currency=charge.CurrencyCode),
            other_charges=AGAmountCurrencyCovert(value=charge.Amount, currency=charge.CurrencyCode),
        )
        
    # Map leg details to AGLegDetails format.
    def get_leg_details(self, passenger):
            
            return AGLegDetails(
                leg_public_id=passenger.PersonOrgID,
                segment_details=[],
                fare_detail=AGPassengerFareDetails(
                    public_id=passenger.PersonOrgID,
                    refund_charges=self.map_refund_charges(passenger.Charges[0]),
                ),
            )
    
    # Map segment details to AGSegmentDetails format.
    def get_segment_details(self, physical_flight):
        segment_details = []
        for customer in physical_flight.Customers:
            for passenger in customer.AirlinePersons:
                segment_details.append(
                    AGSegmentDetails(
                        departure_city_code=physical_flight.Origin,
                        arrival_city_code=physical_flight.Destination,
                        departure_date_time=datetime.fromisoformat(physical_flight.DepartureTime),
                        arrival_date_time=datetime.fromisoformat(physical_flight.Arrivaltime),
                        airline_code=physical_flight.CarrierCode,
                        flight_number=physical_flight.FlightNumber,
                        flight_segment_number=passenger.PersonOrgID,
                    )
                )
        return segment_details
    
    # Map fare details to AGFareInfoDetails format.
    def get_fare_details(self, passenger):
        return AGFareInfoDetails(
            currency_code=passenger.Charges[0].CurrencyCode,
            total_fare=AGAmountCurrencyCovert(value=passenger.Charges[0].Amount, currency=passenger.Charges[0].CurrencyCode),
            base_fare=AGAmountCurrencyCovert(value=passenger.Charges[0].Amount, currency=passenger.Charges[0].CurrencyCode),
            taxes=AGAmountCurrencyCovert(value=passenger.Charges[0].Amount, currency=passenger.Charges[0].CurrencyCode),
            fees=AGAmountCurrencyCovert(value=passenger.Charges[0].Amount, currency=passenger.Charges[0].CurrencyCode),
            others=AGAmountCurrencyCovert(value=passenger.Charges[0].Amount, currency=passenger.Charges[0].CurrencyCode),
        )
    
    
    # map charges details to RefundTaxInfoDetails format.
    # def get_charge_details(self, passenger):
    #     tax_details = []
    #     for charge in passenger.Charges:
    #         if charge.CodeType == 'TAX':
    # # tax details but same tax_code is not merged
    #             tax_details.append(
    #                 RefundTaxInfoDetails(
    #                     tax_code=charge.TaxCode,
    #                     amount=AGAmountCurrencyCovert(value=charge.Amount, currency=charge.CurrencyCode)
    #                 )
    #             )
    #     return tax_details
    
    
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    # Map charges details to RefundTaxInfoDetails format.
    def get_charge_details(self, passenger):
        tax_details = []
        for charge in passenger.Charges:
            if charge.CodeType == 'TAX':
                # Find if the tax_code already exists in tax_details
                existing_tax_detail = next((tax for tax in tax_details if tax.tax_code == charge.TaxCode), None)
                if existing_tax_detail:
                    # Add up the value if the tax_code exists
                    existing_tax_detail.amount.value += Decimal(charge.Amount)
                else:
                    # Append new tax detail if the tax_code does not exist
                    tax_details.append(RefundTaxInfoDetails(
                        tax_code=charge.TaxCode,
                        amount=AGAmountCurrencyCovert(value=Decimal(charge.Amount), currency=charge.CurrencyCode),
                    ))
        return tax_details
    #--------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------
    
    # Map refund charges to RefundCharges format.
    def map_refund_charges(self, charge):
        return RefundCharges(
            base_refund=AGAmountCurrencyCovert(value=charge.Amount, currency=charge.CurrencyCode),
            other_charges=AGAmountCurrencyCovert(value=charge.Amount, currency=charge.CurrencyCode),
        )

    #Map deserialized data to AGFlightRefundResponse.
    def map_to_ag_flight_refund_response(self):
        refund_response = AGFlightRefundResponse()
        refund_response.passenger_details = []

        for airline in self.pnr_response.Airlines:
            for logical_flight in airline.LogicalFlight:
                for physical_flight in logical_flight.PhysicalFlights:
                    for customer in physical_flight.Customers:
                        for passenger in customer.AirlinePersons:
                            passenger_detail = self.get_passenger_details(passenger)
                            refund_charge = self.get_refund_charges(passenger.Charges[0])
                            passenger_detail.fare_detail = AGPassengerFareDetails(
                                public_id=passenger.PersonOrgID,
                                refund_charges=refund_charge,
                            )
                            passenger_detail.leg_details.append(self.get_leg_details(passenger))
                            passenger_detail.leg_details[-1].segment_details = self.get_segment_details(physical_flight)
                            passenger_detail.leg_details[-1].fare_detail = self.get_fare_details(passenger)
                            passenger_detail.leg_details[-1].fare_detail.tax_details = self.get_charge_details(passenger)
                            refund_response.passenger_details.append(passenger_detail)
        return refund_response
    
        
    
    
    
         

            
# Usage
service = FlyDubaiFlightService("D:\\OneDrive - FAST National University\\samaha\\\\aeroglobeInternship\\Task4FlyDubaiResponse\\Cancel_API _resp.json")
response = service.map_to_ag_flight_refund_response()
# print(response.to_json())

# #print response  formatted by seperating each passenger details
# for passenger in response.passenger_details:
#     for key, value in passenger.to_dict().items():
#             print(f"{key}: {value}")
#     print("\n")

#print only charges details of each cusotmer
for passenger in response.passenger_details:
    print(f"Passenger: {passenger.first_name} {passenger.last_name}")
    for leg in passenger.leg_details:
        for fare in leg.fare_detail.tax_details:
            for key, value in fare.to_dict().items():
                print(f"{key}: {value}")
    print("\n")




