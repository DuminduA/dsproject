import json
from database import DbConnection
from .models import Bulksms, BulksmsInfo
from sqlalchemy.orm import Session
from .abstracts import BulksmsAbstract, BulksmsInfoAbstract, UpdateBulksmsStatus
from datetime import datetime
import uuid


class BulksmsRepository:
    def __init__(self, db: DbConnection):
        self.db = db

    # def get_all_bulksms(self):
    #     bulksms = self.db.query(Bulksms).all()
    #     return bulksmscreate_bulksms
    
    async def get_bulksms_by_id(self, bulksms_id:str):
        # return self.db.query(Bulksms).filter(Bulksms.id == bulksms_id).first()
    
        query = """
            SELECT * FROM bulksms WHERE id = :bulksms_id
        """
        row = await self.db.fetch_one(query=query, values={"bulksms_id": bulksms_id})
        return row
        
    async def create_bulksms(self, data:dict):
        validated_data = BulksmsAbstract(**data)
        bulksms = Bulksms(**validated_data.dict())
        print(bulksms.id)

        query = """
            INSERT INTO bulksms (id, name, status, message, contact_count, workspace_id, all_contacts, total_cost, created_at, modified_at)
            VALUES (:id, :name, :status, :message, :contact_count, :workspace_id, :all_contacts, :total_cost, :created_at, :modified_at)
        """
        # Execute the SQL query with parameters
        await self.db.execute(
            query,
            values={
                'id': bulksms.id,
                'name': bulksms.name,
                'status': bulksms.status,
                'message': bulksms.message,
                'contact_count': bulksms.contact_count,
                'workspace_id': bulksms.workspace_id,
                'total_cost': bulksms.total_cost,
                'created_at': bulksms.created_at,
                'modified_at': bulksms.modified_at,
                "all_contacts": json.dumps(bulksms.all_contacts)
            }
        )
        return bulksms
    
    async def update_bulksms_status(self, bulksms_id: uuid.UUID, status: str):
        validated_data = UpdateBulksmsStatus(
            bulksms_id=bulksms_id,
            status=status
        )
        bulksms = Bulksms(**validated_data.dict())

        query = """
            UPDATE bulksms set status=:status where id=:id
        """
        # Execute the SQL query with parameters
        await self.db.execute(
            query,
            values={
                'id': bulksms.id,
                'status': bulksms.status
            }
        )
        return bulksms
    
    async def add_bulksms_info_data(self, bulksms_id: uuid.UUID, contact_number: str, sms_status:str, sms_cost:float):
        validated_data = BulksmsInfoAbstract(
            bulksms_id=bulksms_id,
            contact_number=contact_number,
            contact_name=contact_number,
            sms_status=sms_status,
            sms_cost=sms_cost
        )
        bulksms_info = BulksmsInfo(**validated_data.dict())
        query = """
            INSERT INTO bulksms_info (
                id,bulksms_id, contact_number, contact_name,
                sms_status, sms_cost, created_at, modified_at
            )
            VALUES (
                :id, :bulksms_id, :contact_number, :contact_name,
                :sms_status, :sms_cost, :created_at, :modified_at
            )
        """
        # Execute the SQL query with parameters
        await self.db.execute(
            query,
            values = {
                "id": bulksms_info.id,
                "bulksms_id": bulksms_id,
                "contact_number": bulksms_info.contact_number,
                "contact_name": bulksms_info.contact_name,
                "sms_status": bulksms_info.sms_status,
                "sms_cost": bulksms_info.sms_cost,
                'created_at': bulksms_info.created_at,
                'modified_at': bulksms_info.modified_at,
            }
        )
        return bulksms_info
    
    
    async def get_bulksms_info_data(self, bulksms_id: uuid.UUID, contact: str):
        query = """
            SELECT id, bulksms_id, contact_number, contact_name,
                sms_status, sms_cost
            FROM bulksms_info
            WHERE bulksms_id = :bulksms_id AND contact_number = :contact_number
        """
        values = {
            "bulksms_id": bulksms_id,
            "contact_number": contact,
        }
        return await self.db.fetch_one(query=query, values=values)

    async def update_bulksms_info_data(self, bulksms_id:  uuid.UUID, sms_cost:float, sms_status:str):
        query = """
            UPDATE bulksms_info
            SET sms_cost = :sms_cost, sms_status = :sms_status
            WHERE bulksms_id = :bulksms_id
        """
        values = {
            "bulksms_id": bulksms_id,
            "sms_cost": sms_cost,
            "sms_status": sms_status,
        }
        await self.db.execute(
            query=query, values=values
            )
