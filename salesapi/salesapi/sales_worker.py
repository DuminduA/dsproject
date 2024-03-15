from salesapi.salesapi import settings as config
from arq.connections import RedisSettings
import bootstrap
from bulksms.queue_handlers import (
    save_bulksms_campaign_info,
    generate_system_stat

    # task_update_bulksms_campaign
)


async def startup(ctx):
    settings = config.get_application_settings()
    ctx["settings"] = settings
    ctx["db"] = bootstrap.init_database(ctx["settings"])
    ctx["broadcaster"] = bootstrap.init_broadcaster(ctx["settings"])
    ctx["queue"] = bootstrap.init_queue(ctx["settings"])
    await ctx["db"].connect()
    await ctx["queue"].connect()
    await ctx["broadcaster"].connect()


async def shutdown(ctx):
    await ctx["db"].disconnect()


class WorkerSettings:
    settings = config.get_application_settings()

    functions = [
        save_bulksms_campaign_info,
        generate_system_stat
        # task_update_bulksms_campaign,
    ]
    queue_name = "arq:sales_queue"
    on_startup = startup
    on_shutdown = shutdown

    redis_settings = RedisSettings.from_dsn(settings.redis_settings)
    # if os.environ.get("REDIS_HOST"):
    #     redis_settings = RedisSettings(host=os.environ.get("REDIS_HOST"))
