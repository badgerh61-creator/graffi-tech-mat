from app.models.decor_preset import DecorPreset

def list_decor_presets(db, culture_pack=None, page=1, page_size=50):
    query = db.query(DecorPreset)

    if culture_pack:
        query = query.filter(DecorPreset.culture_pack == culture_pack)

    total = query.count()

    items = (
        query
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "items": items,
        "total": total,
    }

