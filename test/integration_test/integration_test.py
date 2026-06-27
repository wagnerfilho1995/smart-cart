def test_200_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200


def test_200_compare_products(client):
    response = client.post(
        "/products/compare",
        json={
            "items": [
                {
                    "name": "Leite em pó",
                    "brand": "itambe",
                    "price": 14.00,
                    "weight": 300,
                    "unit": "g",
                },
                {
                    "name": "Leite em pó",
                    "brand": "piracanjuba",
                    "price": 12.00,
                    "weight": 200,
                    "unit": "g",
                },
            ]
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "O produto mais vantajoso é Leite em pó (itambe) por R$ 14,00"


def test_200_compare_products_with_quantity(client):
    response = client.post(
        "/products/compare",
        json={
            "items": [
                {
                    "name": "Refrigerante",
                    "brand": "Coca-Cola",
                    "price": 25.00,
                    "quantity": 6,
                    "weight": 250,
                    "unit": "ml",
                },
                {
                    "name": "Refrigerante",
                    "brand": "Coca-Cola",
                    "price": 32.00,
                    "quantity": 12,
                    "weight": 200,
                    "unit": "ml",
                },
            ]
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "O produto mais vantajoso é Refrigerante (Coca-Cola) por R$ 32,00"
