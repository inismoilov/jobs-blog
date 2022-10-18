import json

from fastapi import status


def test_create_job(client, normal_user_token_headers):
    data = {
        "title": "SDE super",
        "company": "doogle",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "python",
        "date_posted": "2022-03-20"
        }
    response = client.post(
        "/jobs/create-job/",
        json.dumps(data),
        headers=normal_user_token_headers
    )
    assert response.status_code == 200
    assert response.json()["company"] == "doogle"
    assert response.json()["description"] == "python"


def test_read_job(client, normal_user_token_headers):
    data = {
        "title": "SDE super",
        "company": "doogle",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "python",
        "date_posted": "2022-03-20"
        }
    response = client.post(
        "/jobs/create-job/",
        json.dumps(data),
        headers=normal_user_token_headers
    )

    response = client.get("/jobs/get/1/")
    assert response.status_code == 200
    assert response.json()['title'] == "SDE super"


# def test_job_not_found(client):
#     response = client.get("/jobs/get/12/")
#     assert response.status_code == 404
#     assert response.json()['detail'] == "Job with this id 2 does not exist"


def test_read_all_jobs(client):
    data = {
       "title": "SDE super",
       "company": "doogle",
       "company_url": "www.doogle.com",
       "location": "USA,NY",
       "description": "python",
       "date_posted": "2022-10-17"
    }
    client.post("/jobs/create-job/", json.dumps(data))
    client.post("/jobs/create-job/", json.dumps(data))

    response = client.get("/jobs/all/")
    assert response.status_code == 200
    assert response.json()[0]
    assert response.json()[1]


def test_update_a_job(client, normal_user_token_headers):
    data = {
        "title": "New Job super",
        "company": "doogle",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "fastapi",
        "date_posted": "2022-03-20",
    }
    client.post("/jobs/create-job/", json.dumps(data), headers=normal_user_token_headers)
    data["title"] = "test new title"

    response = client.put(
        "/jobs/update/1",
        json.dumps(data),
        headers=normal_user_token_headers
        )

    assert response.json()["msg"] == "Successfully updated data."


def test_delete_a_job(client, normal_user_token_headers):
    data = {
        "title": "New Job super",
        "company": "doogle",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "fastapi",
        "date_posted": "2022-03-20"
    }
    client.post("/jobs/create-job/", json.dumps(data), normal_user_token_headers)
    msg = client.delete("/jobs/delete/1", headers=normal_user_token_headers)
    response = client.get("/jobs/get/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
