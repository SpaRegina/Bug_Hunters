# Users Tests Improvement
import pytest
import requests
import uuid

BASE_URL_DEV = "https://dev-gs.qa-playground.com/api/v1"
BASE_URL_RELEASE = "https://release-gs.qa-playground.com/api/v1"
AUTH_HEADER = {"Authorization": "Bearer qahack2024:r.g.spaschenko@gmail.com"}

# Users (9 tests)

def test_delete_user():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-1"}
    non_existing_uuid = str(uuid.uuid4())

    response_dev = requests.delete(f"{BASE_URL_DEV}/users/{non_existing_uuid}", headers=headers)
    response_release = requests.delete(f"{BASE_URL_RELEASE}/users/{non_existing_uuid}", headers=headers)

    assert response_dev.status_code == response_release.status_code == 404, "Expected 404 for deleting a non-existent user."

def test_create_user():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-3"}
    user_data = {
        "email": "test.user@example.com",
        "password": "password123",
        "name": "Test User",
        "nickname": "testuser"
    }

    response_dev = requests.post(f"{BASE_URL_DEV}/users", headers=headers, json=user_data)
    response_release = requests.post(f"{BASE_URL_RELEASE}/users", headers=headers, json=user_data)

    assert response_dev.status_code == response_release.status_code == 201, "Expected 201 when creating a new user."

def test_update_user():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-4"}
    user_uuid = str(uuid.uuid4())
    update_data = {"name": "Updated User"}

    response_dev = requests.put(f"{BASE_URL_DEV}/users/{user_uuid}", headers=headers, json=update_data)
    response_release = requests.put(f"{BASE_URL_RELEASE}/users/{user_uuid}", headers=headers, json=update_data)

    assert response_dev.status_code == response_release.status_code == 400, "Expected 400 when updating a non-existent user."

def test_list_users():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-6"}

    response_dev = requests.get(f"{BASE_URL_DEV}/users", headers=headers)
    response_release = requests.get(f"{BASE_URL_RELEASE}/users", headers=headers)

    assert response_dev.status_code == response_release.status_code == 200, "Expected successful response for listing users."

    users_dev = response_dev.json()
    users_release = response_release.json()

    assert isinstance(users_dev, list) and isinstance(users_release, list), "Expected list of users."
    assert users_dev and users_release, "User lists should not be empty."
    assert users_dev == users_release, "User lists in DEV and RELEASE environments do not match."

def test_get_user_by_email_and_password():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-7"}
    params = {"email": "nonexistent.user@example.com", "password": "password123"}

    response_dev = requests.get(f"{BASE_URL_DEV}/users", headers=headers, params=params)
    response_release = requests.get(f"{BASE_URL_RELEASE}/users", headers=headers, params=params)

    assert response_dev.status_code == response_release.status_code == 404, "Expected 404 for non-existent user."

def test_get_user_activity():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-21"}
    user_uuid = str(uuid.uuid4())

    response_dev = requests.get(f"{BASE_URL_DEV}/users/{user_uuid}/activity", headers=headers)
    response_release = requests.get(f"{BASE_URL_RELEASE}/users/{user_uuid}/activity", headers=headers)

    assert response_dev.status_code == response_release.status_code == 404, "Expected 404 for non-existent user activity."

def test_create_user_alternate():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-22"}
    user_data = {
        "email": "alternate.user@example.com",
        "password": "password123",
        "name": "Alternate User",
        "nickname": "altuser"
    }

    response_dev = requests.post(f"{BASE_URL_DEV}/users", headers=headers, json=user_data)
    response_release = requests.post(f"{BASE_URL_RELEASE}/users", headers=headers, json=user_data)

    assert response_dev.status_code == response_release.status_code == 201, "Expected 201 when creating a user through alternate API."

def test_get_user_info():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-23"}
    user_uuid = str(uuid.uuid4())

    response_dev = requests.get(f"{BASE_URL_DEV}/users/{user_uuid}", headers=headers)
    response_release = requests.get(f"{BASE_URL_RELEASE}/users/{user_uuid}", headers=headers)

    assert response_dev.status_code == response_release.status_code == 404, "Expected 404 for non-existent user information."

def test_update_user_invalid_uuid():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-24"}
    invalid_uuid = "invalid-uuid"
    update_data = {"name": "Invalid UUID"}

    response_dev = requests.put(f"{BASE_URL_DEV}/users/{invalid_uuid}", headers=headers, json=update_data)
    response_release = requests.put(f"{BASE_URL_RELEASE}/users/{invalid_uuid}", headers=headers, json=update_data)

    assert response_dev.status_code == response_release.status_code == 400, "Expected 400 for invalid UUID."

# Wishlist (3 tests)

def test_add_to_wishlist():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-5"}
    user_uuid = str(uuid.uuid4())
    item_data = {"item_name": "Wishlist Item"}

    response_dev = requests.post(f"{BASE_URL_DEV}/users/{user_uuid}/wishlist", headers=headers, json=item_data)
    response_release = requests.post(f"{BASE_URL_RELEASE}/users/{user_uuid}/wishlist", headers=headers, json=item_data)

    assert response_dev.status_code == response_release.status_code == 201, "Expected 201 when adding an item to the wishlist."

