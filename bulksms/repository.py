from database import DbConnection
from .models import Bulksms
from sqlalchemy.orm import Session
from .abstracts import BulksmsAbstract
from datetime import datetime
import uuid


class BulksmsRepository:
    def __init__(self, db: DbConnection):
        self.db = db

    # def get_all_bulksms(self):
    #     bulksms = self.db.query(Bulksms).all()
    #     return bulksms
    
    # def get_bulksms_by_id(self, bulksms_id:str):
    #     return self.db.query(Bulksms).filter(Bulksms.id == bulksms_id).first()
    
    async def create_bulksms(self, data:dict):
        validated_data = BulksmsAbstract(**data)
        bulksms = Bulksms(**validated_data.dict())
        print(bulksms.id)

        query = """
            INSERT INTO bulksms (id, name, status, message, contact_count, workspace_id, total_cost, created_at, modified_at)
            VALUES (:id, :name, :status, :message, :contact_count, :workspace_id, :total_cost, :created_at, :modified_at)
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
                'modified_at': bulksms.modified_at
            }
        )
        return bulksms