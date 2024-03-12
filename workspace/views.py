from uuid import UUID

from database import DbConnection


async def active_workspace_credit(
    workspace_id: UUID,
    db_conn: DbConnection,
):

    query = (
        sa.select(
            [
                orm.workspace_credit.c.id.label("id"),
                orm.workspace_credit.c.amount.label("amount"),
                orm.workspace_credit.c.workspace.label("workspace"),
            ]
        )
        .where(
                orm.billing_credit.c.workspace == workspace_id
            )
        )
    )
    return await db_conn.fetch_one(query)