def test_remove_from_wishlist():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-8"}
    user_uuid = str(uuid.uuid4())
    item_data = {"item_name": "Test Item"}

    response_add_dev = requests.post(f"{BASE_URL_DEV}/users/{user_uuid}/wishlist", headers=headers, json=item_data)
    response_add_release = requests.post(f"{BASE_URL_RELEASE}/users/{user_uuid}/wishlist", headers=headers, json=item_data)

    assert response_add_dev.status_code == response_add_release.status_code == 201, "Expected 201 when adding an item to the wishlist."

    item_id_dev = response_add_dev.json().get("item_id")
    item_id_release = response_add_release.json().get("item_id")

    assert item_id_dev and item_id_release, "API did not return item ID for added item."

    response_remove_dev = requests.delete(f"{BASE_URL_DEV}/users/{user_uuid}/wishlist/{item_id_dev}", headers=headers)
    response_remove_release = requests.delete(f"{BASE_URL_RELEASE}/users/{user_uuid}/wishlist/{item_id_release}", headers=headers)

    assert response_remove_dev.status_code == response_remove_release.status_code == 200, "Expected 200 when removing an item from the wishlist."

def test_duplicate_item_in_wishlist():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-25"}
    user_uuid = str(uuid.uuid4())
    item_data = {"item_name": "Duplicate Item"}

    response_first_dev = requests.post(f"{BASE_URL_DEV}/users/{user_uuid}/wishlist", headers=headers, json=item_data)
    response_first_release = requests.post(f"{BASE_URL_RELEASE}/users/{user_uuid}/wishlist", headers=headers, json=item_data)

    assert response_first_dev.status_code == response_first_release.status_code == 201, "Expected 201 when adding an item to the wishlist."

    response_second_dev = requests.post(f"{BASE_URL_DEV}/users/{user_uuid}/wishlist", headers=headers, json=item_data)
    response_second_release = requests.post(f"{BASE_URL_RELEASE}/users/{user_uuid}/wishlist", headers=headers, json=item_data)

    assert response_second_dev.status_code == response_second_release.status_code == 409, "Expected 409 when adding a duplicate item to the wishlist."

## Games (2 tests)

def test_search_games():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-2"}
    search_query = "test_game"

    response_dev = requests.get(f"{BASE_URL_DEV}/games/search", headers=headers, params={"query": search_query})
    response_release = requests.get(f"{BASE_URL_RELEASE}/games/search", headers=headers, params={"query": search_query})

    assert response_dev.status_code == response_release.status_code == 200, "Expected successful response for game search."

    games_dev = response_dev.json()
    games_release = response_release.json()

    assert games_dev and games_release, "Search results should not be empty."
    assert games_dev == games_release, "Search results in DEV and RELEASE environments do not match."

def test_get_game_info():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-9"}
    game_data = {"name": "Test Game"}

    response_create_dev = requests.post(f"{BASE_URL_DEV}/games", headers=headers, json=game_data)
    response_create_release = requests.post(f"{BASE_URL_RELEASE}/games", headers=headers, json=game_data)

    game_id_dev = response_create_dev.json().get("game_id")
    game_id_release = response_create_release.json().get("game_id")

    assert game_id_dev and game_id_release, "Game was not created."

    response_dev = requests.get(f"{BASE_URL_DEV}/games/{game_id_dev}", headers=headers)
    response_release = requests.get(f"{BASE_URL_RELEASE}/games/{game_id_release}", headers=headers)

    assert response_dev.status_code == response_release.status_code == 200, "Expected successful response for game information retrieval."

    game_dev = response_dev.json()
    game_release = response_release.json()

    assert game_dev == game_release, "Game information in DEV and RELEASE environments do not match."

# Categories (1 test)

def test_get_categories():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-10"}

    response_dev = requests.get(f"{BASE_URL_DEV}/categories", headers=headers)
    response_release = requests.get(f"{BASE_URL_RELEASE}/categories", headers=headers)

    assert response_dev.status_code == response_release.status_code == 200, "Expected successful response for getting categories."

    categories_dev = response_dev.json()
    categories_release = response_release.json()

    assert categories_dev and categories_release, "Category list should not be empty."
    assert categories_dev == categories_release, "Category lists in DEV and RELEASE environments do not match."

    category_ids = set()
    for category in categories_dev:
        assert "category_id" in category and "name" in category, "Invalid category data structure."
        assert category["category_id"] not in category_ids, "Duplicate category found in the list."
        category_ids.add(category["category_id"])


# Avatar (1 test)

