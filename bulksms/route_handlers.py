import json
from starlette.requests import Request
from bulksms import abstracts
from bulksms.helpers import prepare_contact_list_for_estimation_csv, process_contacts_csv
from bulksms.services import BulksmsServices
from starlette.responses import JSONResponse


from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from shortid import ShortId


# @check_workspace_under_review
async def create_bulksms(request):
    data = await request.form()
    db_conn = request.app.state.db
    # try:
    bulksms_service = BulksmsServices(db_conn)        

    # Access uploaded files
    # csv_file = data['file'].file  # Get the file object

    csv_file = data.get("file")
    all_contacts = await process_contacts_csv(
        csv_file=csv_file,
        contact_name_column="Contact Name",
        usecols=["Contact Name", "Phone Number"],
    )
    all_contacts = prepare_contact_list_for_estimation_csv(
        all_contacts
    )
    print(all_contacts)

    new_data = {key: value for key, value in data.items()}
    # Add all_contacts to the new dictionary
    new_data["all_contacts"] = all_contacts
    bulksms = await bulksms_service.create_bulksms(new_data)
    # await request.app.state.queue.run_task(
    #     "task_estimate_bulksms_cost",
    #     bulksms.id,
    #     all_contacts,
    #     data["message"],
    #     _queue_name="arq:twilio_queue",
    # )

    return JSONResponse({"status": 200, "data": {"success": True}, "error": None})

    # except Exception as e:
    #     return JSONResponse(
    #         {"message": str(e)},
    #         status_code=HTTP_500_INTERNAL_SERVER_ERROR
    #     )
    
async def run_bulksms(request: Request):
    # try:
    db_conn = request.app.state.db
    data = await request.json()  # Assuming data is sent as JSON in the request body

    # Your authentication and permission checks can be performed here

    # Extract necessary data from the request
    bulksms_service = BulksmsServices(db_conn)
    bulksms_id = data["bulksms_id"]
    bulksms = await bulksms_service.get_bulksms_by_id(bulksms_id=bulksms_id)
    print(bulksms)
    # workspace_credit = await bulksms_service.grpc_get_workspace_credit(
    #     bulksms["workspace_id"]
    # )
    workspace_credit = 10
    await bulksms_service.update_bulksms_status(
            bulksms_id=bulksms_id, status="inprogress"
        )
    print(dict(bulksms))
    await request.app.state.queue.run_task(
        "run_bulksms_campaign",
        abstracts.SendBulkSms(
            content=bulksms["message"],
            contacts=json.loads(bulksms["all_contacts"]),
            workspace=ShortId.with_uuid(bulksms["workspace_id"]),
            bulksms_id=ShortId.with_uuid(bulksms['id']),
            # estimated_cost=campaign["estimated_cost"],
        ),
        _queue_name="arq:general_queue",
    )

    # Perform necessary business logic using your services and views
    # Example: Call views.get_bulksms_campaign_detail, services.update_bulksms_campaign_status, etc.

    # Construct the response data
    response_data = {
        "status": 200,
        "data": {"success": True},
        "error": None
    }

    return JSONResponse(response_data)

    # except ValidationError as e:
    #     error_message = "Invalid input: " + str(e)
    #     return JSONResponse({"error": error_message}, status_code=400)