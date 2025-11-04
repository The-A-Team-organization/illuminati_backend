# README

## Illuminati Backend

The Illuminati Backend is the core server-side application of the multi-service Illuminati System, developed by The A-Team.
It provides RESTful APIs for authentication, record management, voting, backups and user role administration, forming the backbone of the Illuminati ecosystem.

## Overview

The backend is a modular Django REST Framework application designed for scalability, security and maintainability. 
It exposes a well-structured API consumed by the Illuminati Frontend and other microservices such as the email and scheduler services.

Each application module (app) is isolated by domain responsibility (e.g., authentific, records, votes), ensuring a clean separation of concerns.

## Core Technologies

- Python 3.12 with Django 5.x and Django REST Framework
- Liquibase for database versioning and migrations
- JWT for authentication and session handling
- Docker and docker-compose for containerized deployment
- Jenkins for CI/CD automation

## System Architecture

The backend is structured into multiple Django apps under the apps/ directory:

- authentific	→ Handles authentication, registration and login logic.
- entry_password → Manages the initial system entry password for restricted access.
- users →	Manages user profiles, roles, permissions and invitations.
- records	→ CRUD operations for records displayed on the interactive map.
- votes → Implements the internal voting and poll system.
- hall_of_fame → Maintains a list of notable users and there are also rumors that you can contact them.
- snapshot → Provides backup and restore functionality for record data.

## Supporting modules include:

- api/ → global URL routing and pagination.
- core/ → project configuration and environment settings.
- enums/ → predefined roles and rules constants for access control.
- tests/ — structured unit and integration tests for every app.

## Role System

Users have four access levels:

- Architect: Highest rank. Can manage records, invite new members, vote and try to communicate with retired architects.
- GoldenMason: Extended privileges. Can manage records, invite new members, vote.
- SilverMason: Can create and view records, vote.
- Mason (Regular): Basic viewing and participation in votes.


## Main API Endpoints

- /api/authentific/entry/ → Validate entry password for restricted access.
- /api/authentific/login/	→ Authenticate existing users and issue JWT tokens.
- /api/authentific/register/ → Register new users.
- /api/records/all → Retrieve all existing records (paginated).
- /api/records/create → Create a new record with metadata and image.
- /api/records/{id} → Retrieve or modify a specific record.
- /api/votes/... → Handle polls, user votes, and vote results.
- /api/hall_of_fame/... → Manage and display Hall of Fame entries.
- /api/users/invite/ → Send invitation links to new users via email.

## Testing

We use Vitest for automated tests. Test modules follow the application structure: `authentific`, `entry_password`, `records`, `snapshot`, `users`, and `votes`. 
Each test package contains `test_serializers.py`, `test_services.py`, and `test_views.py`. 
Tests cover serialization correctness, core business logic, and API response integrity.

## Security

- All sensitive operations are protected via JWT authentication.
- Passwords are hashed.
- API access is role-restricted using custom permissions.

## Infrastructure Context

Illuminati Backend is part of a multi-service ecosystem managed with Terraform and Docker.

- [illuminati_backend](https://github.com/The-A-Team-organization/illuminati_backend)(This repository)	→ REST API & business logic (Python)
- [illuminati_email_service](https://github.com/The-A-Team-organization/illuminati_email_service)	→ Email delivery and password reset microservice (Go)
- [illuminati_scheduler_service](https://github.com/The-A-Team-organization/illuminati_scheduler_service)	→ Scheduled automation service (Go)
- [illuminati_iac](https://github.com/The-A-Team-organization/illuminati_iac) → Infrastructure (Terraform, Docker)
- [illuminati_frontend](https://github.com/The-A-Team-organization/illuminati_frontend)  →	 the user interface (React)
