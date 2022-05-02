"""Add errata support

Revision ID: cd8a664d68a8
Revises: 433fd427f579
Create Date: 2022-05-02 16:32:38.770397

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "cd8a664d68a8"
down_revision = "433fd427f579"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "errata_records",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("platform_id", sa.Integer(), nullable=False),
        sa.Column("issued_date", sa.DateTime(), nullable=False),
        sa.Column("updated_date", sa.DateTime(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("original_description", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("original_title", sa.Text(), nullable=False),
        sa.Column("contact_mail", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("version", sa.Text(), nullable=False),
        sa.Column("type", sa.Text(), nullable=False),
        sa.Column("severity", sa.Text(), nullable=False),
        sa.Column("solution", sa.Text(), nullable=False),
        sa.Column("release", sa.Text(), nullable=False),
        sa.Column("rights", sa.Text(), nullable=False),
        sa.Column("reboot_suggested", sa.Boolean(), nullable=False),
        sa.Column("pushcount", sa.Text(), nullable=False),
        sa.Column("collection_name", sa.Text(), nullable=False),
        sa.Column("short_collection_name", sa.Text(), nullable=False),
        sa.Column("definition_id", sa.Integer(), nullable=False),
        sa.Column("definition_version", sa.Integer(), nullable=False),
        sa.Column("definition_class", sa.Text(), nullable=False),
        sa.Column(
            "affected_cpe", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["platform_id"],
            ["platforms.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "errata_module",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("errata_record_id", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("version", sa.Text(), nullable=False),
        sa.Column("stream", sa.Text(), nullable=False),
        sa.Column("context", sa.Text(), nullable=False),
        sa.Column("arch", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["errata_record_id"],
            ["errata_records.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "errata_packages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("errata_record_id", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("version", sa.Text(), nullable=False),
        sa.Column("release", sa.Text(), nullable=False),
        sa.Column("epoch", sa.Integer(), nullable=False),
        sa.Column("arch", sa.Text(), nullable=False),
        sa.Column("filename", sa.Text(), nullable=False),
        sa.Column("reboot_suggested", sa.Boolean(), nullable=False),
        sa.Column("relogin_suggested", sa.Boolean(), nullable=False),
        sa.Column("restart_suggested", sa.Boolean(), nullable=False),
        sa.Column("src_rpm", sa.Text(), nullable=False),
        sa.Column("checksum", sa.Text(), nullable=False),
        sa.Column("checksum_type", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["errata_record_id"],
            ["errata_records.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "errata_references",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("href", sa.Text(), nullable=False),
        sa.Column("ref_id", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("errata_record_id", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["errata_record_id"],
            ["errata_records.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "errata_cves",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("reference_id", sa.Integer(), nullable=False),
        sa.Column("cvss3", sa.Text(), nullable=False),
        sa.Column("cwe", sa.Text(), nullable=False),
        sa.Column("impact", sa.Text(), nullable=False),
        sa.Column("public", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["reference_id"],
            ["errata_references.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("errata_cves")
    op.drop_table("errata_references")
    op.drop_table("errata_packages")
    op.drop_table("errata_module")
    op.drop_table("errata_records")
    # ### end Alembic commands ###
