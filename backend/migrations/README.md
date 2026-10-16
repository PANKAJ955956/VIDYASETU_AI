# Alembic migrations

The MVP creates tables automatically for first-run simplicity. Alembic is included so production schema changes can be migrated safely.

Initialize a real migration history with:

```bash
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```
