from app.models.material import Material

def list_materials(db, page=1, page_size=50):
    query = db.query(Material)
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

