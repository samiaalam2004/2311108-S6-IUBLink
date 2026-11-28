# Independent University, Bangladesh
## Department of Computer Science & Engineering
### CSE309 – Web Application & Internet

# Final Project Submission Report

**Submitted by:**

- **Name:** Mst. Samia Alam
- **Student ID:** 2311108
- **Section:** 06
- **Team Number:** None

**Project Title:** IUBLink – CareerHub

**Vercel URL:** https://iublink-careerhub.vercel.app  
**GitHub Repository:** https://github.com/samiaalam2004/2311108-S6-IUBLink

**Submitted To:**

Sayef Reyadh  
Adjunct Lecturer  
Department of Computer Science & Engineering  
Independent University, Bangladesh

**Semester:** Autumn 2026  
**Date of Submission:** 28 November 2026

---

# Table of Contents

1. Executive Summary
   - 1.1 Project Overview
   - 1.2 Development Since Mid-Assessment
   - 1.3 Live Project Links
2. Part A: Product Requirements Document (PRD)
   - A1. Problem Statement
   - A2. Users and Roles
   - A3. Project Goals and Success Measures
   - A4. Scope, Non-Goals, Assumptions and Constraints
   - A5. User Stories
3. Part B: Software Requirements Specification (SRS)
   - B1. Introduction and Definitions
   - B2. Functional Requirements
   - B3. Non-Functional Requirements
   - B4. Roles and Permission Matrix
   - B5. Use Cases
   - B6. Acceptance Criteria
   - B7. Requirements Traceability Matrix
4. Part C: Technical Design Document (TDD)
   - C1. Technology Stack
   - C2. System Architecture
   - C3. Project Folder Structure
   - C4. Database Design
   - C5. API Documentation
   - C6. Authentication and JWT Design
   - C7. RBAC Design
   - C8. Admin Dashboard Design
   - C9. Security Considerations
   - C10. Vercel Deployment
   - C11. Testing Strategy
5. Part D: Evidence and Screenshots
   - D1. User Features
   - D2. Security Evidence
   - D3. Admin Features
   - D4. Deployment Evidence
   - D5. Testing Evidence
6. Part E: Project Management and Conclusion
   - E1. Setup and Run Instructions
   - E2. GitHub Issues, Pull Requests and Contributions
   - E3. Limitations
   - E4. Future Improvements
   - E5. References and Tools
7. Appendix
   - Video Demonstration
   - Test Accounts and Credentials
   - Group and Member Permissions
   - Conclusion

---

# 1. Executive Summary

## 1.1 Project Overview

IUBLink CareerHub is a web-based career management platform developed as part of the CSE309 Web Application and Internet course at Independent University, Bangladesh. The system provides a centralized platform where users can access and manage career-related opportunities, including job and internship posts.

Registered users can create and manage their own career posts, while administrators can review submitted posts and approve or reject them. The application also includes user authentication, role-based access control, user management, and group management functionality.

The primary goal of the project is to make career-related information easier to share, organize, and manage through a structured and accessible web application.

**Technology Stack:** React with TypeScript (Frontend), FastAPI with Python (Backend), PostgreSQL (Database), JWT (Authentication), and Vercel (Deployment).

## 1.2 Development Since Mid-Assessment

Several important features and improvements have been introduced since the mid-assessment.

**JWT Authentication:** Implemented user registration, login, JWT-based authentication, refresh-token/session functionality, and logout operations.

**Role-Based Access Control (RBAC):** Implemented role-based restrictions for regular users and administrators, together with ownership checks for career posts.

**Career Post Management:** Developed functionality for creating, viewing, editing, and deleting career-related posts, including job-seeking, job, and internship post types.

**Admin Dashboard:** Implemented administrative functionality for viewing registered users and managing submitted career posts through approval and rejection operations.

**Audit Logging and Brute-Force Protection:** Implemented activity and login-attempt tracking with a failed-login limit and temporary account lockout mechanism.

**Group Management:** Added the initial group creation and member-management functionality. Advanced group permission management requires further verification.

**Vercel Deployment:** Deployed the frontend and backend separately on Vercel and configured communication between the application and backend REST API.

## 1.3 Live Project Links

| Resource | Link |
|---|---|
| GitHub Repository | https://github.com/samiaalam2004/2311108-S6-IUBLink |
| Vercel Frontend | https://iublink-careerhub.vercel.app |
| Backend API | https://2311108-s6-iub-link.vercel.app |
| API Documentation | https://2311108-s6-iub-link.vercel.app/docs |
| API Health Check | https://2311108-s6-iub-link.vercel.app/api/health |
| Video Demonstration | https://drive.google.com/file/d/1PLEtf4QxfoR-paQ_TP7XyGeQNLr8Odh3/view?usp=drive_link |

---

# Part A: Product Requirements Document (PRD)

## A1. Problem Statement

Finding and managing career opportunities can be challenging for university students and recent graduates. Students often search for job opportunities, internships, and career-related information through different sources, such as social media groups, university communities, and personal networks. As a result, relevant information may become scattered, difficult to track, or missed entirely.

Students who are looking for jobs also need a convenient way to communicate their career interests and share their professional information.

Alumni and other opportunity providers may also face difficulties when sharing job and internship opportunities with the university community. Without a centralized platform, it can be difficult to organize posts, review submitted information, and maintain the quality of shared opportunities.

Administrators also need a structured way to monitor users and manage submitted career posts. These problems highlight the need for a more organized and accessible career information management system for the university community.

## A2. Users and Roles

IUBLink CareerHub is intended for visitors, registered users, group members or owners, and administrators. Each role has different responsibilities and access limitations.

**Table 2: Users and Roles**

| Role | Who They Are | Main Tasks | Restricted Actions |
|---|---|---|---|
| Visitor | A person who visits without logging in. | View publicly available information and explore the platform. | Cannot create posts, access private information, or perform restricted actions. |
| User | A registered student or alumni member. | Register, log in, create career posts, and manage their own posts. | Cannot modify another user's posts or access administrative functions. |
| Group Member or Owner | A registered user who participates in or creates a group. | Participate in groups and use available group-management functionality. | Cannot perform actions beyond their assigned permissions. |
| Admin | An authorized administrator. | Manage users, review career posts, approve or reject submissions, and monitor platform activities. | Must not misuse administrative privileges or disclose sensitive information unnecessarily. |

**Note:** The current backend authorization implementation distinguishes regular users and administrators. Student, alumni, and faculty-specific permissions should not be assumed to be fully enforced unless verified in the deployed application.

## A3. Project Goals and Success Measures

The main goals of IUBLink CareerHub are to provide an organized career platform, protect user information, and ensure that users can access only the features permitted by their roles.

**Table 3: Goals and Measures**

| Goal ID | Goal | Success Measure |
|---|---|---|
| G-01 | Provide a centralized platform for career-related posts. | Registered users can create supported career posts successfully. |
| G-02 | Provide secure user authentication. | Users can register and log in with valid credentials, while invalid attempts are rejected. |
| G-03 | Enforce role-based access control. | Unauthorized users cannot perform restricted administrative actions. |
| G-04 | Protect user-owned information. | A user cannot edit or delete another user's posts through unauthorized access. |
| G-05 | Improve administrative control and content quality. | Admins can review pending posts and approve or reject them. |
| G-06 | Reduce repeated unauthorized login attempts. | After five consecutive failed login attempts, the account is temporarily locked for 15 minutes. |

## A4. Scope, Non-Goals, Assumptions and Constraints

### In Scope

The project focuses on the following functionalities:

1. **User Authentication:** User registration, login, logout, and session-related functionality.
2. **Role-Based Access Control:** Different access permissions for regular users and administrators.
3. **Career Post Management:** Users can create, view, edit, and delete their own career-related posts.
4. **Career Post Categories:** Support for job-seeking, job, and internship posts.
5. **Post Moderation:** Administrators can review pending posts and approve or reject submissions.
6. **User Management:** Administrators can view registered users and manage user access through available controls.
7. **Group Functionality:** Initial group creation and member-management functionality.
8. **Audit and Security Monitoring:** Record relevant activities and track failed login attempts.
9. **Deployment:** Make the frontend and backend accessible through the deployed application and API.

