# IUBLink — Software Requirements Specification (SRS)

## 1. Introduction

### 1.1 Purpose

This document specifies the functional and non-functional requirements of IUBLink, a web-based networking platform for students, alumni, faculty members, and administrators of Independent University, Bangladesh.

### 1.2 Scope

IUBLink will support user authentication, profile management, alumni discovery, connection requests, mentorship requests, career opportunity sharing, event management, and administrative verification.

### 1.3 Intended Audience

This document is intended for project developers, course instructors, testers, and other stakeholders.

## 2. System Overview

IUBLink consists of a React.js frontend, a FastAPI backend, and a relational database. The frontend communicates with the backend through REST APIs. The backend validates user identity, checks permissions, processes requests, and stores application data.

## 3. User Classes

### 3.1 Student
A registered student can manage their own profile, browse alumni profiles, submit connection and mentorship requests, view career opportunities, and register for events.

### 3.2 Alumni
A verified alumnus can manage their professional profile, respond to connection and mentorship requests, and create or manage their own job and internship opportunities.

### 3.3 Faculty
A faculty member can browse the alumni directory and create or manage events and mentorship activities within their authorized permissions.

### 3.4 Administrator
An administrator can manage user accounts, verify alumni, moderate opportunities, manage roles, and oversee platform activities.

## 4. Functional Requirements

### FR-01: User Registration
The system shall allow users to register with the required information. The system shall validate input and prevent duplicate accounts for the same email address.

### FR-02: User Login
The system shall authenticate users using their registered credentials and issue an authentication token after successful login.

### FR-03: Profile Management
The system shall allow authenticated users to view and update their own profile. Users shall not be allowed to modify another user's private profile information without authorization.

### FR-04: Alumni Verification
The system shall allow administrators to review alumni verification requests and approve or reject them.

### FR-05: Alumni Directory
The system shall allow authorized users to browse and search alumni profiles using available fields such as name, graduation year, department, company, and industry.

### FR-06: Connection Requests
The system shall allow students and alumni to send connection requests. Recipients shall be able to accept or reject incoming requests. Users shall be able to view their own connection requests and connections.

### FR-07: Mentorship Requests
The system shall allow students to submit mentorship requests to alumni. The relevant alumni shall be able to accept or reject their requests. Students shall be able to track request status.

### FR-08: Opportunity Management
The system shall allow verified alumni to create, update, and manage their own job and internship opportunity posts. Authorized users shall be able to browse available opportunities.

### FR-09: Event Management
The system shall allow authorized faculty members and administrators to create and manage events. Students and alumni shall be able to view events and register for them.

### FR-10: User Management
The system shall allow administrators to view user accounts and perform authorized account management operations.

### FR-11: Access Control
The system shall restrict protected operations according to the authenticated user's role and permission scopes.

### FR-12: Content Moderation
The system shall allow authorized administrators to review and moderate inappropriate or unauthorized opportunity and event content.

## 5. Non-Functional Requirements

### NFR-01: Security
Passwords shall be stored using a secure password-hashing algorithm. Protected API endpoints shall require authentication and appropriate authorization.

### NFR-02: Performance
The system should return normal directory, profile, and opportunity requests within an acceptable response time under typical course-project usage.

### NFR-03: Usability
The user interface shall be simple, consistent, and easy to navigate for all supported user roles.

### NFR-04: Reliability
The system shall validate inputs and handle invalid requests and server errors without exposing sensitive internal information.

### NFR-05: Maintainability
The frontend and backend shall use a modular structure to support future improvements.

### NFR-06: Compatibility
The web application should work on modern browsers and adapt to common desktop and mobile screen sizes.

### NFR-07: Data Integrity
The system shall validate submitted data and maintain appropriate relationships between users, connections, mentorship requests, opportunities, and events.

## 6. Authentication Requirements

- Users must authenticate before accessing protected features.
- Passwords must not be stored in plain text.
- The backend must validate JWT tokens on protected requests.
- Invalid, expired, or missing tokens must not grant access.
- Logout must clear the client-side authentication state; token revocation may be added if supported by the implementation.

## 7. Authorization and RBAC Requirements

### 7.1 Student Permissions

- `profile:read`
- `profile:update`
- `alumni:read`
- `connection:create`
- `connection:read`
- `mentorship:create`
- `mentorship:read`
- `opportunity:read`
- `event:read`
- `event:register`

### 7.2 Alumni Permissions

- `profile:read`
- `profile:update`
- `alumni:read`
- `connection:create`
- `connection:read`
- `connection:manage`
- `mentorship:manage`
- `opportunity:create`
- `opportunity:update`
- `opportunity:read`
- `event:read`
- `event:register`

### 7.3 Faculty Permissions

- `profile:read`
- `profile:update`
- `alumni:read`
- `event:create`
- `event:manage`
- `mentorship:manage`

### 7.4 Administrator Permissions

- `user:read`
- `user:manage`
- `alumni:verify`
- `role:manage`
- `content:moderate`
- `event:manage`

Permissions shall be checked on the backend. The frontend may hide unavailable actions for usability, but frontend restrictions alone shall not be considered security enforcement.

## 8. Data Requirements

The system shall maintain the following main data entities:

- Users
- Profiles
- Connection Requests
- Mentorship Requests
- Opportunities
- Events
- Event Registrations

Each entity shall have an appropriate identifier and required fields. Relationships shall be maintained using database keys and constraints where appropriate.

## 9. API Requirements

The backend shall expose REST APIs for authentication, profiles, alumni search, connection requests, mentorship requests, opportunities, events, and administrative operations.

The API shall use standard HTTP methods and appropriate status codes. Protected endpoints shall enforce authentication and authorization.

## 10. Constraints and Assumptions

- The application will be developed using React.js with TypeScript and FastAPI with Python.
- The application will use a relational database.
- The first version will focus on essential networking features.
- Real-time messaging, online payments, and AI-based recommendations are excluded.
- The application is intended for academic demonstration and is not assumed to be an officially deployed IUB service.

## 11. Acceptance Criteria

The system will satisfy the main requirements when:

1. Users can register and log in successfully.
2. Each role receives access only to authorized features.
3. Students can browse alumni and submit connection or mentorship requests.
4. Verified alumni can manage opportunities.
5. Authorized faculty members can manage events.
6. Administrators can verify alumni and manage users.
7. Unauthorized API requests are rejected.
8. Frontend and backend operations work correctly together.


