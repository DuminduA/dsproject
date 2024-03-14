from uuid import UUID

from database import DbConnection
from shortid import ShortId


async def get_workspace_credit(workspace_id: UUID, db_conn: DbConnection):
    query = f"""
        SELECT id, credit
        FROM workspace
        WHERE id = :workspace_id
    """
    return await db_conn.fetch_one(query=query, values={"workspace_id": ShortId(workspace_id).uuid()})


async def deduct_credit(workspace_id: UUID, db_conn: DbConnection):
    query = f"""
        UPDATE workspace
        SET credit = credit - 0.1
        WHERE id = :workspace_id
    """
    values = {"workspace_id": workspace_id}
    await db_conn.execute(query=query, values=values)
    return await get_workspace_credit(workspace_id=ShortId.with_uuid(workspace_id), db_conn=db_conn)