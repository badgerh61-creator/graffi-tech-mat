def test_filter_presets_by_culture_pack(client, decor_preset):
    response = client.get(
        f"/decor-presets?culture_pack={decor_preset.culture_pack}"
    )

    assert response.status_code == 200

