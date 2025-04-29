from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        # Verifica se as colunas já existem antes de adicioná-las
        migrations.RunSQL(
            sql="""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_name='user_login' AND column_name='client_category'
                ) THEN
                    ALTER TABLE user_login ADD COLUMN client_category VARCHAR(10) DEFAULT 'Comum';
                END IF;
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_name='user_login' AND column_name='role'
                ) THEN
                    ALTER TABLE user_login ADD COLUMN role VARCHAR(10) DEFAULT 'Leitor';
                END IF;
            END $$;
            """,
            reverse_sql="""
            ALTER TABLE user_login DROP COLUMN IF EXISTS client_category;
            ALTER TABLE user_login DROP COLUMN IF EXISTS role;
            """
        ),
    ]
