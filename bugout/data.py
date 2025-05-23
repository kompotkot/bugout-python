import uuid
from datetime import datetime
from enum import Enum, unique
from typing import Any, Dict, List, Optional, Set, Union

from pydantic import BaseModel, Extra, Field, root_validator


@unique
class Method(Enum):
    delete = "delete"
    get = "get"
    post = "post"
    put = "put"


@unique
class Role(Enum):
    owner = "owner"
    member = "member"


@unique
class TokenType(Enum):
    bugout = "bugout"
    slack = "slack"
    github = "github"


@unique
class HolderType(Enum):
    user = "user"
    group = "group"


class ResourcePermissions(Enum):
    ADMIN = "admin"
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"


class AuthType(Enum):
    bearer = "Bearer"
    web3 = "Web3"


class JournalTypes(Enum):
    DEFAULT = "default"
    HUMBUG = "humbug"


class EntryRepresentationTypes(Enum):
    ENTRY = "entry"
    ENTITY = "entity"


class BugoutUser(BaseModel):
    id: uuid.UUID = Field(alias="user_id")
    username: str
    email: Optional[str]
    normalized_email: Optional[str]
    web3_address: Optional[str]
    verified: Optional[bool]
    autogenerated: Optional[bool]
    application_id: Optional[uuid.UUID]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class BugoutUserShort(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    user_type: Role


class BugoutToken(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    active: bool
    token_type: Optional[str]
    note: Optional[str]
    restricted: Optional[bool]
    created_at: datetime
    updated_at: datetime


class BugoutUserTokens(BaseModel):
    user_id: uuid.UUID
    username: str
    tokens: List[BugoutToken] = Field(alias="token")


class BugoutGroup(BaseModel):
    id: uuid.UUID
    group_name: Optional[str] = Field(alias="name")
    autogenerated: bool
    parent: Optional[uuid.UUID] = None
    application_id: Optional[uuid.UUID] = None


class BugoutGroupUser(BaseModel):
    group_id: uuid.UUID
    user_id: uuid.UUID
    user_type: str
    autogenerated: Optional[bool] = None
    group_name: Optional[str] = None
    parent: Optional[uuid.UUID] = None
    application_id: Optional[uuid.UUID] = None


class BugoutUserWithGroups(BugoutUser):
    groups: List[BugoutGroupUser] = Field(default_factory=list)


class BugoutUserGroups(BaseModel):
    groups: List[BugoutGroupUser]


class BugoutGroupMembers(BaseModel):
    id: uuid.UUID
    name: str
    users: List[BugoutUserShort]


class BugoutApplication(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    group_id: uuid.UUID


class BugoutApplications(BaseModel):
    applications: List[BugoutApplication]


class BugoutResource(BaseModel):
    id: uuid.UUID
    application_id: str
    resource_data: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


class BugoutResources(BaseModel):
    resources: List[BugoutResource]


class BugoutResourceHolder(BaseModel):
    id: uuid.UUID = Field(alias="holder_id")
    holder_type: HolderType
    permissions: List[ResourcePermissions] = Field(default_factory=list)

    class Config:
        # Required configuration because in Brood we use "holder_id" instead of "id"
        # during creation and deletion of new permissions for holder
        allow_population_by_field_name = True


class BugoutResourceHolders(BaseModel):
    resource_id: uuid.UUID
    holders: List[BugoutResourceHolder] = Field(default_factory=list)


class BugoutJournalPermission(BaseModel):
    holder_type: HolderType
    holder_id: str
    permissions: List[str] = Field(default_factory=list)


class BugoutJournalPermissions(BaseModel):
    journal_id: uuid.UUID
    permissions: List[BugoutJournalPermission] = Field(default_factory=list)


class BugoutScope(BaseModel):
    api: str
    scope: str
    description: str


class BugoutScopes(BaseModel):
    scopes: List[BugoutScope]


class BugoutJournalScopeSpec(BaseModel):
    journal_id: uuid.UUID
    holder_type: HolderType
    holder_id: str
    permission: str


class BugoutJournalScopeSpecs(BaseModel):
    scopes: List[BugoutJournalScopeSpec]


class BugoutJournal(BaseModel):
    id: uuid.UUID
    bugout_user_id: uuid.UUID
    holder_ids: Set[uuid.UUID] = Field(default_factory=set)
    name: str
    created_at: datetime
    updated_at: datetime


class BugoutJournals(BaseModel):
    journals: List[BugoutJournal]


class BugoutJournalEntry(BaseModel):
    id: uuid.UUID
    journal_url: Optional[str]
    content_url: Optional[str]
    title: Optional[str]
    content: Optional[str]
    tags: List[str] = Field(default_factory=list)
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    context_url: Optional[str]
    context_type: Optional[str]


class BugoutJournalEntries(BaseModel):
    entries: List[BugoutJournalEntry]


class BugoutJournalEntryRequest(BaseModel):
    title: str
    content: str
    tags: List[str] = Field(default_factory=list)
    context_url: Optional[str]
    context_id: Optional[str]
    context_type: Optional[str]


class BugoutJournalEntriesRequest(BaseModel):
    entries: List[BugoutJournalEntryRequest] = Field(default_factory=list)


class BugoutJournalEntryContent(BaseModel):
    title: str
    content: str
    tags: List[str] = Field(default_factory=list)
    locked_by: Optional[str] = None


class BugoutJournalEntryTags(BaseModel):
    journal_id: uuid.UUID
    entry_id: uuid.UUID
    tags: List[str]


class BugoutJournalEntryTagsRequest(BaseModel):
    journal_entry_id: uuid.UUID = Field(alias="entry_id")
    tags: List[str]

    class Config:
        # Required configuration because in Spire we use "journal_entry_id" instead of "entry_id"
        # during creation and deletion of new tags for journal entry
        allow_population_by_field_name = True


class BugoutJournalEntriesTagsRequest(BaseModel):
    entries: List[BugoutJournalEntryTagsRequest] = Field(default_factory=list)


class BugoutSearchResult(BaseModel):
    entry_url: str
    content_url: str
    title: str
    content: Optional[str]
    tags: List[str]
    created_at: str
    updated_at: str
    score: float
    context_type: Optional[str] = None
    context_url: Optional[str] = None
    context_id: Optional[str] = None


class BugoutHumbugIntegration(BaseModel):
    id: uuid.UUID
    group_id: uuid.UUID
    journal_id: uuid.UUID
    journal_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class BugoutHumbugIntegrationsList(BaseModel):
    integrations: List[BugoutHumbugIntegration] = Field(default_factory=list)


class BugoutSearchResultWithEntryID(BugoutSearchResult):
    id: str


class BugoutJournalEntityRequest(BaseModel, extra=Extra.allow):
    title: str
    address: str
    blockchain: str
    required_fields: List[Dict[str, Union[str, bool, int, list]]] = Field(
        default_factory=list
    )

    extra: Dict[str, Any]

    @root_validator(pre=True)
    def build_extra(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        all_required_field_names = {
            field.alias for field in cls.__fields__.values() if field.alias != "extra"
        }

        extra: Dict[str, Any] = {}
        for field_name in list(values):
            if field_name not in all_required_field_names:
                extra[field_name] = values.pop(field_name)
        values["extra"] = extra
        return values


class BugoutJournalEntity(BaseModel):
    id: uuid.UUID
    journal_id: uuid.UUID
    journal_url: Optional[str] = None
    title: Optional[str] = None
    address: Optional[str] = None
    blockchain: Optional[str] = None
    required_fields: Optional[List[Dict[str, Any]]] = None
    secondary_fields: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    locked_by: Optional[str] = None


class BugoutJournalEntities(BaseModel):
    entities: List[BugoutJournalEntity] = Field(default_factory=list)


class BugoutSearchResultAsEntity(BaseModel):
    journal_id: str
    entity_url: str
    title: str
    address: Optional[str] = None
    blockchain: Optional[str] = None
    required_fields: List[Dict[str, Any]] = Field(default_factory=list)
    secondary_fields: Dict[str, Any] = Field(default_factory=dict)
    created_at: str
    updated_at: str
    score: float


class BugoutSearchResults(BaseModel):
    total_results: int
    offset: int
    next_offset: Optional[int]
    max_score: float
    results: List[Union[BugoutSearchResult, BugoutSearchResultAsEntity]] = Field(
        default_factory=list
    )
