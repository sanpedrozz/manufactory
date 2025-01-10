from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from shared.config.config import settings
from shared.db.manufactory.models import *  # noqa

# Конфигурация Alembic
config = context.config

# Подключаем файл логирования (если настроен в alembic.ini)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Устанавливаем строку подключения из Settings
config.set_main_option("sqlalchemy.url", f"{settings.manufactory_db_url_async}?async_fallback=True")

# Импортируем модели для автоматической генерации миграций
from shared.db.base import Base

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
