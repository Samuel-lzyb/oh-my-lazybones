"""Shared test fixtures."""

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from server.config import settings
from server.database import get_db
from server.dependencies import get_search_service, get_skill_registry
from server.main import app
from server.models import Base
from server.models.skill import Skill
from server.repositories.skill import SkillRepository
from server.schemas.skill import SkillCreate
from server.services.search import SearchService
from server.services.skill_registry import SkillRegistry


# ── Database ──────────────────────────────────────────────
TEST_DB_URL = "sqlite+aiosqlite://"


@pytest_asyncio.fixture
async def db_session():
    """In-memory SQLite session with tables created."""
    engine = create_async_engine(TEST_DB_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    test_sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    async with test_sessionmaker() as session:
        yield session

    await engine.dispose()


@pytest_asyncio.fixture
async def repo(db_session: AsyncSession):
    """SkillRepository wired to test DB."""
    return SkillRepository(db_session)


# ── Mock Search ────────────────────────────────────────────
class MockSearchService(SearchService):
    """In-memory search for testing — no Meilisearch needed."""

    def __init__(self):
        self._index: dict[str, dict] = {}

    async def index(self, skill: dict) -> None:
        self._index[skill["name"]] = skill

    async def deindex(self, name: str) -> None:
        self._index.pop(name, None)

    async def search(self, query, tag, sort, page, limit):
        results = [
            name for name, s in self._index.items()
            if query.lower() in name.lower()
            or query.lower() in s.get("description", "").lower()
        ]
        total = len(results)
        start = (page - 1) * limit
        return results[start:start + limit], total

    async def reindex_all(self, skills):
        self._index = {s["name"]: s for s in skills}


@pytest_asyncio.fixture
async def search_svc():
    return MockSearchService()


# ── SkillRegistry ──────────────────────────────────────────
@pytest_asyncio.fixture
async def registry(repo: SkillRepository, search_svc: MockSearchService):
    return SkillRegistry(repo, search_svc)


# ── API Client ─────────────────────────────────────────────
@pytest_asyncio.fixture
async def client(db_session: AsyncSession, search_svc: MockSearchService):
    """Async HTTP client with test DB and mock search."""
    async def override_get_db():
        yield db_session

    def override_get_search():
        return search_svc

    async def override_get_registry(
        db=db_session,  # noqa: B008
    ):
        repo = SkillRepository(db)
        return SkillRegistry(repo, search_svc)

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_search_service] = override_get_search

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


# ── Helpers ────────────────────────────────────────────────
@pytest_asyncio.fixture
async def sample_skill(repo: SkillRepository):
    """Create a sample skill in the DB."""
    skill = Skill(
        name="test-skill",
        version="0.1.0",
        author="dev",
        description="A test skill",
        tags=["test"],
    )
    return await repo.create(skill)
