from typing import Optional, TypedDict
from decimal import Decimal
from datetime import datetime

from pydantic_xml import BaseXmlModel, element, attr
from pydantic import field_validator, ValidationInfo, ValidationError


class PersonInfoSchemaDict(TypedDict):
    Name: str
    Country: str
    City: str
    Street: str
    PostalCode: str


class PersonInfoSchema(BaseXmlModel, tag='Sender'):
    Name: str = element(default=..., max_length=100)
    Country: str = element(default=..., pattern=r'^[A-Z]{2}$')  # ISO 3166-1 alpha-2
    City: str = element(default=..., max_length=100)
    Street: str = element(default=..., max_length=100)
    PostalCode: str = element(default=..., max_length=10)


class MakeTransferToCardSchema(BaseXmlModel, tag='MakeTransferToCard'):
    class Config:
        xml_nsmap = {
            'i': "http://www.w3.org/2001/XMLSchema-instance",
            None: "http://schemas.datacontract.org/2004/07/ArmenianSoftware.Bank.IntegrationService.Common"
        }

    PartnerID: int = element()
    TransactionID: int = element()
    PayDate: str = element()
    CardNumber: str = element(default=..., max_length=16)
    Currency: str = element(default=..., max_length=3, pattern=r'^[A-Z]{3}$')
    Amount: Decimal = element()
    Sender: Optional[PersonInfoSchema] = element(default=None)
    Recipient: PersonInfoSchema = element()
    Signature: str = element()

    @field_validator('PayDate', mode='before')  # noqa
    @classmethod
    def validate_pay_date_format(cls, value: str) -> str:
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError('PayDate must be in YYYY-MM-DD format')
        return value

    @field_validator('PartnerID', mode='before')  # noqa
    @classmethod
    def validate_five_digit_int(cls, value: int) -> int:
        if isinstance(value, int) and len(str(value)) != 5:
            raise ValueError('PartnerID must be a 5-digit integer')
        return value
