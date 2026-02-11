def test_material_bank_has_no_mutation_routes(client):
    routes = [route.path for route in client.app.routes]

    assert "/materials/" in routes
    assert "/materials/create" not in routes
    assert "/materials/update" not in routes


