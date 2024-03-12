import json
from database import DbConnection
from .models import Bulksms
from sqlalchemy.orm import Session
from .abstracts import BulksmsAbstract, UpdateBulksmsStatus
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
        row = await self.db.fetch_one(query=query, values={"bulksms_id": uuid.UUID(bulksms_id)})
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