### Out of Scope

The following features are not included in the current project version:

- Real-time messaging and direct chat.
- Online job application submission.
- Payment processing and paid subscriptions.
- AI-based job matching and career recommendations.
- Advanced business intelligence and predictive analytics.
- Complete advanced group permission management.

These features are excluded to keep the project focused on its core career management functionalities within the available development time.

### Assumptions

- Users have access to an internet connection and a modern web browser.
- Users provide valid information during registration.
- Administrators are authorized to manage users and review submitted posts.
- Career information submitted by users should be relevant and appropriate for the university community.

### Constraints

- The application is developed within the time and resource limitations of the CSE309 course.
- The platform depends on third-party hosting and database services.
- Deployment and database operations are subject to the limitations of the selected hosting services.
- The application is primarily designed for modern desktop and mobile web browsers.
- Advanced features may be postponed due to development time and testing limitations.

## A5. User Stories

The following user stories describe the expected interactions of different users with IUBLink CareerHub.

**Table 4: User Stories**

| Story ID | Role | User Story |
|---|---|---|
| US-01 | Visitor | As a visitor, I want to explore the platform so that I can understand its purpose and available features. |
| US-02 | Visitor | As a visitor, I want to view publicly available career information so that I can learn about opportunities. |
| US-03 | User | As a user, I want to register an account so that I can access the platform's features. |
| US-04 | User | As a user, I want to log in and log out securely so that I can protect my account. |
| US-05 | User | As a user, I want to create a job-seeking post so that I can share my career interests. |
| US-06 | User | As a user, I want to publish job or internship opportunities so that other users can discover them, when permitted by my account. |
| US-07 | User | As a user, I want to edit or delete my own career posts so that I can keep my information updated. |
| US-08 | Group Owner | As a group owner, I want to create a group and add members so that I can organize users around shared interests. |
| US-09 | Group Member | As a group member, I want to participate in my group according to the available permissions. |
| US-10 | Admin | As an admin, I want to view registered users so that I can monitor platform membership. |
| US-11 | Admin | As an admin, I want to approve or reject pending career posts so that inappropriate content is not published. |
| US-12 | Admin | As an admin, I want to manage user access so that I can take action against accounts that violate platform rules. |
| US-13 | Admin | As an admin, I want to monitor platform activities and failed login attempts so that I can identify suspicious behavior. |

---

# Part B: Software Requirements Specification (SRS)

## B1. Introduction and Definitions

### Purpose

The purpose of this Software Requirements Specification (SRS) is to define the functional and non-functional requirements of IUBLink CareerHub. It describes the expected system behavior, user permissions, security requirements, and acceptance criteria.

This document provides a reference for developers, testers, project supervisors, and other stakeholders involved in the development and evaluation of the application.

### Intended Readers

This document is intended for:

- Course instructors and project evaluators.
- Developers responsible for maintaining the application.
- Testers who verify the application's functionality and security.
- Students, alumni, and administrators who use the platform.

### Definitions

| Term | Definition |
|---|---|
| JWT | JSON Web Token, a token format used to securely transmit authentication information. |
| Access Token | A short-lived token used to authenticate requests to protected resources. |
| Refresh Token | A token used to obtain a new access token without requiring the user to log in again. |
| RBAC | Role-Based Access Control, a method of assigning access rights according to user roles. |
| Role | A category assigned to a user, such as user or admin in the current backend implementation. |
| Permission | Authorization to perform a specific action or access a particular resource. |
| Audit Log | A record of relevant system activities used for monitoring and security purposes. |
| API | Application Programming Interface, which allows the frontend and backend to communicate. |
| CRUD | Create, Read, Update, and Delete operations performed on application data. |

### References

1. Jones, M., Bradley, J., and Sakimura, N. (2015). JSON Web Token (JWT), RFC 7519. https://www.rfc-editor.org/rfc/rfc7519
2. OWASP Foundation. Application Security Verification Standard (ASVS). https://owasp.org/www-project-application-security-verification-standard/
3. FastAPI Documentation. https://fastapi.tiangolo.com/
4. React Documentation. https://react.dev/
5. PostgreSQL Documentation. https://www.postgresql.org/docs/

## B2. Functional Requirements

The functional requirements describe the expected operations of IUBLink CareerHub. Each requirement has a unique ID to support implementation, testing, and traceability.

### FR-AUTH: Authentication and Account Management

| Requirement ID | Functional Requirement |
|---|---|
| FR-AUTH-01 | The system shall allow visitors to register an account by submitting the required registration information. |
| FR-AUTH-02 | The system shall allow registered users to log in using valid credentials. |
| FR-AUTH-03 | The system shall reject login attempts containing invalid credentials. |
| FR-AUTH-04 | The system shall securely hash user passwords before storing them in the database. |
| FR-AUTH-05 | The system shall use the configured password pepper as part of its password security process. |
| FR-AUTH-06 | The system shall issue a signed JWT access token after successful authentication. |
| FR-AUTH-07 | The system shall validate the JWT signature and relevant claims when a protected API endpoint is accessed. |
| FR-AUTH-08 | The system shall provide refresh-token functionality to support continued authenticated sessions. |
| FR-AUTH-09 | The system shall allow authenticated users to log out and invalidate applicable refresh-token access. |
| FR-AUTH-10 | The system shall temporarily lock an account for 15 minutes after five consecutive failed login attempts. |
| FR-AUTH-11 | The system shall reject authentication attempts while an account is under the temporary lockout period. |

**Implementation Note:** The current project includes JWT authentication, password hashing, refresh-token/session functionality, logout, and a five-attempt, 15-minute login lockout mechanism. Detailed session-list and individual session-revocation behavior should be documented as implemented only after verification.

### FR-RBAC: Role-Based Access Control

| Requirement ID | Functional Requirement |
|---|---|
| FR-RBAC-01 | The system shall distinguish users according to their assigned roles. |
| FR-RBAC-02 | The system shall perform authorization checks on the backend before allowing access to protected operations. |
| FR-RBAC-03 | The system shall restrict access to administrative operations to authorized administrators. |
| FR-RBAC-04 | The system shall allow users to update or delete only their own career posts. |
| FR-RBAC-05 | The system shall reject requests from unauthorized users when they attempt to access restricted resources. |
| FR-RBAC-06 | The system shall support group creation and member-management operations through available group functionality. |

**Implementation Note:** The current backend authorization module uses regular-user and admin roles. Basic group creation and member-management development exists, but complete group permission assignment, updates, and owner-only action enforcement have not been fully verified.

### FR-ADM: Administrative Functions

| Requirement ID | Functional Requirement |
|---|---|
| FR-ADM-01 | The system shall provide authorized administrators with access to administrative functions. |
| FR-ADM-02 | The system shall allow administrators to view registered users. |
| FR-ADM-03 | The system shall allow administrators to review submitted career posts. |
| FR-ADM-04 | The system shall allow administrators to approve pending career posts. |
| FR-ADM-05 | The system shall allow administrators to reject pending career posts. |
| FR-ADM-06 | The system shall allow authorized administrators to manage user access through available user-management controls. |
| FR-ADM-07 | The system shall support user access restrictions through available ban functionality. |
| FR-ADM-08 | The system shall record relevant authentication and security-related events for monitoring purposes. |

**Implementation Note:** User listing, post approval/rejection, and failed-login tracking are included in the current project. Advanced filtering, bulk moderation, detailed user profiles, filtered audit-log viewing, CSV exports, and a dedicated security dashboard have not been confirmed as implemented and are therefore not claimed as completed features.

### FR-DOMAIN: Career Post Management

