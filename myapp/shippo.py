from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import shippo
from shippo.models import components
import json


shippo_sdk = shippo.Shippo(api_key_header="shippo_test_f3cb884569acedbe9a0860114d181ec57bed5277")

@csrf_exempt
def submit_address(request):
    if request.method == "POST":
        data = json.loads(request.body)

        address_from = components.AddressCreateRequest(
            firstname=data.get("customerFirstName"),
            lastname=data.get("customerLastName"),
            streetAddress=data.get("customerStreetAddress"),
            addressOptional=data.get("addressOptional", ""),  # If provided
            city=data.get("customerCity"),
            state=data.get("customerState"),
            zip=data.get("customerZipCode"),
            country="US",
            phone=data.get("customerPhone"),
            email=data.get("customerEmail")
        )

        address_to = components.AddressCreateRequest(
            name="Mr Hippo",
            company="",
            street1="Broadway 1",
            street2="",
            city="New York",
            state="NY",
            zip="10007",
            country="US",
            phone="+1 555 341 9393",
            email="mrhippo@shippo.com",
            metadata="Hippos dont lie"
        )

        parcel = components.ParcelCreateRequest(
            length="5",
            width="5",
            height="5",
            distance_unit=components.DistanceUnitEnum.IN,
            weight="2",
            mass_unit=components.WeightUnitEnum.LB
        )

        shipment = components.ShipmentCreateRequest(
            address_from=address_from,
            address_to=address_to,
            parcels=[parcel]
        )

        transaction = shippo_sdk.transactions.create(
            components.InstantTransactionCreateRequest(
                shipment=shipment,
                carrier_account="49dcfb244b4540bebe1158d41cac4042",
                servicelevel_token="FedEx FedEx Priority"
            )
        )

        if transaction.status == "SUCCESS":
            # Return success response with tracking URL and shipping label URL
            return JsonResponse({
                'status': 'success',
                'tracking_url': transaction.tracking_url_provider,
                'label_url': transaction.label_url
            })
        else:
            # Return error response if transaction fails
            return JsonResponse({
                'status': 'error',
                'message': transaction.error_message
            })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})