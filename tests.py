import asyncio
from decimal import Decimal

from pydantic_core._pydantic_core import ValidationError

from xml_schemas import MakeTransferToCardSchema, PersonInfoSchema
from main import make_transfer_to_card_post_request


def test_parsing_data_to_xml():
    try:
        # test data
        transfer = MakeTransferToCardSchema(
            PartnerID=11234,
            TransactionID=775829504,
            PayDate="2018-05-04",
            CardNumber="9051000011112222",
            Currency="AMD",
            Amount="1000.0",
            Recipient=PersonInfoSchema(
                Name="Պողոսյան Պետրոս",
                Country="AM",
                City="Yerevan",
                Street="Charents",
                PostalCode="0025"
            ),
            Signature="mz2AtKE5wI6EOSuAT6434C96gKUFmH32srH1wHvvZz8="
        )

        xml_str = transfer.to_xml(pretty_print=True, encoding='unicode', xml_declaration=False)
        print(xml_str)

    except ValidationError as e:
        print("Validation error:", e)


def test_make_transfer_to_card_post_request():
    try:
        # Подготовка данных
        transfer = MakeTransferToCardSchema(
            PartnerID=11234,
            TransactionID=775829504,
            PayDate="2018-05-04",
            CardNumber="9051000011112222",
            Currency="AMD",
            Amount=Decimal("1000.0"),
            Sender=PersonInfoSchema(
                Name="Անանուն Ուղարկող",
                Country="AM",
                City="Yerevan",
                Street="Abovyan",
                PostalCode="0010"
            ),
            Recipient=PersonInfoSchema(
                Name="Պողոսյան Պետրոս",
                Country="AM",
                City="Yerevan",
                Street="Charents",
                PostalCode="0025"
            ),
            Signature="mz2AtKE5wI6EOSuAT6434C96gKUFmH32srH1wHvvZz8="
        )

        xml_body = transfer.to_xml(pretty_print=True, encoding='unicode', xml_declaration=False)

        async def inner():
            status, response_text = await make_transfer_to_card_post_request(xml_body=xml_body, url ="https://httpbin.org/post")
            print(f"Response Status: {status}")
            assert status == 200, "Status code is not 200"
            assert "<CardNumber>9051000011112222</CardNumber>" in response_text, "Card number not found in response body"
            print("✅ Test passed successfully.")

        asyncio.run(inner())

    except ValidationError as e:
        print("Validation error:", e)


if __name__ == '__main__':
    test_parsing_data_to_xml()
    test_make_transfer_to_card_post_request()
