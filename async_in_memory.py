from typing import Optional

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

SQLITE_SYNC_URL_PREFIX = "sqlite:///"
SQLITE_ASYNC_URL_PREFIX = "sqlite+aiosqlite:///"
MEMORY_LOCATION_START = "file:"
MEMORY_LOCATION_END = "?mode=memory&cache=shared&uri=true"


class InMemoryDatabase:
    """
    Async in-memory SQLite DB
    """

    def __init__(self, sql_echo: bool = False):
        self.sql_echo = sql_echo
        self._sync_memory_engine: Optional[Engine] = None
        self._async_memory_engine: Optional[AsyncEngine] = None
        self._async_sessionmaker: Optional[sessionmaker] = None

    def setup(self, filename: str):
        """
        Copy DB data from disk to memory and setup async session
        """
        sync_disk_engine = create_engine(
            url=SQLITE_SYNC_URL_PREFIX + filename, echo=self.sql_echo
        )
        in_memory_url = MEMORY_LOCATION_START + filename + MEMORY_LOCATION_END
        # Reference to sync in-memory engine remains open
        self._sync_memory_engine = create_engine(
            url=SQLITE_SYNC_URL_PREFIX + in_memory_url, echo=self.sql_echo
        )
        # Use sync engines to copy DB to memory
        backup_db(source_db=sync_disk_engine, target_db=self._sync_memory_engine)
        sync_disk_engine.dispose()
        # Create async engine at same memory location
        self._async_memory_engine = create_async_engine(
            url=SQLITE_ASYNC_URL_PREFIX + in_memory_url, echo=self.sql_echo
        )
        self._async_sessionmaker = sessionmaker(
            self._async_memory_engine, class_=AsyncSession
        )