| Requirement ID | Functional Requirement |
|---|---|
| FR-DOMAIN-01 | The system shall allow eligible registered users to create career-related posts. |
| FR-DOMAIN-02 | The system shall support job-seeking, job, and internship post types. |
| FR-DOMAIN-03 | The system shall allow users to provide a title and description when creating a career post. |
| FR-DOMAIN-04 | The system shall allow users to provide an optional company name. |
| FR-DOMAIN-05 | The system shall allow users to view available approved career posts. |
| FR-DOMAIN-06 | The system shall allow users to view and manage their own submitted posts. |
| FR-DOMAIN-07 | The system shall allow users to edit their own career posts. |
| FR-DOMAIN-08 | The system shall allow users to delete their own career posts. |
| FR-DOMAIN-09 | The system shall maintain a review status for submitted career posts. |
| FR-DOMAIN-10 | The system shall allow administrators to approve or reject submitted posts. |

## B3. Non-Functional Requirements

Non-functional requirements define the quality, security, performance, usability, reliability, and maintainability expectations of the application.

**Table 9: Non-Functional Requirements**

| Requirement ID | Category | Requirement |
|---|---|---|
| NFR-01 | Security | Sensitive configuration values, including database credentials and secret keys, shall be stored in environment variables. |
| NFR-02 | Security | Passwords shall be stored using a secure password-hashing mechanism rather than plaintext. |
| NFR-03 | Security | Invalid login attempts shall return an appropriate generic authentication error. |
| NFR-04 | Security | Invalid, expired, or tampered authentication tokens shall be rejected. |
| NFR-05 | Security | Authorization checks shall be enforced on the backend. |
| NFR-06 | Performance | Ordinary API responses should complete within three seconds under normal operating conditions, excluding external network and hosting delays. |
| NFR-07 | Performance | List endpoints should support controlled result sizes. |
| NFR-08 | Usability | The system should be accessible through modern desktop and mobile web browsers. |
| NFR-09 | Usability | The interface should provide appropriate loading, success, and error feedback. |
| NFR-10 | Reliability | Application data shall be stored in the configured PostgreSQL database. |
| NFR-11 | Reliability | The system shall return appropriate error responses when API requests cannot be completed. |
| NFR-12 | Maintainability | Authentication, routing, database operations, and administrative functionality shall be organized into separate modules. |
| NFR-13 | Maintainability | The project shall include automated tests for important application behavior. |

**Note:** The three-second response-time target is a quality objective and requires performance testing for confirmation. The currently verified automated test coverage includes one health-endpoint test. Broader automated test coverage remains future work.

## B4. Roles and Permission Matrix

This section describes the intended access boundaries of the application. The matrix distinguishes between verified access and functionality that requires further verification.

**Legend:**

- Yes: The role is permitted to perform the operation.
- No: The role is not permitted.
- Own: The role can perform the operation only on its own resources.
- Conditional: Access depends on assigned permissions.
- Not Verified: The functionality requires further implementation or testing.

### Table 10: Endpoint Groups by Roles

| Endpoint or Operation | Visitor | User | Group Member | Group Owner | Admin |
|---|---|---|---|---|---|
| View public platform information | Yes | Yes | Yes | Yes | Yes |
| Register account | Yes | No | No | No | No |
| Log in | Yes | Yes | Yes | Yes | Yes |
| Access own authenticated profile | No | Own | Own | Own | Own |
| Create eligible career post | No | Conditional | Conditional | Conditional | Conditional |
| View approved career posts | Yes | Yes | Yes | Yes | Yes |
| Edit own career posts | No | Own | Own | Own | Own |
| Delete own career posts | No | Own | Own | Own | Own |
| Review pending career posts | No | No | No | No | Yes |
| Approve or reject career posts | No | No | No | No | Yes |
| View registered users | No | No | No | No | Yes |
| Manage user access | No | No | No | No | Yes |
| Create a group | No | Conditional | Conditional | Conditional | Not Verified |
| Manage group membership | No | Not Verified | Not Verified | Conditional | Not Verified |
| Manage advanced group permissions | No | No | No | Not Verified | Not Verified |

**Note:** Group-related rows describe intended access boundaries, not a fully verified permission system.

### Table 11: Group Permissions

| Group Permission or Action | Meaning | Current Implementation Status |
|---|---|---|
| Create | Allows an eligible user to create a group. | Basic group creation code added; testing required. |
| Update | Allows an authorized user to update group information. | Not fully verified. |
| Assign | Allows an authorized user to assign permissions to group members. | Not fully verified. |
| Add Member | Allows a group manager to add members. | Basic member-management code added; testing required. |
| Remove Member | Allows an authorized user to remove a member. | Not fully verified. |
| Owner-only Actions | Restricts sensitive group-management actions to the group owner. | Not fully verified. |

### Table 12: Admin Rules

| Rule ID | Administrative Rule | Current Status |
|---|---|---|
| ADM-R01 | An administrator shall be restricted from accessing functions outside authorized privileges. | Backend role-based restrictions are implemented; individual cases require testing. |
| ADM-R02 | An administrator shall not modify another administrator's account without an authorized procedure. | Requires verification. |
| ADM-R03 | An administrator shall not ban another administrator through an unrestricted user-management action. | Requires verification. |
| ADM-R04 | An administrator shall be able to review and moderate submitted career posts. | Implemented for post approval and rejection. |
| ADM-R05 | An administrator shall not automatically receive group-owner privileges merely because of having the admin role. | Advanced group-role behavior is not fully verified. |

## B5. Use Cases

The following use cases describe important interactions between users and IUBLink CareerHub.

### Use Case Diagram

A use case diagram should illustrate the interactions between Visitor, User, Group Owner, Group Member, and Admin with the application.

**Suggested Use Case Diagram Actors and Actions:**

- Visitor: Explore platform, register, view public information.
- User: Log in, log out, create career post, view career posts, edit own post, delete own post.
- Group Owner: Create group and manage available group membership functionality.
- Group Member: Participate in available group functionality.
- Admin: View users, review posts, approve posts, reject posts, manage user access.

### Table 13: Use Case Descriptions

#### UC-01: User Login and Session Refresh

| Field | Description |
|---|---|
| Actor | Registered User |
| Preconditions | The user has a registered account and is not currently locked out. |
| Main Flow | 1. The user opens the login page. 2. The user enters an email address and password. 3. The system validates the credentials. 4. The system creates an authenticated session and issues the required authentication tokens. 5. The client can use refresh functionality when the access token needs renewal. |
| Alternative Flow | If the credentials are invalid, the system rejects the attempt and records the failed login attempt. |
| Error Flow | Invalid credentials: HTTP 401. Missing required input: HTTP 422. Temporarily locked account: authentication rejection response. |
| Postconditions | The user is authenticated after successful login and can access permitted resources. |

#### UC-02: Create a Career Post

| Field | Description |
|---|---|
| Actor | Registered User |
| Preconditions | The user is logged in and has permission to create the selected type of post. |
| Main Flow | 1. The user opens the career post creation page. 2. The user selects an eligible post type. 3. The user enters the title and description. 4. The user optionally provides a company name. 5. The user submits the form. 6. The system validates and saves the post. |
| Alternative Flow | If required information is missing, the system requests valid information. |
| Error Flow | Unauthorized request: HTTP 401 or 403. Invalid request data: HTTP 422. |
| Postconditions | The career post is stored and receives the appropriate review status. |

#### UC-03: Edit or Delete an Own Career Post

| Field | Description |
|---|---|
| Actor | Registered User |
| Preconditions | The user is authenticated and has created the selected career post. |
| Main Flow | 1. The user opens their own posts. 2. The user selects a post. 3. The user chooses to edit or delete it. 4. For editing, the user updates the information and submits it. 5. For deletion, the user confirms the action. 6. The system checks ownership and processes the request. |
| Alternative Flow | If the user cancels deletion, the post remains unchanged. |
| Error Flow | Unauthenticated request: HTTP 401. Access to another user's post: HTTP 403 or an appropriate not-found response, depending on endpoint implementation. |
| Postconditions | The user's own post is updated or deleted successfully. |

#### UC-04: Access a Restricted Resource

| Field | Description |
|---|---|
| Actor | Registered User |
| Preconditions | The user is authenticated but does not have the required permission. |
| Main Flow | 1. The user sends a request to a protected endpoint. 2. The system validates the authentication token. 3. The backend checks the user's role and resource ownership. 4. The system identifies that the user is not authorized. 5. The system rejects the request. |
| Alternative Flow | If the user has the required role and ownership rights, the system processes the request normally. |
| Error Flow | Missing or invalid authentication: HTTP 401. Authenticated but unauthorized access: HTTP 403. |
| Postconditions | Unauthorized access is prevented and the requested restricted operation is not performed. |

