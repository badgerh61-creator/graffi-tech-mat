def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    columns = {col["name"] for col in inspector.get_columns("assets")}

    asset_status = sa.Enum(
        "created",
        "uploading",
        "uploaded",
        "processing",
        "ready",
        "failed",
        name="asset_status",
    )

    # Create enum if missing
    asset_status.create(bind, checkfirst=True)

    if "status" not in columns:
        op.add_column(
            "assets",
            sa.Column(
                "status",
                asset_status,
                nullable=True,  # TEMPORARY
            ),
        )

        # Backfill legacy rows
        op.execute(
            """
            UPDATE assets
            SET status = CASE
                WHEN processing_error IS NOT NULL THEN 'failed'
                ELSE 'ready'
            END
            """
        )

        # Make NOT NULL after backfill
        op.alter_column(
            "assets",
            "status",
            nullable=False,
        )

    if "status_updated_at" not in columns:
        # SQLite-safe: NO DEFAULT here
        op.add_column(
            "assets",
            sa.Column(
                "status_updated_at",
                sa.DateTime(timezone=True),
                nullable=True,
            ),
        )

        # Backfill timestamps
        op.execute(
            """
            UPDATE assets
            SET status_updated_at = CURRENT_TIMESTAMP
            WHERE status_updated_at IS NULL
            """
        )

        # Enforce NOT NULL after backfill
        op.alter_column(
            "assets",
            "status_updated_at",
            nullable=False,
        )

