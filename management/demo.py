#!/usr/bin/env python3
"""
Example showing the use of the API to create a new organization along with
new users, buckets, and tasks. This way a new org is ready to go and start
collecting new data.
"""
import argparse
import sys
import yaml

from influxdb_client import (
    AddResourceMemberRequestBody,
    InfluxDBClient,
    OrganizationsService,
    User,
    UsersService,
)
from influxdb_client.rest import ApiException


def find_org(org_api, org_name):
    """Find organization by name, return none if it does not exist."""
    try:
        orgs = org_api.find_organizations(org=org_name)
        return orgs[0]
    except ApiException:
        return None


def find_user(user_api, user_name):
    """Find user by name, return none if it does not exist."""
    try:
        result = user_api.find_users(name=user_name)
        if len(result.users) > 0:
            return result.users[0]
    except ApiException:
        return None


def find_bucket(bucket_api, bucket_name):
    """Find bucket by name, return none if it does not exist."""
    return bucket_api.find_bucket_by_name(bucket_name)


def find_task(task_api, task_name):
    """Find task by name, return none if it does not exist."""
    return task_api.find_tasks(name=task_name)


def create_tasks(client, org, tasks):
    """Create tasks with a cron in a particular org if it does not already exist."""
    task_api = client.tasks_api()
    for task_name, task in tasks.items():
        result = find_task(task_api, task_name)
        if result:
            print(f"task '{task_name}' already exists, skipping")
            continue

        result = task_api.create_task_cron(
            name=task_name, flux=task["flux"], cron=task["cron"], org_id=org.id
        )
        print(f"task '{result.name}' created and added to '{org.name}' sucessfully")


def create_buckets(client, org, buckets):
    """Create buckets if it does not already exist."""
    bucket_api = client.buckets_api()
    for bucket_name in buckets:
        buckets = find_bucket(bucket_api, bucket_name)
        if buckets:
            print(f"bucket '{bucket_name}' already exists, skipping")
            continue

        bucket = bucket_api.create_bucket(bucket_name=bucket_name, org_id=org.id)
        print(f"bucket '{bucket.name}' created and added to '{org.name}' sucessfully")


def create_users(client, org, users):
    """Create users and add to new org if it does not already exist."""
    user_api = client.users_api()
    for user_name in users:
        user = find_user(user_api, user_name)
        if user is not None:
            print(f"user '{user_name}' already exists, skipping")
            continue

        user = user_api.create_user(user_name)

        # set user password
        # user_service = UsersService(api_client=client.api_client)
        # user_service.post_users_id_password(
        #   user_id=user.id, password_reset_body="""{"password": "string"}"""
        # )

        # add user to new organization
        organization_service = OrganizationsService(api_client=client.api_client)
        member_request = AddResourceMemberRequestBody(id=user.id)
        organization_service.post_orgs_id_members(
            org_id=org.id, add_resource_member_request_body=member_request
        )

        print(f"user '{user.name}' created and added to '{org.name}' sucessfully")


def create_org(client, name):
    """Create new organization and add current user to the org."""
    org_api = client.organizations_api()

    org = find_org(org_api, name)
    if org is not None:
        print(f"org '{name}' already exists, skipping")
    else:
        org = org_api.create_organization(name)
        print(f"org '{org.name}' created sucessfully")

    return org


def main():
    """Create a new org."""
    with open("devops.yaml", "r", encoding="utf-8") as file:
        org_data = yaml.safe_load(file)

    with InfluxDBClient.from_config_file("creds.toml") as client:
        org = create_org(client, org_data["name"])

        create_users(client, org, org_data["users"])
        create_buckets(client, org, org_data["buckets"])
        create_tasks(client, org, org_data["tasks"])


if __name__ == "__main__":
    sys.exit(main())