#### UC-05: Admin Reviews a Career Post

| Field | Description |
|---|---|
| Actor | Admin |
| Preconditions | The administrator is authenticated and has administrative permission. |
| Main Flow | 1. The admin opens the administrative dashboard. 2. The admin views submitted career posts. 3. The admin selects a pending post. 4. The admin reviews its information. 5. The admin approves or rejects the post. 6. The system updates the post status. |
| Alternative Flow | The admin may select another pending post for review. |
| Error Flow | Unauthorized access: HTTP 401 or 403. Invalid post identifier: appropriate error response. |
| Postconditions | The selected post receives the updated review status. |

#### UC-06: User Registration

| Field | Description |
|---|---|
| Actor | Visitor |
| Preconditions | The visitor is not logged in and provides the required registration information. |
| Main Flow | 1. The visitor opens the registration page. 2. The visitor enters the required details. 3. The system validates the submitted information. 4. The system checks whether the account information is acceptable. 5. The system creates the user account. |
| Alternative Flow | If required information is missing or invalid, the system displays validation feedback. |
| Error Flow | Invalid input: HTTP 422. Duplicate or unacceptable account information: appropriate error response. |
| Postconditions | A user account is created successfully. |

## B6. Acceptance Criteria

Acceptance criteria define the conditions that must be satisfied for the main system features to be considered acceptable.

| Feature | Acceptance Criteria |
|---|---|
| Registration | A visitor can submit valid registration information and receive an appropriate result. |
| Login | A registered user can log in using valid credentials. Invalid credentials are rejected. |
| Password Security | Passwords are stored using a secure hashing mechanism. |
| Token Authentication | Protected endpoints reject missing, invalid, or expired access tokens. |
| Refresh Session | The client can request a new access token through the refresh mechanism. |
| Login Lockout | Repeated failed login attempts trigger the configured temporary lockout. |
| Career Post Creation | An eligible authenticated user can submit a valid career post. |
| Career Post Ownership | A user can manage their own posts but cannot modify another user's posts without permission. |
| Post Moderation | An authorized administrator can approve or reject submitted posts. |
| User Management | An authorized administrator can view registered users through the available administrative interface. |
| API Availability | The health endpoint returns a successful response when the backend is operating correctly. |

## B7. Requirements Traceability Matrix

The following matrix connects major requirements to their related implementation areas and verification evidence.

| Requirement ID | Requirement Area | Implementation Location | Verification Evidence |
|---|---|---|---|
| FR-AUTH-01 | Registration | `routes/auth.py`, `services/auth_service.py` | Registration interface and API testing |
| FR-AUTH-02 | Login | `routes/auth.py`, `services/auth_service.py` | Login interface |
| FR-AUTH-04 | Password Hashing | `auth/security.py` | Authentication implementation |
| FR-AUTH-06 | JWT Access Token | `auth/security.py` | Protected API request |
| FR-AUTH-08 | Refresh Token | `routes/auth.py`, `crud/session_crud.py` | Refresh request |
| FR-AUTH-10 | Login Lockout | Authentication service and audit-related database operations | Failed login tracking |
| FR-RBAC-02 | Backend Authorization | `auth/permissions.py` | Unauthorized API response |
| FR-RBAC-04 | Post Ownership | Post routes and services | Own-post management |
| FR-ADM-02 | User Listing | `routes/admin.py`, `services/admin_service.py` | Admin interface |
| FR-ADM-04 | Post Approval | Admin routes and services | Admin approval screenshot |
| FR-ADM-05 | Post Rejection | Admin routes and services | Admin rejection screenshot |
| FR-DOMAIN-01 | Career Post Creation | `routes/posts.py`, `services/post_service.py` | Post creation screenshot |
| FR-DOMAIN-07 | Post Update | Post routes and services | Post editing test |
| FR-DOMAIN-08 | Post Deletion | Post routes and services | Post deletion test |
| NFR-13 | Automated Testing | `tests/test_health.py` | Pytest output |

**Note:** The evidence column identifies suggested verification evidence. Only the health-endpoint automated test has a confirmed recorded result in this report.

---

# Part C: Technical Design Document (TDD)

## C1. Technology Stack

IUBLink CareerHub uses a modern full-stack architecture with separate frontend and backend applications.

| Technology | Version / Environment | Purpose |
|---|---|---|
| Python | 3.13.17 (local environment) | Backend programming language |
| FastAPI | 0.162.0 | REST API development |
| React | 19.3.0 | Frontend user interface |
| TypeScript | 7.0.2 | Type-safe frontend development |
| React Router DOM | 7.18.5 | Frontend routing and navigation |
| Vite | 8.3.2 | Frontend development server and build tool |
| PostgreSQL | Supabase-hosted | Relational database |
| PyJWT | 2.15.1 | JWT token handling |
| pwdlib | 0.3.1 | Password hashing using Argon2 |
| Psycopg | 3.3.9 | PostgreSQL database connectivity |
| SQLAlchemy | 2.1.9 | Database-related Python tooling, where used |
| python-dotenv | Declared in requirements | Loading environment variables |
| Pytest | 9.2.0 | Backend automated testing |
| HTTPX | 0.28.1 | HTTP client and API testing support |
| Vercel | Cloud deployment | Frontend and backend hosting |
| Git and GitHub | Version control | Source code management |

## C2. System Architecture

IUBLink CareerHub follows a client-server architecture. The React frontend communicates with the FastAPI backend through REST API endpoints. The backend handles application logic, authentication, authorization, and database operations.

### Main Architectural Components

**Frontend Layer**

The frontend is developed using React and TypeScript. It provides the user interface for registration, login, career post management, and administrative operations.

**Backend API Layer**

The backend uses FastAPI to define REST endpoints. It receives requests from the frontend, validates input, checks authentication and authorization, and returns appropriate responses.

**Service Layer**

The service layer handles application logic, including authentication, career post operations, user management, and administrative functionality.

**CRUD Layer**

The CRUD layer performs database operations such as creating, retrieving, updating, and deleting records.

**Database Layer**

PostgreSQL is used as the main application database. The hosted database is managed through Supabase.

### System Architecture Flow

```text
+---------------------------+
|       Web Browser         |
|    React + TypeScript     |
+-------------+-------------+
              |
              | HTTPS / REST API
              v
+---------------------------+
|       FastAPI Backend     |
|                           |
|  API Routes               |
|  Authentication          |
|  Authorization / RBAC     |
|  Business Services        |
|  CRUD Operations          |
+-------------+-------------+
              |
              | Database Connection
              v
+---------------------------+
|        PostgreSQL         |
|      Supabase Hosted      |
+---------------------------+

Frontend and Backend Deployment:
          Vercel
```

## C3. Project Folder Structure

### C3.1 Backend Folder Structure

The backend of IUBLink CareerHub is developed using Python and FastAPI. It follows a modular architecture that separates API routes, business logic, database operations, authentication, data models, and validation schemas.

**Backend Directory Structure:**

```text
backend/
├── auth/
│   ├── permissions.py
│   ├── request_info.py
│   └── security.py
├── backend/
│   └── api/
│       └── index.py
├── config/
│   └── settings.py
├── crud/
│   ├── audit_crud.py
│   ├── group_crud.py
│   ├── post_crud.py
│   ├── session_crud.py
│   └── user_crud.py
├── database/
│   └── connection.py
├── models/
│   ├── audit.py
│   ├── group.py
│   ├── post.py
│   ├── session.py
│   ├── user.py
│   └── __init__.py
├── routes/
│   ├── admin.py
│   ├── audit.py
│   ├── auth.py
│   ├── groups.py
│   ├── posts.py
│   └── users.py
├── schemas/
│   ├── group.py
│   ├── post.py
│   └── user.py
├── services/
│   ├── admin_service.py
│   ├── auth_service.py
│   ├── group_service.py
│   ├── post_service.py
│   └── user_service.py
├── tests/
│   └── test_health.py
├── db.py
├── main.py
└── requirements.txt
```

