from django.db import migrations


def ensure_gps_district_column(apps, schema_editor):
    if schema_editor.connection.vendor != "sqlite":
        return

    table_name = "checkin_gps"
    with schema_editor.connection.cursor() as cursor:
        columns = [
            column.name
            for column in schema_editor.connection.introspection.get_table_description(
                cursor,
                table_name,
            )
        ]

    if "district_id" not in columns:
        schema_editor.execute(
            'ALTER TABLE "checkin_gps" '
            'ADD COLUMN "district_id" integer NULL '
            'REFERENCES "checkin_district" ("id") DEFERRABLE INITIALLY DEFERRED'
        )

    schema_editor.execute(
        'CREATE INDEX IF NOT EXISTS "checkin_gps_district_id_f4b116d5" '
        'ON "checkin_gps" ("district_id")'
    )


class Migration(migrations.Migration):
    dependencies = [
        ("checkin", "0003_auto_20200920_1951"),
    ]

    operations = [
        migrations.RunPython(ensure_gps_district_column, migrations.RunPython.noop),
    ]
