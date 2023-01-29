from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "department" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL,
    "description" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "job" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL,
    "department_id_id" INT NOT NULL REFERENCES "department" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "collaborator" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL,
    "last_name" VARCHAR(64) NOT NULL,
    "gender" VARCHAR(6) NOT NULL,
    "age" INT NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "job_id_id" INT NOT NULL REFERENCES "job" ("id") ON DELETE RESTRICT
);
COMMENT ON COLUMN "collaborator"."gender" IS 'MALE: MALE\nFEMALE: FEMALE';
CREATE TABLE IF NOT EXISTS "project" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL,
    "description" TEXT NOT NULL,
    "customer" VARCHAR(64) NOT NULL,
    "start_date" DATE NOT NULL,
    "final_date" DATE NOT NULL
);
CREATE TABLE IF NOT EXISTS "assignment" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL,
    "start_date" DATE NOT NULL,
    "final_date" DATE NOT NULL,
    "project_id_id" INT NOT NULL REFERENCES "project" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(64) NOT NULL,
    "password" VARCHAR(128) NOT NULL,
    "email" VARCHAR(256) NOT NULL,
    "role" VARCHAR(7) NOT NULL,
    "department_id_id" INT NOT NULL REFERENCES "department" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "user"."role" IS 'C_LEVEL: C-LEVEL\nLEADER: LEADER';
CREATE TABLE IF NOT EXISTS "announcement" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL,
    "description" TEXT NOT NULL,
    "date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "assignment_collaborator" (
    "assignment_id" INT NOT NULL REFERENCES "assignment" ("id") ON DELETE CASCADE,
    "collaborator_id" INT NOT NULL REFERENCES "collaborator" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