### Responsibilities of Backend Components

| Folder/File | Responsibilities |
|---|---|
| `main.py` | Creates the FastAPI application, configures CORS, initializes the database, and registers API routers. |
| `auth/` | Handles authentication security, JWT-related operations, permission checking, and request information. |
| `config/` | Stores application configuration and environment-based settings. |
| `routes/` | Defines API endpoints for authentication, career posts, administration, users, and groups. |
| `services/` | Contains business logic for authentication, posts, administration, users, and groups. |
| `crud/` | Handles database operations such as creating, retrieving, updating, and deleting records. |
| `database/` | Manages database connections and initialization. |
| `models/` | Contains database table definitions and related SQL statements. |
| `schemas/` | Defines request and response data structures and validation rules. |
| `tests/` | Contains automated backend tests. |
| `requirements.txt` | Lists the Python dependencies required by the backend. |

### Backend Architecture and Implementation

The backend follows a layered architecture to keep different responsibilities separate.

- **Route Layer:** Receives HTTP requests from the frontend and directs them to the appropriate service functions.
- **Service Layer:** Processes application logic, including authentication, post management, and administrative operations.
- **CRUD Layer:** Performs database operations through reusable functions.
- **Model Layer:** Defines the database structures used by the application.
- **Schema Layer:** Validates incoming request data and structures API responses.

The application uses reusable authentication and authorization dependencies. The `get_current_user()` function verifies the access token and retrieves the authenticated user. The `require_role()` function checks whether the user's role is permitted to perform a particular operation.

The `main.py` file registers the authentication, posts, admin, users, and groups routers with the FastAPI application.

### C3.2 Frontend Folder Structure

The frontend of IUBLink CareerHub is developed using React and TypeScript. It follows a component-based structure where pages, reusable UI components, API services, and TypeScript types are maintained separately.

**Frontend Directory Structure:**

```text
frontend/
└── src/
    ├── components/
    │   ├── DashboardStats.tsx
    │   ├── Navbar.tsx
    │   └── Sidebar.tsx
    ├── pages/
    │   ├── Dashboard.tsx
    │   ├── Home.tsx
    │   ├── Login.tsx
    │   └── Register.tsx
    ├── services/
    │   ├── adminService.ts
    │   ├── api.ts
    │   ├── authService.ts
    │   ├── groupService.ts
    │   └── postService.ts
    ├── types/
    │   ├── auth.ts
    │   ├── group.ts
    │   ├── post.ts
    │   └── user.ts
    ├── App.tsx
    ├── App.css
    ├── index.css
    └── main.tsx
```

### Responsibilities of Frontend Components

| Folder/File | Responsibilities |
|---|---|
| `main.tsx` | Entry point of the React application. |
| `App.tsx` | Defines the main application structure and page routing. |
| `components/` | Contains reusable UI components such as Navbar, Sidebar, and Dashboard Statistics. |
| `pages/` | Contains the main application pages, including Home, Login, Register, and Dashboard. |
| `services/` | Handles communication with backend APIs through separate service modules. |
| `services/api.ts` | Provides a centralized API client for sending requests, attaching access tokens, refreshing sessions, and handling responses. |
| `types/` | Contains TypeScript type definitions for authentication, users, groups, and career posts. |
| `App.css` | Contains application-level styling. |
| `index.css` | Contains global styling rules. |

### Frontend Routing

React Router DOM is used to navigate between the main application pages. The routes are defined in `App.tsx`.

| Route | Page Component | Description |
|---|---|---|
| `/` | Home | Displays the home page. |
| `/login` | Login | Provides the user login interface. |
| `/register` | Register | Provides the user registration interface. |
| `/dashboard` | CareerDashboard | Displays the main career management dashboard. |

### Frontend Authentication and API Communication

The frontend communicates with the FastAPI backend through a centralized API service.

The `api.ts` file manages access tokens and API requests. The access token is maintained in a JavaScript module variable and attached to protected API requests through the HTTP Authorization header using the Bearer token scheme.

The application also uses a refresh-token cookie to maintain the user's session. When an API request returns an unauthorized response (HTTP 401), the frontend attempts to refresh the access token and retries the original request once.

Separate service modules organize API communication:

- `authService.ts` handles authentication-related API operations.
- `postService.ts` handles career post-related API operations.
- `adminService.ts` handles administrative API operations.
- `groupService.ts` handles group-related API operations.

This structure improves code organization, reusability, and maintainability.

## C4. Database Design

IUBLink CareerHub uses PostgreSQL as its primary relational database. The database is hosted through Supabase and is accessed by the FastAPI backend.

The database stores information required for user authentication, career posts, groups, sessions, and security-related activities.

### Main Database Entities

| Entity | Purpose |
|---|---|
| Users | Stores registered user information, account details, roles, and account status. |
| Posts | Stores career-related posts, including title, description, post type, company information, and review status. |
| Groups | Stores group information and ownership-related details. |
| Sessions | Stores refresh-token session information and related session metadata. |
| Audit Logs | Stores relevant user and administrative activity records. |

### Database Relationships

The database uses relational connections between users and other application records.

- One user can create multiple career posts.
- One user can have multiple session records.
- One user can be associated with relevant audit-log records.
- Groups can be associated with their owners and membership records.
- Career posts are associated with their respective creators.

### Database Security

The backend uses environment-based configuration to connect to the hosted PostgreSQL database. Database credentials are not stored directly in public source code.

**Note:** The exact database columns, foreign-key constraints, and group-membership relationship should be verified against the current Supabase schema before adding a detailed ER diagram.

## C5. API Documentation

The backend provides REST API endpoints through FastAPI.

The interactive Swagger documentation is available at:

https://2311108-s6-iub-link.vercel.app/docs

The API health endpoint is available at:

https://2311108-s6-iub-link.vercel.app/api/health

The health endpoint returns a response similar to:

```json
{
  "status": "ok"
}
```

### API Functional Areas

| API Area | Purpose |
|---|---|
| Authentication API | Registration, login, refresh-token, and logout operations. |
| Posts API | Career post creation, viewing, updating, and deletion. |
| Admin API | Administrative user and post management operations. |
| Users API | User-related operations. |
| Groups API | Group creation and available membership operations. |

### HTTP Status Codes

| Status Code | Meaning |
|---|---|
| 200 OK | The request was completed successfully. |
| 201 Created | A resource was created successfully. |
| 401 Unauthorized | Authentication is missing, invalid, or expired. |
| 403 Forbidden | The authenticated user does not have the required permission. |
| 404 Not Found | The requested resource could not be found. |
| 422 Unprocessable Entity | The request data failed validation. |
| 500 Internal Server Error | An unexpected server-side error occurred. |

**Note:** The exact endpoint paths and supported methods should be checked in the live Swagger documentation.

## C6. Authentication and JWT Design

IUBLink CareerHub uses JSON Web Tokens (JWT) to authenticate users and protect restricted API endpoints.

### Authentication Flow

1. A user submits their login credentials through the frontend.
2. The backend validates the supplied credentials.
3. The password is verified using the configured password-hashing mechanism.
4. After successful authentication, the backend issues a signed JWT access token.
5. The frontend uses the access token when accessing protected API endpoints.
6. The backend verifies the token before processing protected requests.
7. When the access token needs renewal, the frontend sends a refresh request.
8. The backend processes the refresh request and returns a renewed access token when valid.
9. The user can log out to invalidate the applicable refresh-token session.

### JWT and Session Security

- JWT access tokens are signed using the configured secret key.
- The configured signing algorithm is HS256.
- Passwords are hashed using Argon2 through `pwdlib`.
- A configured password pepper is included in the password-security process.
- Refresh-token functionality supports continued authenticated sessions.
- The frontend sends the access token through the Bearer Authorization header.
- Refresh-token cookies are configured through backend settings.

### Authentication Configuration

The backend settings include the following configuration values:

