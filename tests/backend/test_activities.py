def test_root_redirects_to_static_html(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Chess Club" in response.json()


def test_signup_for_activity_success(client):
    email = "test.student@mergington.edu"
    response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}


def test_signup_for_activity_nonexistent_activity(client):
    response = client.post(
        "/activities/Nonexistent%20Club/signup", params={"email": "student@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_for_activity_already_signed_up(client):
    email = "michael@mergington.edu"
    response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_from_activity_success(client):
    email = "michael@mergington.edu"
    response = client.delete("/activities/Chess%20Club/unregister", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}


def test_unregister_from_activity_not_registered(client):
    response = client.delete("/activities/Chess%20Club/unregister", params={"email": "unknown@mergington.edu"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student not registered for this activity"


def test_unregister_from_activity_nonexistent_activity(client):
    response = client.delete(
        "/activities/Nonexistent%20Club/unregister", params={"email": "student@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
