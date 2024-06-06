from dataclasses import dataclass, field
from typing import List, Dict, Optional
from dataclasses_json import dataclass_json, config
from datetime import datetime
from marshmallow import fields

from aeroglobebackend.data_models import AGAmountCurrencyCovert
from flights_providers.models.response.ag.ag_provider_base_response import AGProviderRefundBaseResponse


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
class AGFlightRefundResponse(AGProviderRefundBaseResponse):
    penalties: Optional[List[Dict[str, str]]] = field(default_factory=dict)
    passenger_details: List[AGPassengerDetails] = field(default_factory=list)
    refund_reference_id: str = None
    refund_status: str = None