| Configuration | Purpose |
|---|---|
| `SECRET_KEY` | Used for signing authentication tokens. |
| `PEPPER` | Additional password-security configuration. |
| `ALGORITHM` | JWT signing algorithm, configured as HS256. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access-token lifetime configuration. |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh-token lifetime configuration. |
| `MAX_FAILED_ATTEMPTS` | Maximum failed login attempts before lockout. |
| `LOCKOUT_MINUTES` | Temporary account lockout duration. |
| `REFRESH_COOKIE_NAME` | Name of the refresh-token cookie. |
| `COOKIE_SECURE` | Controls whether cookies require HTTPS. |
| `COOKIE_SAMESITE` | Configures the cookie SameSite policy. |

## C7. RBAC Design

Role-Based Access Control (RBAC) is used to restrict access to application resources according to a user's assigned role.

The backend uses authentication and authorization dependencies to check whether a user is permitted to perform a requested operation.

### Main RBAC Components

**Authentication Dependency:** The `get_current_user()` function verifies the JWT access token and retrieves the authenticated user.

**Role Dependency:** The `require_role()` function checks whether the user's assigned role is included in the list of permitted roles.

**Ownership Checks:** Career post operations use ownership checks to prevent unauthorized users from modifying another user's posts.

### Authorization Process

1. The user sends a request to a protected API endpoint.
2. The backend checks the authentication token.
3. The backend retrieves the authenticated user.
4. The authorization dependency checks the user's role.
5. Resource ownership is checked when applicable.
6. The backend processes or rejects the request.

An unauthenticated request receives an HTTP 401 response. An authenticated user without the required permission receives an HTTP 403 response.

**Implementation Note:** The current backend role implementation distinguishes regular users and administrators. Advanced group-level permission assignment and enforcement require further development and testing.

## C8. Admin Dashboard Design

The administrative dashboard provides authorized administrators with access to management functionality.

### Main Administrative Features

- View registered users.
- Access administrative functionality.
- View submitted career posts.
- Review pending posts.
- Approve career posts.
- Reject career posts.
- Manage user access through available controls.
- Support security-related monitoring through recorded authentication and activity information.

### Post Moderation Workflow

1. A registered user submits a career post.
2. The submitted post receives an appropriate review status.
3. The administrator opens the post-management section.
4. The administrator reviews the submitted information.
5. The administrator approves or rejects the post.
6. The system updates the post status.

The dashboard helps administrators maintain the quality and organization of career-related information.

## C9. Security Considerations

Security is an important consideration in IUBLink CareerHub.

### Password Security

Passwords are not stored as plaintext. The application uses Argon2 password hashing through `pwdlib`.

### JWT Authentication

Protected API endpoints require valid authentication tokens. The backend verifies the token before providing access to protected resources.

### Role-Based Authorization

Administrative endpoints are restricted through backend authorization checks. Frontend visibility alone is not treated as the security boundary.

### Account Lockout

The authentication system tracks failed login attempts. The configured limit is five failed attempts, followed by a temporary lockout period of 15 minutes.

### Environment Variables

Sensitive configuration values, including secret keys, password pepper, and database connection details, are loaded through environment variables.

### Refresh-Token Handling

Refresh-token functionality supports continued authenticated sessions. The frontend uses credentials-enabled requests to support the refresh-cookie mechanism.

### Audit and Login Tracking

Relevant activity and login-attempt information is recorded for security monitoring and administrative review.

### Security Limitations

Further testing is required to verify session revocation, refresh-token edge cases, advanced group authorization, and broader security scenarios.

## C10. Vercel Deployment

The frontend and backend of IUBLink CareerHub are deployed separately using Vercel.

### Frontend Deployment

The React and TypeScript frontend is deployed through Vercel.

**Production URL:**

https://iublink-careerhub.vercel.app

### Backend Deployment

The Python FastAPI backend is deployed separately through Vercel.

**Backend URL:**

https://2311108-s6-iub-link.vercel.app

### API Documentation

https://2311108-s6-iub-link.vercel.app/docs

### Database Hosting

The application uses a Supabase-hosted PostgreSQL database. The backend connects to the database using the configured database connection string.

### Environment Configuration

Deployment-specific settings are configured through environment variables. Sensitive values are not included in the public GitHub repository.

### Deployment Architecture

```text
User Browser
     |
     v
Vercel Frontend
     |
     | HTTPS REST API
     v
Vercel Backend
     |
     | PostgreSQL Connection
     v
Supabase PostgreSQL
```

Separate frontend and backend deployments allow the application interface and API services to be maintained independently.

## C11. Testing Strategy

Testing is necessary to verify that the application behaves correctly and that important security requirements are enforced.

### Testing Areas

**Authentication Testing:** Registration, login, invalid credentials, and refresh-token functionality.

**Authorization Testing:** Protected endpoint access and role-based restrictions.

**Career Post Testing:** Post creation, viewing, editing, deletion, and moderation.

**Database Testing:** Database connectivity and record operations.

**Deployment Testing:** Live frontend availability, backend health, and API documentation access.

**Automated Testing:** Pytest is used for backend automated tests.

### Verified Automated Test

The following test was executed from the backend directory:

```powershell
python -m pytest tests/test_health.py -v
```

Verified output:

```text
tests\test_health.py::test_health_endpoint PASSED

1 passed in 6.49s
```

This confirms that the health-endpoint test completed successfully.

**Testing Limitation:** The verified automated test coverage currently includes one health-endpoint test. Additional automated tests are needed for authentication, authorization, database operations, and administrative features.

---

# Part D: Evidence and Screenshots

This section presents screenshots of the running IUBLink CareerHub application and supporting deployment and testing evidence.

Screenshots should be captured from the deployed application whenever possible. Passwords, secret keys, and authentication tokens must be masked before including screenshots in the report.

## D1. User Features

### Figure D1.1: User Registration and Login

Shows the user registration and login interfaces, including appropriate validation feedback.

**Related Requirements:** FR-AUTH-01, FR-AUTH-02, FR-AUTH-03.

**Screenshot:** Insert the registration and login screenshot here.

### Figure D1.2: Logged-in User Dashboard

Shows the main application interface after a user successfully logs in.

**Related Requirements:** FR-AUTH-02, FR-DOMAIN-05.

**Screenshot:** Insert the logged-in dashboard screenshot here.

### Figure D1.3: Career Post Creation

Shows the career post creation form, including post type, title, description, and optional company name.

**Related Requirements:** FR-DOMAIN-01, FR-DOMAIN-02, FR-DOMAIN-03, FR-DOMAIN-04.

**Screenshot:** Insert the career post creation screenshot here.

### Figure D1.4: Career Post Details

Shows the details of a submitted or published career post.

**Related Requirements:** FR-DOMAIN-05, FR-DOMAIN-09.

**Screenshot:** Insert the career post details screenshot here.

### Figure D1.5: User's Own Career Posts

Shows the career posts associated with the logged-in user.

**Related Requirements:** FR-DOMAIN-06, FR-DOMAIN-07, FR-DOMAIN-08.

**Screenshot:** Insert the user's own posts screenshot here.

### Figure D1.6: Group Functionality

Shows the available group interface and member-related functionality, if accessible in the deployed version.

**Related Requirements:** FR-RBAC-06.

**Screenshot:** Insert a verified group screenshot here, if available.

## D2. Security Evidence

### Figure D2.1: Authentication Validation

Shows an authentication validation error for invalid input.

**Related Requirements:** FR-AUTH-02, FR-AUTH-03.

**Screenshot:** Insert the validation screenshot here.

### Figure D2.2: Authorization Header

Shows a protected API request using the Bearer Authorization header. The actual token must be masked.

**Related Requirements:** FR-AUTH-06, FR-AUTH-07.

**Screenshot:** Insert the browser Network tab screenshot here, if captured.

### Figure D2.3: Refresh-Token Request

Shows the refresh request and the related response. Sensitive cookie and token values must be hidden.

**Related Requirements:** FR-AUTH-08.

**Screenshot:** Insert the refresh request screenshot here, if captured.

### Figure D2.4: Unauthorized Access

Shows an unauthorized request being rejected by the backend.

