#
# Copyright (C) 2025 Spotify
#
# Release: 0.0
# @link
#

__author__ = "tan.le"
__date__ = "Oct 26, 2022"

from django.conf import settings
from django.db.backends.mysql.base import DatabaseWrapper as MySqlDatabaseWrapper
from django.db.backends.mysql.schema import DatabaseSchemaEditor as MySqlDatabaseSchemaEditor

from ai_api.constants.system import WebSystem

if settings.SYSTEM_ID in [
    WebSystem.STG,
    WebSystem.LOCALHOST
]:
    INPLACE_POSTFIX = ", ALGORITHM = COPY, LOCK = SHARED"
else:
    INPLACE_POSTFIX = ", ALGORITHM = INPLACE, LOCK = NONE"

DISALLOW_ALTER_TABLES = (

)

# Customize MySql DB Backend for no-down-time migrations
class DatabaseSchemaEditor(MySqlDatabaseSchemaEditor):

    """
    This class made for auto append "ALGORITHM = INPLACE, LOCK = NONE" to the sqls which run by django migration
    https://dev.mysql.com/doc/refman/5.6/en/innodb-online-ddl.html

    These sql can be found at either:
        - Base Schema Editor: <env_dir>/lib/python3.6/site-packages/django/db/backends/schema.py
        - MySql Schema Editor (extends Base Schema Editor): <env_dir>/lib/python3.6/site-packages/django/db/backends/mysql/schema.py

    NOTES:
        - Changing column type does not allow INPLACE https://dev.mysql.com/doc/refman/5.6/en/innodb-online-ddl-operations.html#online-ddl-column-operations
            --> No solution found for changing column type yet
        - Adding FK does not allow INPLACE with foreign_key_checks=True (default) https://dev.mysql.com/doc/refman/5.6/en/innodb-online-ddl-operations.html#online-ddl-foreign-key-syntax-notes
            --> Override `add_field()` and disable foreign_key_checks as bellow
        - Show sqls executed by a migration `sqlmigrate ai_api 1059_auto_20200612_0927`
    """

    def _remove_inplace_suffix(self, sql):
        return sql.replace(INPLACE_POSTFIX, "")

    def add_fields(self, model, field):
        self.execute("SET FOREIGN_KEY_CHECKS=0;")
        super().add_field(model, field)
        self.execute("SET FOREIGN_KEY_CHECKS=1;")

    def _rename_field_sql(self, table, old_field, new_field, new_type):
        sql = super()._rename_field_sql(table, old_field, new_field, new_type)

        old_db_params = old_field.db_parameters(connection=self.connection)
        old_type = old_db_params["type"]
        if old_type != new_type:
            # If renaming field including changing type, we don't apply INPLACE
            sql = self._remove_inplace_suffix(sql)

        return sql

    def remove_field(self, model, field):
        # from ai_system.services.application_log import AppLog

        """
        DON'T allow delete column to avoid downtime during migration
        """
        print(f"MIGRATION SKIPPED - Skip removing field {field} to avoid downtime during migration")
        # AppLog.project.warn(f"Skip removing field {field} to avoid downtime during migration", "MIGRATION SKIPPED")

    def alter_field(self, model, old_field, new_field, strict=False):
        # from ai_system.services.application_log import AppLog

        old_db_params = old_field.db_parameters(connection=self.connection)
        old_type = old_db_params["type"]
        new_db_params = new_field.db_parameters(connection=self.connection)
        new_type = new_db_params["type"]

        if old_type != new_type:
            is_extending_varchar = (
                old_type
                and old_type.lower().startswith("varchar")
                and new_type
                and new_type.lower().startswith("varchar")
            )
            is_extending_varchar = False # temporary disable INPLACE mode for extending varchar
            if is_extending_varchar:
                # Support INPLACE for extending varchar
                self.sql_alter_column_type = f"{self.sql_alter_column_type}{INPLACE_POSTFIX}"
            else:
                if model._meta.db_table.lower() in DISALLOW_ALTER_TABLES:
                    # AppLog.project.error(
                    #     f"Skip changing field `{old_field.column}` type to avoid downtime during migration",
                    #     "MIGRATION SKIPPED",
                    # )
                    raise Exception(
                        f"MIGRATION SKIPPED - Skip changing field `{old_field.column}` type to avoid downtime during migration"
                    )

        # Reject rename field
        if old_field.column != new_field.column:
            # AppLog.project.error(
            #     f"Skip rename field `{old_field.column}` type to avoid downtime during migration",
            #     "MIGRATION SKIPPED",
            # )
            raise Exception(f"MIGRATION SKIPPED - Skip changing field `{old_field.column}` to `{new_field.column}`")

        ret = super().alter_field(model, old_field, new_field, strict)
        self.sql_alter_column_type = self._remove_inplace_suffix(self.sql_alter_column_type)
        return ret

    def delete_model(self, model):
        # from ai_system.services.application_log import AppLog
        #
        # AppLog.project.error(
        #     f"Skip delete table `{model._meta.db_table}` type to avoid downtime during migration",
        #     "MIGRATION SKIPPED",
        # )
        raise Exception(f"MIGRATION SKIPPED - Skip delete table `{model._meta.db_table}`")

    def alter_db_table(self, model, old_db_table, new_db_table):
        # from ai_system.services.application_log import AppLog
        #
        # AppLog.project.error(
        #     f"Skip rename table `{old_db_table}` type to avoid downtime during migration",
        #     "MIGRATION SKIPPED",
        # )
        raise Exception(f"MIGRATION SKIPPED - Skip rename `{old_db_table}` to {new_db_table}")


DLL_INPLACE_OPERATION_SQLS = (
    "sql_create_column",
    "sql_rename_column",
    "sql_delete_column",
    "sql_alter_column_null",
    # "sql_alter_column_not_null", This will error if there are existing NULL values
    "sql_alter_column_default",
    "sql_alter_column_no_default",
)

for sql in DLL_INPLACE_OPERATION_SQLS:
    default_sql = getattr(DatabaseSchemaEditor, sql)
    customized_sql = f"{default_sql}{INPLACE_POSTFIX}"
    setattr(DatabaseSchemaEditor, sql, customized_sql)


class DatabaseWrapper(MySqlDatabaseWrapper):
    SchemaEditorClass = DatabaseSchemaEditor
