def test_activity_ordered_newest_first(
    client,
    editor_user,
):
    response = client.get(
        "/dashboard/activity",
        headers=auth(editor_user),
    )

    items = response.json()
    timestamps = [i["created_at"] for i in items]

    assert timestamps == sorted(timestamps, reverse=True)