**Related Requirements:** FR-RBAC-02, FR-RBAC-05.

**Screenshot:** Insert a verified unauthorized response screenshot here, if available.

### Figure D2.5: Failed Login Tracking

Shows relevant failed login-attempt tracking or the configured account lockout behavior.

**Related Requirements:** FR-AUTH-10, FR-AUTH-11.

**Screenshot:** Insert a verified screenshot here, if available.

## D3. Admin Features

### Figure D3.1: Admin Dashboard

Shows the administrative dashboard and its available management features.

**Related Requirements:** FR-ADM-01, FR-ADM-02.

**Screenshot:** Insert the admin dashboard screenshot here.

### Figure D3.2: Admin User Management

Shows the registered users available through the administrative interface.

**Related Requirements:** FR-ADM-02, FR-ADM-06.

**Screenshot:** Insert the user management screenshot here.

### Figure D3.3: Career Post Approval and Rejection

Shows an administrator reviewing a submitted career post and approving or rejecting it.

**Related Requirements:** FR-ADM-03, FR-ADM-04, FR-ADM-05.

**Screenshot:** Insert the admin post moderation screenshot here.

### Figure D3.4: Administrative Access Control

Shows an administrative operation being accessed through an authorized account.

**Related Requirements:** FR-ADM-01, FR-RBAC-02.

**Screenshot:** Insert a verified screenshot here.

### Figure D3.5: Security and Activity Tracking

Shows available activity or failed-login tracking information, if accessible in the deployed application.

**Related Requirements:** FR-ADM-08.

**Screenshot:** Insert a verified screenshot here, if available.

**Evidence Note:** Do not create screenshots for features that are not implemented or cannot be accessed. Advanced filtering, bulk moderation, CSV export, dedicated security views, and detailed session management should only be shown if they are actually available.

## D4. Deployment Evidence

### Figure D4.1: Frontend Deployment on Vercel

Shows the IUBLink CareerHub frontend project with its production deployment and domain.

**Screenshot:** Insert the Vercel frontend deployment screenshot here.

### Figure D4.2: Backend Deployment on Vercel

Shows the backend project and its deployment status.

**Screenshot:** Insert the Vercel backend deployment screenshot here.

### Figure D4.3: Environment Variable Configuration

Shows the configured environment variable names in Vercel. All secret values must remain hidden.

**Screenshot:** Insert the Vercel environment variable screenshot here.

### Figure D4.4: FastAPI Swagger Documentation

Shows the live FastAPI Swagger documentation page.

**API Documentation:** https://2311108-s6-iub-link.vercel.app/docs

**Screenshot:** Insert the Swagger UI screenshot here.

### Figure D4.5: API Health Check

Shows the successful response from the deployed backend health endpoint.

**API Endpoint:** https://2311108-s6-iub-link.vercel.app/api/health

Expected response:

```json
{
  "status": "ok"
}
```

**Screenshot:** Insert the API health-check screenshot here.

### Figure D4.6: GitHub Repository

Shows the IUBLink project repository and its source-code structure.

**Repository:** https://github.com/samiaalam2004/2311108-S6-IUBLink

**Screenshot:** Insert the GitHub repository screenshot here.

## D5. Testing Evidence

### Figure D5.1: Automated Backend Test Execution

The backend health endpoint was tested using Pytest.

**Command:**

```powershell
python -m pytest tests/test_health.py -v
```

**Verified Result:**

```text
tests\test_health.py::test_health_endpoint PASSED

1 passed in 6.49s
```

This test confirms that the health endpoint test completed successfully.

**Screenshot:** Insert the terminal screenshot showing the Pytest output here.

---

# Part E: Project Management and Conclusion

## E1. Setup and Run Instructions

This section explains how to install, configure, run, and test the IUBLink CareerHub application.

### E1.1 Prerequisites

The following software and tools are required:

| Software / Tool | Version / Requirement |
|---|---|
| Python | 3.13.17 |
| Node.js | Compatible with Vite 8 |
| npm | Installed with Node.js |
| PostgreSQL | Supabase-hosted PostgreSQL or another compatible PostgreSQL instance |
| Git | Latest stable version |
| Visual Studio Code | Recommended code editor |

### E1.2 Clone the Repository

Clone the project from GitHub:

```powershell
git clone https://github.com/samiaalam2004/2311108-S6-IUBLink.git
```

Navigate to the project directory:

```powershell
cd 2311108-S6-IUBLink
```

### E1.3 Backend Environment Configuration

Create a `.env` file inside the `backend` directory.

Example configuration:

```env
SECRET_KEY=your_generated_secret_key
PEPPER=your_generated_pepper
DATABASE_URL=postgresql://username:password@host:5432/database

FRONTEND_URL=http://localhost:5173

ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

MAX_FAILED_ATTEMPTS=5
LOCKOUT_MINUTES=15

COOKIE_SECURE=false
COOKIE_SAMESITE=lax
```

Replace the example values with valid environment-specific configuration.

For local HTTP development, `COOKIE_SECURE` can be set to `false`. For production HTTPS deployment, it should be set to `true`.

The database URL, secret key, and pepper must never be committed to the public repository.

**Important:** The actual deployment configuration is managed through Vercel environment variables. The example above is for local setup and should be checked against the current backend settings before use.

### E1.4 Frontend Environment Configuration

Create or configure the `.env` file inside the `frontend` directory:

```env
VITE_API_URL=http://127.0.0.1:8000
```

This variable specifies the backend API base URL used by the frontend during local development.

### E1.5 Backend Installation and Execution

Open a terminal and navigate to the backend directory:

```powershell
cd backend
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

Install backend dependencies:

```powershell
pip install -r requirements.txt
```

Run the FastAPI development server:

```powershell
python -m uvicorn main:app --reload
```

The backend will be available at:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

### E1.6 Frontend Installation and Execution

Open another terminal and navigate to the frontend directory:

```powershell
cd frontend
```

Install the frontend dependencies:

```powershell
npm install
```

Start the Vite development server:

```powershell
npm run dev
```

The frontend will normally be available at:

http://localhost:5173

### E1.7 Running Automated Tests

The backend uses Pytest for automated testing.

Navigate to the backend directory and activate the virtual environment if it is not already active.

Run all available backend tests:

```powershell
python -m pytest tests -v
```

To run the health endpoint test separately:

```powershell
python -m pytest tests/test_health.py -v
```

The verified health test result was:

```text
tests\test_health.py::test_health_endpoint PASSED