def test_upload_avatar():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-11"}
    user_uuid = str(uuid.uuid4())
    files = {"avatar": ("avatar.png", b"test_avatar_content", "image/png")}

    response_dev = requests.post(f"{BASE_URL_DEV}/users/{user_uuid}/avatar", headers=headers, files=files)
    response_release = requests.post(f"{BASE_URL_RELEASE}/users/{user_uuid}/avatar", headers=headers, files=files)

    assert response_dev.status_code == response_release.status_code == 201, "Expected 201 when uploading an avatar."

    avatar_url_dev = response_dev.json().get("avatar_url")
    avatar_url_release = response_release.json().get("avatar_url")

    assert avatar_url_dev and avatar_url_release, "Avatar URL should be returned after successful upload."
    assert avatar_url_dev == avatar_url_release, "Avatar URLs in DEV and RELEASE environments do not match."

# Cart (4 tests)

def test_get_cart():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-12"}
    user_uuid = str(uuid.uuid4())

    response_dev = requests.get(f"{BASE_URL_DEV}/users/{user_uuid}/cart", headers=headers)
    response_release = requests.get(f"{BASE_URL_RELEASE}/users/{user_uuid}/cart", headers=headers)

    assert response_dev.status_code == response_release.status_code == 200, "Expected 200 when getting the cart."

def test_add_item_to_cart():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-13"}
    user_uuid = str(uuid.uuid4())
    item_data = {"item_uuid": str(uuid.uuid4()), "quantity": 1}

    response_dev = requests.post(f"{BASE_URL_DEV}/users/{user_uuid}/cart", headers=headers, json=item_data)
    response_release = requests.post(f"{BASE_URL_RELEASE}/users/{user_uuid}/cart", headers=headers, json=item_data)

    assert response_dev.status_code == response_release.status_code == 201, "Expected 201 when adding an item to the cart."

def test_remove_item_from_cart():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-14"}
    user_uuid = str(uuid.uuid4())
    item_uuid = str(uuid.uuid4())

    response_dev = requests.delete(f"{BASE_URL_DEV}/users/{user_uuid}/cart/{item_uuid}", headers=headers)
    response_release = requests.delete(f"{BASE_URL_RELEASE}/users/{user_uuid}/cart/{item_uuid}", headers=headers)

    assert response_dev.status_code == response_release.status_code == 404, "Expected 404 when removing a non-existent item from the cart."

def test_clear_cart():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-15"}
    user_uuid = str(uuid.uuid4())

    response_dev = requests.post(f"{BASE_URL_DEV}/users/{user_uuid}/cart/clear", headers=headers)
    response_release = requests.post(f"{BASE_URL_RELEASE}/users/{user_uuid}/cart/clear", headers=headers)

    assert response_dev.status_code == response_release.status_code == 200, "Expected 200 when clearing the cart."

# Orders (3 tests)

def test_create_order():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-16"}
    user_uuid = str(uuid.uuid4())
    order_data = {"items": [{"item_uuid": str(uuid.uuid4()), "quantity": 1}]}

    response_dev = requests.post(f"{BASE_URL_DEV}/users/{user_uuid}/orders", headers=headers, json=order_data)
    response_release = requests.post(f"{BASE_URL_RELEASE}/users/{user_uuid}/orders", headers=headers, json=order_data)

    assert response_dev.status_code == response_release.status_code == 201, "Expected 201 when creating a new order."

def test_get_orders():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-17"}
    user_uuid = str(uuid.uuid4())

    response_dev = requests.get(f"{BASE_URL_DEV}/users/{user_uuid}/orders", headers=headers)
    response_release = requests.get(f"{BASE_URL_RELEASE}/users/{user_uuid}/orders", headers=headers)

    assert response_dev.status_code == response_release.status_code == 200, "Expected 200 when retrieving user orders."

def test_update_order_status():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-18"}
    order_uuid = str(uuid.uuid4())
    status_data = {"status": "completed"}

    response_dev = requests.patch(f"{BASE_URL_DEV}/orders/{order_uuid}/status", headers=headers, json=status_data)
    response_release = requests.patch(f"{BASE_URL_RELEASE}/orders/{order_uuid}/status", headers=headers, json=status_data)

    assert response_dev.status_code == response_release.status_code == 404, "Expected 404 when updating the status of a non-existent order."

# Payments (2 tests)

def test_create_payment():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-19"}
    user_uuid = str(uuid.uuid4())
    payment_data = {"order_uuid": str(uuid.uuid4()), "payment_method": "card"}

    response_dev = requests.post(f"{BASE_URL_DEV}/users/{user_uuid}/payments", headers=headers, json=payment_data)
    response_release = requests.post(f"{BASE_URL_RELEASE}/users/{user_uuid}/payments", headers=headers, json=payment_data)

    assert response_dev.status_code == response_release.status_code == 201, "Expected 201 when creating a new payment."

def test_get_payments():
    headers = {**AUTH_HEADER, "X-Task-Id": "api-20"}
    user_uuid = str(uuid.uuid4())

    response_dev = requests.get(f"{BASE_URL_DEV}/users/{user_uuid}/payments", headers=headers)
    response_release = requests.get(f"{BASE_URL_RELEASE}/users/{user_uuid}/payments", headers=headers)

    assert response_dev.status_code == response_release.status_code == 200, "Expected 200 when retrieving user payments."


