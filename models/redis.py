
from redis.asyncio import Redis
from config import db_settings

_token_blacklist = Redis(
    host=db_settings.REDIS_HOST,
    port=db_settings.REDIS_PORT,
    db=0,
    decode_responses=True
)


async def add_token_to_blacklist(jti: str, exp: int) -> None:
    await _token_blacklist.setex(jti, exp, "blacklisted")


async def is_token_blacklisted(jti: str) -> bool:
    return await _token_blacklist.get(jti)