1 passed in 6.49s
```

This confirms that the health endpoint test completed successfully. It does not indicate that every application feature has been fully tested.

### E1.8 Test Account Login

After starting the application, open the frontend in a web browser and navigate to the login page.

The application supports different user access levels:

- **Admin:** Used to access administrative functions and manage permitted application activities.
- **User:** Used to access regular application features, including career post management.

Demonstration account IDs and passwords should be provided only in the Appendix of the final PDF report.

All demonstration accounts should use non-sensitive test data. Credentials must not be included in this Markdown file, README, source code, or public GitHub repository.

## E2. GitHub Issues, Pull Requests and Contributions

The project source code is maintained in the following GitHub repository:

https://github.com/samiaalam2004/2311108-S6-IUBLink

The project was developed and maintained through Git commits and feature branches. Pull requests were used to review and merge feature changes into the main branch.

### E2.1 Pull Requests and Feature Contributions

| Issue / PR | Title | Contribution |
|---|---|---|
| PR #9 | Refresh Token Sessions | Added refresh-token session functionality and related session-management changes. |
| Feature | JWT Authentication | Implemented authentication-related functionality, including token-based access and password security. |
| Feature | Role-Based Access Control | Added backend role checks and resource ownership restrictions. |
| Feature | Admin Dashboard | Developed administrative user and career post management functionality. |
| Feature | Career Post Management | Implemented career post creation, viewing, updating, deletion, and moderation functionality. |
| Feature | Group Management | Added initial group creation and member-management functionality. |

**Note:** Only PR #9 is listed here as a verified numbered pull request. The remaining rows describe project features, not confirmed PR numbers. The full PR history can be checked at:

https://github.com/samiaalam2004/2311108-S6-IUBLink/pulls

GitHub Issues:

https://github.com/samiaalam2004/2311108-S6-IUBLink/issues

### E2.2 Recent Commit Contributions

The following recent commits are associated with the GitHub account `samiaalam2004`:

| Commit | Date | Description |
|---|---|---|
| `a9b2267` | 2026-11-28 | Removed the temporary admin password reset endpoint. |
| `0685bed` | 2026-11-28 | Added a temporary admin password reset endpoint. |
| `d96bb90` | 2026-11-28 | Updated the backend to use native Vercel FastAPI deployment. |
| `69dc6ca` | 2026-11-28 | Restored the backend Vercel entry point with a Python path fix. |
| `1259efd` | 2026-11-28 | Reverted an earlier Vercel deployment routing change. |
| `805b0fa` | 2026-11-28 | Removed an outdated root Vercel configuration file. |
| `3e566bc` | 2026-11-28 | Updated Vercel deployment routing. |
| `5b95fb1` | 2026-11-28 | Merged Pull Request #9 for refresh-token sessions. |

These records show recent development, deployment configuration, and session-management work. The complete contribution history can be reviewed in the GitHub repository.

### E2.3 Work Distribution Over Time

The development work was carried out in multiple stages:

1. **Initial Development:** Project setup, frontend and backend structure, and core application development.
2. **Feature Development:** Authentication, career post management, user management, and administrative functionality.
3. **Security Improvements:** JWT authentication, role-based authorization, refresh-token handling, and session-related functionality.
4. **Integration and Deployment:** Frontend-backend integration, database configuration, and Vercel deployment.
5. **Testing and Final Updates:** Health endpoint testing, deployment corrections, and final code maintenance.

## E3. Limitations

Although IUBLink CareerHub implements important career-management and security features, some limitations remain.

**Automated Test Coverage:** The verified automated test currently covers the backend health endpoint. More tests are needed for authentication, authorization, database operations, and administrative features.

**Group Functionality:** Group creation and membership functionality require further testing, particularly member permissions and access restrictions.

**Administrative Features:** Advanced administration features such as comprehensive filtering, bulk moderation, and detailed security reporting require further verification and improvement.

**Session Management:** Session revocation and refresh-token handling should receive additional integration and security testing.

**Security Testing:** More comprehensive security testing is required for token handling, access control, account lockout, and unauthorized requests.

**User Experience:** Additional usability improvements and error-handling refinements could make the application easier to use.

These limitations identify areas that require additional implementation, testing, or verification.

## E4. Future Improvements

The following improvements are planned for future development, in priority order:

| Priority | Future Improvement | Reason |
|---|---|---|
| High | Expand automated test coverage | To improve reliability and detect errors in critical features. |
| High | Complete and test group permissions | To ensure correct access control for group members. |
| High | Strengthen security testing | To identify authentication and authorization vulnerabilities. |
| High | Improve session management | To provide more reliable session monitoring and revocation. |
| Medium | Improve admin search, filtering, and pagination | To make administration easier with larger datasets. |
| Medium | Add or improve bulk moderation | To reduce repetitive administrative work. |
| Medium | Improve activity and security reporting | To provide administrators with better visibility into system activity. |
| Low | Improve interface and accessibility | To provide a better user experience. |
| Low | Add more career-related features | To expand the usefulness of the platform for students and alumni. |

## E5. References and Tools

### E5.1 Libraries and Frameworks

| Name | Version | Purpose |
|---|---|---|
| Python | 3.13.17 (local environment) | Backend programming language. |
| FastAPI | 0.162.0 | REST API development. |
| React | 19.3.0 | Frontend user interface development. |
| TypeScript | 7.0.2 | Type-safe frontend development. |
| React Router DOM | 7.18.5 | Frontend routing and navigation. |
| Vite | 8.3.2 | Frontend development server and build tool. |
| PyJWT | 2.15.1 | JWT token handling. |
| pwdlib | 0.3.1 | Password hashing using Argon2. |
| Psycopg | 3.3.9 | PostgreSQL database connectivity. |
| SQLAlchemy | 2.1.9 | Database-related Python tooling, where used. |
| python-dotenv | Declared in requirements | Loading environment variables. |
| Pytest | 9.2.0 | Backend automated testing. |
| HTTPX | 0.28.1 | HTTP client and API testing support. |

### E5.2 Development and Deployment Tools

| Tool | Purpose |
|---|---|
| Visual Studio Code | Source code editing and development. |
| Git | Version control. |
| GitHub | Source code hosting and collaboration. |
| Vercel | Frontend and backend deployment. |
| Supabase | Hosted PostgreSQL database. |
| FastAPI Swagger UI | API documentation and endpoint testing. |
| PowerShell | Running development and testing commands. |
| Browser Developer Tools | Inspecting network requests, responses, and application behaviour. |

### E5.3 Documentation and Learning Resources

| Resource | Purpose |
|---|---|
| FastAPI Documentation – https://fastapi.tiangolo.com/ | Backend API development and configuration reference. |
| React Documentation – https://react.dev/ | React component and frontend development reference. |
| TypeScript Documentation – https://www.typescriptlang.org/docs/ | TypeScript language reference. |
| Vite Documentation – https://vite.dev/ | Frontend development and build configuration. |
| PyJWT Documentation – https://pyjwt.readthedocs.io/ | JWT implementation reference. |
| Supabase Documentation – https://supabase.com/docs | PostgreSQL database configuration and management. |
| Vercel Documentation – https://vercel.com/docs | Deployment and environment configuration. |
| GitHub Documentation – https://docs.github.com/ | Repository and version-control workflow reference. |

### E5.4 AI Assistance

ChatGPT by OpenAI was used as an AI-assisted development and learning tool for:

- Understanding programming concepts and debugging errors.
- Reviewing implementation approaches and project structure.
- Preparing documentation and project-report sections.
- Understanding API behaviour, authentication, and deployment-related issues.

The project code, commands, application behaviour, and test results were checked by the developer during implementation and testing. AI-generated suggestions were reviewed and adapted before being used.

---

# Appendix

## A. Video Demonstration

**Video Demonstration Link:**

https://drive.google.com/file/d/1PLEtf4QxfoR-paQ_TP7XyGeQNLr8Odh3/view?usp=drive_link

The demonstration video presents the deployed application and explains its main functionality, including user login, career post management, administrative operations, and relevant security behaviour.

## B. Demonstration Test Accounts

The following table is reserved for the PDF report only. Use actual non-sensitive demonstration accounts and verify their roles before submission.

| User ID / Email | Password | Role |
|---|---|---|
| [Actual Admin Account 1] | [PDF ONLY] | Admin |
| [Actual Admin Account 2] | [PDF ONLY] | Admin |
| [Actual Normal User 1] | [PDF ONLY] | User |
| [Actual Normal User 2] | [PDF ONLY] | User |
| [Actual Normal User 3] | [PDF ONLY] | User |

**Security Notice:** These accounts must contain demonstration data only. Their credentials must never be added to the public Markdown file, README, source code, or GitHub repository.

## C. Group and Member Permissions

**Group Members:** None confirmed for the final demonstration.

The project contains initial group creation and member-management development. Complete group permission assignment and enforcement have not been fully verified. Only actual implemented and verified group permissions should be documented here.

## D. Conclusion

IUBLink CareerHub was developed as a web-based career management platform to support career-related interactions and information sharing.

The project combines a React and TypeScript frontend with a Python FastAPI backend and a PostgreSQL database. It provides a structured environment for managing career-related posts and administrative activities.

The application includes user authentication, career post management, administrative functionality, and security-related mechanisms such as JWT authentication, password hashing, refresh-token functionality, and role-based authorization.

The project provided practical experience in full-stack development, REST API integration, database management, authentication, version control, automated testing, and cloud deployment.

Although further testing and improvements are required in some areas, the project establishes a foundation for future development of a more complete career management platform.

---

**End of Report**

Independent University, Bangladesh  
Department of Computer Science & Engineering  
CSE309 – Web Application & Internet  
Autumn 2026
