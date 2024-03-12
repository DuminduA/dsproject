from starlette.requests import Request
from bulksms.helpers import prepare_contact_list_for_estimation_csv, process_contacts_csv
from bulksms.services import BulksmsServices
from starlette.responses import JSONResponse


# @requires(scopes=['authenticated', 'admin'])
# async def create_product(request: Request):
#     db = request.app.state.db
#     try:
#         product_service = ProductServices(db)
#         data = await request.json()
#         product = product_service.create_product(data)
#         product = DatabaseProductAbstract(
#             id=product.id,
#             name=product.name,
#             price=product.price,
#             description=product.description,
#             quantity= product.quantity,
#             # image=product.image,
#         )
#         product = product.dict()
#         product['id'] = str(product['id'])
#         return JSONResponse(
#             product,
#         )
#     except Exception as e:
#         return JSONResponse({'message': str(e)}, status_code=400)

from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR


# @check_workspace_under_review
async def create_bulksms(request):
    data = await request.form()
    db_conn = request.app.state.db
    try:
        bulksms_service = BulksmsServices(db_conn)        

        # Access uploaded files
        # csv_file = data['file'].file  # Get the file object

        csv_file = data.get("file")
        all_contacts = await process_contacts_csv(
            csv_file=csv_file,
            contact_name_column="Full Name",
            usecols=["Full Name", "Phone Number"],
        )
        all_contacts = prepare_contact_list_for_estimation_csv(
            all_contacts
        )
        bulksms = await bulksms_service.create_bulksms(data)
        # await request.app.state.queue.run_task(
        #     "task_estimate_bulksms_cost",
        #     bulksms.id,
        #     all_contacts,
        #     data["message"],
        #     _queue_name="arq:twilio_queue",
        # )

        return JSONResponse({"status": 200, "data": {"success": True}, "error": None})

    except Exception as e:
        return JSONResponse(
            {"message": str(e)},
            status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )