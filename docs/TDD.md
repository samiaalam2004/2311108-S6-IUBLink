# IUBLink — Technical Design Document (TDD)

## 1. Introduction

### 1.1 Purpose

This document describes the proposed technical architecture, technology stack, database design, REST API structure, authentication mechanism, and authorization strategy for IUBLink.

### 1.2 System Overview

IUBLink will be developed as a client-server web application. The React frontend will communicate with the FastAPI backend through REST APIs. The backend will validate requests, enforce permissions, execute business logic, and interact with the database.

## 2. Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Frontend | React.js | User interface |
| Programming Language | TypeScript | Type-safe frontend development |
| Backend | FastAPI | REST API and business logic |
| Backend Language | Python | Server-side implementation |
| Database | PostgreSQL | Persistent data storage |
| Authentication | JWT | Authenticated API access |
| Password Security | Argon2 or bcrypt | Secure password hashing |
| API Documentation | FastAPI OpenAPI/Swagger | API inspection and testing |
| Version Control | Git and GitHub | Source control and collaboration |

## 3. System Architecture

The application will follow a layered client-server architecture.

```text
+----------------------------------+
|       React + TypeScript         |
|  Pages, Forms, Dashboards        |
+----------------------------------+
                |
                | HTTP / REST API
                | JWT Bearer Token
                v
+----------------------------------+
|          FastAPI Backend         |
|                                  |
|  Authentication and Validation   |
|  Role and Permission Checks      |
|  Business Logic                  |
|  API Routes                      |
+----------------------------------+
                |
                v
+----------------------------------+
|         PostgreSQL               |
|                                  |
|  Users and Profiles              |
|  Connections and Mentorship      |
|  Opportunities and Events        |
+----------------------------------+
```

## 4. Frontend Design

The frontend will be divided into reusable components, pages, and service modules.

### 4.1 Main Pages

- Login and Registration
- Student Dashboard
- Alumni Dashboard
- Faculty Dashboard
- Admin Dashboard
- User Profile
- Alumni Directory
- Connection Requests
- Mentorship Requests
- Opportunities
- Events

### 4.2 Frontend Responsibilities

- Display data received from REST APIs.
- Collect and validate user input.
- Maintain authentication state.
- Display role-specific navigation and actions.
- Show success messages and error responses.
- Send authenticated requests to protected API endpoints.

The frontend shall not be responsible for enforcing security independently. All sensitive authorization checks must be performed by the backend.

## 5. Backend Design

The backend will use FastAPI to provide modular REST API endpoints.

### 5.1 Main Backend Modules

- `auth`: registration, login, and token handling.
- `users`: user accounts and profile management.
- `alumni`: alumni directory and verification.
- `connections`: connection request management.
- `mentorship`: mentorship request management.
- `opportunities`: job and internship posts.
- `events`: event management and registration.
- `admin`: user administration and content moderation.

### 5.2 Backend Responsibilities

- Validate incoming requests.
- Authenticate users.
- Check roles and permission scopes.
- Enforce ownership rules for user-specific resources.
- Execute application business logic.
- Read and write database records.
- Return appropriate HTTP responses.

## 6. Database Design

The application will use PostgreSQL as its relational database.

### 6.1 Proposed Tables

#### Users
- `id`: Primary key
- `name`: User's name
- `email`: Unique email address
- `password_hash`: Hashed password
- `role`: Student, Alumni, Faculty, or Admin
- `is_active`: Account status
- `created_at`: Account creation time

#### Profiles
- `id`: Primary key
- `user_id`: Foreign key referencing Users
- `department`: Department information
- `graduation_year`: Graduation year, when applicable
- `company`: Current company, when applicable
- `industry`: Professional industry
- `bio`: Short profile description
- `verification_status`: Alumni verification status, where applicable

#### ConnectionRequests
- `id`: Primary key
- `sender_id`: Foreign key referencing Users
- `receiver_id`: Foreign key referencing Users
- `status`: Pending, Accepted, or Rejected
- `created_at`: Request creation time

#### MentorshipRequests
- `id`: Primary key
- `student_id`: Foreign key referencing Users
- `alumni_id`: Foreign key referencing Users
- `message`: Request message
- `status`: Pending, Accepted, or Rejected
- `created_at`: Request creation time

#### Opportunities
- `id`: Primary key
- `created_by`: Foreign key referencing Users
- `title`: Opportunity title
- `description`: Opportunity details
- `company`: Company or organization
- `opportunity_type`: Job or Internship
- `deadline`: Application deadline
- `created_at`: Creation time

#### Events
- `id`: Primary key
- `created_by`: Foreign key referencing Users
- `title`: Event title
- `description`: Event details
- `event_date`: Scheduled date
- `location`: Event location

#### EventRegistrations
- `id`: Primary key
- `event_id`: Foreign key referencing Events
- `user_id`: Foreign key referencing Users
- `registered_at`: Registration time

### 6.2 Relationships

- One user may have one profile.
- A user may send or receive multiple connection requests.
- A student may submit multiple mentorship requests.
- An alumnus may create multiple opportunities.
- A faculty member or administrator may create multiple events.
- Users may register for multiple events.

## 7. REST API Design

### 7.1 Authentication

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/register` | Register a user |
| POST | `/api/auth/login` | Authenticate a user |
| GET | `/api/auth/me` | Retrieve the current user's information |

### 7.2 Profiles and Alumni

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/profiles/me` | View own profile |
| PUT | `/api/profiles/me` | Update own profile |
| GET | `/api/alumni` | Search alumni |
| GET | `/api/alumni/{id}` | View an alumni profile |
| PATCH | `/api/admin/alumni/{id}/verify` | Verify an alumnus |

### 7.3 Connections

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/connections` | Send a connection request |
| GET | `/api/connections` | View own connections and requests |
| PATCH | `/api/connections/{id}` | Accept or reject a request |

### 7.4 Mentorship

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/mentorship` | Submit a mentorship request |
| GET | `/api/mentorship` | View authorized requests |
| PATCH | `/api/mentorship/{id}` | Update request status |

### 7.5 Opportunities

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/opportunities` | Create an opportunity |
| GET | `/api/opportunities` | Browse opportunities |
| GET | `/api/opportunities/{id}` | View an opportunity |
| PUT | `/api/opportunities/{id}` | Update an owned opportunity |
| DELETE | `/api/opportunities/{id}` | Delete an owned opportunity |

### 7.6 Events

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/events` | Create an event |
| GET | `/api/events` | List events |
| GET | `/api/events/{id}` | View event details |
| POST | `/api/events/{id}/register` | Register for an event |
| PATCH | `/api/events/{id}` | Update an authorized event |

Administrative endpoints will be restricted to appropriately authorized users.

## 8. Authentication Design

JWT-based authentication will be used for protected API access.

1. The user submits login credentials.
2. The backend verifies the credentials.
3. The backend issues a signed JWT access token.
4. The frontend uses the token when calling protected APIs.
5. FastAPI validates the token before processing protected requests.
6. The backend checks authorization before returning or modifying data.

Passwords will be hashed before storage. JWT signing keys and database credentials will be stored in environment variables and excluded from version control.

## 9. RBAC and Security Scopes

The backend will implement role-based access control and permission scopes.

Examples of scopes include:

- `profile:read`
- `profile:update`
- `alumni:read`
- `alumni:verify`
- `connection:create`
- `connection:manage`
- `mentorship:create`
- `mentorship:manage`
- `opportunity:create`
- `event:create`
- `event:manage`
- `user:manage`

Each protected endpoint will require the appropriate scope. Permissions will be associated with the relevant roles and enforced through FastAPI dependencies or equivalent authorization logic.

The backend will also check resource ownership. For example, an alumnus may update their own opportunity but must not update another user's opportunity without explicit authorization.

## 10. Error Handling and Validation

The backend will validate request data and return appropriate HTTP status codes.

- `200 OK`: Successful request.
- `201 Created`: Resource created successfully.
- `400 Bad Request`: Invalid operation or request.
- `401 Unauthorized`: Missing or invalid authentication.
- `403 Forbidden`: Insufficient permissions.
- `404 Not Found`: Resource not found.
- `409 Conflict`: Duplicate or conflicting operation.
- `422 Unprocessable Entity`: Request validation failed.

Sensitive information shall not be included in error responses.

## 11. Proposed Folder Structure

```text
IUBLink/
├── docs/
│   ├── PRD.md
│   ├── SRS.md
│   └── TDD.md
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── types/
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── core/
│   └── requirements.txt
└── README.md
```

This structure represents the proposed organization. Files and directories may be added as implementation progresses.

## 12. Testing Strategy

- Test registration and login with valid and invalid credentials.
- Test profile creation and updates.
- Test alumni search and verification.
- Test connection and mentorship request workflows.
- Test opportunity and event operations.
- Verify that each role can access only permitted endpoints.
- Test unauthorized and forbidden API requests.
- Test frontend-backend integration.

## 13. Deployment Considerations

The application may be deployed using a frontend hosting service, a Python-compatible backend hosting service, and a managed PostgreSQL database. Deployment details will be finalized after local development and testing.

## 14. Conclusion

IUBLink will use a modular client-server architecture to provide networking, mentorship, career opportunities, and event management. React.js, TypeScript, FastAPI, PostgreSQL, JWT authentication, RBAC, and security scopes will support the development of a secure and maintainable web application.
