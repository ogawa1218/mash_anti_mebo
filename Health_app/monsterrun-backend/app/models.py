"""SQLAlchemy 2.0 ORM models — 1:1 with migrations/001_initial_schema.sql."""

import enum
import uuid
from datetime import date, datetime

from sqlalchemy import (
    ARRAY,
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class WearableSource(str, enum.Enum):
    garmin = "garmin"
    strava = "strava"
    apple_healthkit = "apple_healthkit"
    google_health_connect = "google_health_connect"
    manual = "manual"


class ActivityStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    flagged = "flagged"
    quarantined = "quarantined"
    rejected = "rejected"
    duplicate = "duplicate"


class ActivityType(str, enum.Enum):
    run = "run"
    walk = "walk"
    ride = "ride"
    swim = "swim"
    strength = "strength"
    hike = "hike"
    other = "other"


class EvolutionLine(str, enum.Enum):
    balanced = "balanced"
    stamina_guardian = "stamina_guardian"
    speed_striker = "speed_striker"


class MonsterAnim(str, enum.Enum):
    idle = "idle"
    happy = "happy"
    tired = "tired"
    training = "training"
    evolving = "evolving"
    sick = "sick"
    sleeping = "sleeping"


class EffectKind(str, enum.Enum):
    buff = "buff"
    debuff = "debuff"


def _enum(e: type[enum.Enum], name: str) -> Enum:
    return Enum(e, name=name, values_callable=lambda x: [m.value for m in x])


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(Text, unique=True)
    display_name: Mapped[str] = mapped_column(Text)
    password_hash: Mapped[str | None] = mapped_column(Text)
    date_of_birth: Mapped[date | None] = mapped_column(Date)
    sex: Mapped[str | None] = mapped_column(Text)
    height_cm: Mapped[float | None] = mapped_column(Numeric(5, 1))
    weight_kg: Mapped[float | None] = mapped_column(Numeric(5, 1))
    hr_rest: Mapped[int] = mapped_column(SmallInteger, default=60)
    hr_max: Mapped[int | None] = mapped_column(SmallInteger)
    timezone: Mapped[str] = mapped_column(Text, default="Asia/Tokyo")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    connections: Mapped[list["WearableConnection"]] = relationship(back_populates="user")
    monsters: Mapped[list["Monster"]] = relationship(back_populates="user")

    def estimated_hr_max(self, on: date | None = None) -> int:
        """Tanaka式 (208 - 0.7*age)。実測値があればそちらを優先。"""
        if self.hr_max:
            return self.hr_max
        if self.date_of_birth:
            today = on or date.today()
            age = (today - self.date_of_birth).days // 365
            return round(208 - 0.7 * age)
        return 185


class WearableConnection(Base):
    __tablename__ = "wearable_connections"
    __table_args__ = (
        UniqueConstraint("source", "provider_user_id"),
        UniqueConstraint("user_id", "source"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    source: Mapped[WearableSource] = mapped_column(_enum(WearableSource, "wearable_source"))
    provider_user_id: Mapped[str] = mapped_column(Text)
    access_token_enc: Mapped[str] = mapped_column(Text)
    refresh_token_enc: Mapped[str | None] = mapped_column(Text)
    token_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    scopes: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped[User] = relationship(back_populates="connections")


class RawPayload(Base):
    __tablename__ = "raw_payloads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[WearableSource] = mapped_column(_enum(WearableSource, "wearable_source"))
    external_id: Mapped[str | None] = mapped_column(Text)
    payload: Mapped[dict] = mapped_column(JSONB)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class WearableActivity(Base):
    __tablename__ = "wearable_activities"
    __table_args__ = (UniqueConstraint("source", "external_id"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    source: Mapped[WearableSource] = mapped_column(_enum(WearableSource, "wearable_source"))
    external_id: Mapped[str] = mapped_column(Text)
    activity_type: Mapped[ActivityType] = mapped_column(
        _enum(ActivityType, "activity_type"), default=ActivityType.run
    )
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    duration_s: Mapped[int] = mapped_column(Integer)
    distance_m: Mapped[float] = mapped_column(Numeric(10, 1), default=0)
    steps: Mapped[int | None] = mapped_column(Integer)
    calories_active: Mapped[float | None] = mapped_column(Numeric(7, 1))
    hr_avg: Mapped[int | None] = mapped_column(SmallInteger)
    hr_max: Mapped[int | None] = mapped_column(SmallInteger)
    hr_samples: Mapped[list | None] = mapped_column(JSONB)
    gps_polyline: Mapped[str | None] = mapped_column(Text)
    gps_samples: Mapped[list | None] = mapped_column(JSONB)
    elevation_gain_m: Mapped[float | None] = mapped_column(Numeric(6, 1))
    temperature_c: Mapped[float | None] = mapped_column(Numeric(4, 1))
    status: Mapped[ActivityStatus] = mapped_column(
        _enum(ActivityStatus, "activity_status"), default=ActivityStatus.pending
    )
    cheat_score: Mapped[int] = mapped_column(SmallInteger, default=0)
    cheat_flags: Mapped[list] = mapped_column(JSONB, default=list)
    exp_awarded: Mapped[float | None] = mapped_column(Numeric(10, 2))
    zone_seconds: Mapped[dict | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Monster(Base):
    __tablename__ = "monsters"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(Text)
    species_code: Mapped[str] = mapped_column(Text, default="runmon_baby")
    generation: Mapped[int] = mapped_column(SmallInteger, default=1)
    level: Mapped[int] = mapped_column(SmallInteger, default=1)
    exp: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    stamina: Mapped[float] = mapped_column(Numeric(8, 2), default=10)
    agility: Mapped[float] = mapped_column(Numeric(8, 2), default=10)
    attack: Mapped[float] = mapped_column(Numeric(8, 2), default=10)
    defense: Mapped[float] = mapped_column(Numeric(8, 2), default=10)
    heart_points: Mapped[float] = mapped_column(Numeric(8, 2), default=100)
    evolution_line: Mapped[EvolutionLine] = mapped_column(
        _enum(EvolutionLine, "evolution_line"), default=EvolutionLine.balanced
    )
    evolution_gauge: Mapped[float] = mapped_column(Numeric(6, 2), default=0)
    stamina_points: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    speed_points: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    condition_score: Mapped[int] = mapped_column(SmallInteger, default=70)
    animation_state: Mapped[MonsterAnim] = mapped_column(
        _enum(MonsterAnim, "monster_anim"), default=MonsterAnim.idle
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped[User] = relationship(back_populates="monsters")
    effects: Mapped[list["MonsterEffect"]] = relationship(back_populates="monster")


class ExpLedger(Base):
    __tablename__ = "exp_ledger"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    monster_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("monsters.id", ondelete="CASCADE"))
    activity_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("wearable_activities.id", ondelete="SET NULL")
    )
    idempotency_key: Mapped[str] = mapped_column(Text, unique=True)
    exp_delta: Mapped[float] = mapped_column(Numeric(10, 2))
    stamina_delta: Mapped[float] = mapped_column(Numeric(8, 2), default=0)
    speed_delta: Mapped[float] = mapped_column(Numeric(8, 2), default=0)
    reason: Mapped[str] = mapped_column(Text)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class MonsterEffect(Base):
    __tablename__ = "monster_effects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    monster_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("monsters.id", ondelete="CASCADE"))
    kind: Mapped[EffectKind] = mapped_column(_enum(EffectKind, "effect_kind"))
    code: Mapped[str] = mapped_column(Text)
    exp_multiplier: Mapped[float] = mapped_column(Numeric(4, 2), default=1.0)
    stat_modifiers: Mapped[dict] = mapped_column(JSONB, default=dict)
    granted_by: Mapped[str] = mapped_column(Text)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    monster: Mapped[Monster] = relationship(back_populates="effects")


class EvolutionHistory(Base):
    __tablename__ = "evolution_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    monster_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("monsters.id", ondelete="CASCADE"))
    from_species: Mapped[str] = mapped_column(Text)
    to_species: Mapped[str] = mapped_column(Text)
    line: Mapped[EvolutionLine] = mapped_column(_enum(EvolutionLine, "evolution_line"))
    stamina_points: Mapped[float] = mapped_column(Numeric(10, 2))
    speed_points: Mapped[float] = mapped_column(Numeric(10, 2))
    evolved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class NutritionLog(Base):
    __tablename__ = "nutrition_logs"
    __table_args__ = (UniqueConstraint("user_id", "log_date", "source"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    log_date: Mapped[date] = mapped_column(Date)
    source: Mapped[str] = mapped_column(Text, default="manual")
    calories_in: Mapped[float] = mapped_column(Numeric(7, 1))
    protein_g: Mapped[float] = mapped_column(Numeric(6, 1), default=0)
    fat_g: Mapped[float] = mapped_column(Numeric(6, 1), default=0)
    carbs_g: Mapped[float] = mapped_column(Numeric(6, 1), default=0)
    meals: Mapped[list] = mapped_column(JSONB, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class DailyConditionSnapshot(Base):
    __tablename__ = "daily_condition_snapshots"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    snapshot_date: Mapped[date] = mapped_column(Date, primary_key=True)
    energy_balance_kcal: Mapped[float] = mapped_column(Numeric(7, 1))
    pfc_score: Mapped[int] = mapped_column(SmallInteger)
    condition_score: Mapped[int] = mapped_column(SmallInteger)
    effects_applied: Mapped[list] = mapped_column(JSONB, default=list)
