import asyncio
from decimal import Decimal
from typing import Tuple

import aiohttp
import json
import ssl

from xml_schemas import (
    PersonInfoSchema,
    MakeTransferToCardSchema,
    PersonInfoSchemaDict,
)
from settings import DOMAIN, PARTNER_ID


SSL_CONTEXT = ssl.create_default_context(cafile="")  # if needed
USE_SSL = False  # set to True if using HTTPS

PROTOCOL = "https" if USE_SSL else "http"
URL = f"{PROTOCOL}://{DOMAIN}/Partners/{PARTNER_ID}/TransferToCard"

SENDER: PersonInfoSchemaDict = {
    "Name": "...",
    "Country": "...",
    "City": "...",
    "Street": "...",
    "PostalCode": "...",
}

RECIPIENT: PersonInfoSchemaDict = {
    "Name": "...",
    "Country": "...",
    "City": "...",
    "Street": "...",
    "PostalCode": "...",
}


def build_xml_body(
    partner_id: int,
    transaction_id: int,
    pay_date: str,
    card_number: str,
    currency: str,
    amount: Decimal,
    sender: PersonInfoSchemaDict,
    recipient: PersonInfoSchemaDict,
    signature: str,
) -> str:
    body = MakeTransferToCardSchema(
        PartnerID=partner_id,
        TransactionID=transaction_id,
        PayDate=pay_date,
        CardNumber=card_number,
        Currency=currency,
        Amount=amount,
        Sender=PersonInfoSchema(**sender),
        Recipient=PersonInfoSchema(**recipient),
        Signature=signature,
    )
    return body.to_xml(encoding="utf-8", xml_declaration=False)


async def make_transfer_to_card_post_request(
    url: str,
    xml_body: str
) -> Tuple[int, str]:
    headers = {"Content-Type": "application/xml"}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=url, data=xml_body.encode("utf-8"), headers=headers
        ) as response:
            return response.status, await response.text()


async def main():
    xml_body = build_xml_body(
        partner_id=PARTNER_ID,
        transaction_id=12345,
        pay_date="2025-06-05",
        card_number="1234567890123456",
        currency="USD",
        amount=Decimal("100.00"),
        sender=SENDER,
        recipient=RECIPIENT,
        signature="example_signature",
    )

    status, text = await make_transfer_to_card_post_request(URL, xml_body)
    print(f"RESPONSE STATUS: {status}")

    try:
        from pprint import pprint
        pprint(json.loads(text))
    except json.JSONDecodeError:
        print("Response is not JSON:", text)


if __name__ == "__main__":
    asyncio.run(main())
