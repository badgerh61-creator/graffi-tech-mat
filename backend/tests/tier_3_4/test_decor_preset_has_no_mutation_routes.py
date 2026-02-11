def test_decor_preset_has_no_mutation_routes(client):
    routes = [route.path for route in client.app.routes]

    assert "/decor-presets/" in routes
    assert "/decor-presets/create" not in routes
    assert "/decor-presets/delete" not in routes

