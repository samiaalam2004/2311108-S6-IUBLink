# IUBLink — Product Requirements Document (PRD)

## 1. Project Information

- **Project Name:** IUBLink
- **Project Type:** Web Application
- **Course:** CSE309
- **Frontend:** React.js with TypeScript
- **Backend:** FastAPI with Python
- **Document Version:** 1.0

## 2. Introduction

IUBLink is a university networking platform designed to connect current students, alumni, faculty members, and administrators of Independent University, Bangladesh (IUB). The platform aims to support professional networking, mentorship, career opportunities, and alumni engagement through a centralized web application.

## 3. Problem Statement

Students may find it difficult to connect with alumni for career guidance, mentorship, and professional networking. Alumni may also lack a centralized platform to share their professional experiences and career opportunities with current students. IUBLink aims to address these challenges by providing an organized and secure networking platform.

## 4. Project Objectives

- Build a centralized platform for students, alumni, faculty, and administrators.
- Help students discover and connect with alumni.
- Enable students to request mentorship from alumni.
- Allow verified alumni to share job and internship opportunities.
- Support campus and alumni event announcements and registration.
- Protect user information through authentication and role-based access control.

## 5. Target Users

### 5.1 Students
Current IUB students who want to connect with alumni, seek mentorship, and explore career opportunities.

### 5.2 Alumni
Graduates of IUB who want to maintain their professional profiles, mentor students, and share career opportunities.

### 5.3 Faculty
Faculty members who want to engage with alumni and manage relevant events or mentorship activities.

### 5.4 Administrators
Authorized personnel responsible for user management, alumni verification, and platform moderation.

## 6. Proposed Solution

IUBLink will provide a centralized web interface where users can access features according to their assigned roles. Students can explore alumni profiles and submit connection or mentorship requests. Verified alumni can respond to requests and publish opportunities. Faculty members can manage relevant events, while administrators oversee user verification and platform activities.

## 7. Core Features

1. User registration and login.
2. Role-based dashboards.
3. Profile creation and updating.
4. Alumni directory with search and filters.
5. Connection request management.
6. Mentorship request management.
7. Job and internship opportunity posting and browsing.
8. Event creation and registration.
9. Alumni verification and content moderation.
10. Secure role-based access to application features.

## 8. User Roles and Responsibilities

| Role | Main Responsibilities |
|---|---|
| Student | Manage profile, search alumni, request connections and mentorship, browse opportunities, register for events |
| Alumni | Manage professional profile, handle connection and mentorship requests, publish opportunities |
| Faculty | Browse alumni, create or manage authorized events and mentorship activities |
| Admin | Manage users, verify alumni, moderate content, manage roles and permissions |

## 9. Project Scope

### 9.1 In Scope

- Secure registration and login.
- Student, alumni, faculty, and admin roles.
- Alumni profile directory and search.
- Connection and mentorship requests.
- Job and internship opportunity management.
- Event management and registration.
- Administrative verification and moderation.
- REST API integration between frontend and backend.

### 9.2 Out of Scope

- Real-time chat and video calling.
- AI-based alumni recommendations.
- Online payment processing.
- Mobile application development.
- Real-time notifications through external messaging services.

## 10. Expected Outcomes

IUBLink is expected to provide an organized platform for alumni networking, mentorship, career opportunity sharing, and university community engagement. The project will also demonstrate a complete web application with REST APIs, authentication, authorization, role-based access control, and secure frontend-backend integration.

## 11. Success Criteria

- Users can log in and access features allowed by their roles.
- Students can search alumni and submit requests.
- Alumni can manage requests and publish opportunities.
- Faculty can manage authorized events.
- Administrators can verify alumni and manage users.
- Unauthorized users cannot access restricted resources.
- The React frontend communicates successfully with the FastAPI backend.

## 12. Technology Stack

- Frontend: React.js and TypeScript
- Backend: FastAPI and Python
- Database: PostgreSQL
- API Style: REST
- Authentication: JWT-based authentication
- Security: Password hashing, RBAC, and permission scopes

  ## 13. User Stories

The following user stories describe the main requirements of IUBLink from the perspective of its different user roles.

### 13.1 Student User Stories

- As a student, I want to create and update my profile so that alumni and other users can learn about my academic background and interests.
- As a student, I want to search and filter the alumni directory so that I can find alumni from relevant departments or professional backgrounds.
- As a student, I want to send connection requests to alumni so that I can expand my professional network.
- As a student, I want to request mentorship from alumni so that I can receive career guidance and professional advice.
- As a student, I want to browse job and internship opportunities so that I can explore career options.
- As a student, I want to view and register for events so that I can participate in university and alumni activities.

### 13.2 Alumni User Stories

- As an alumnus, I want to create and maintain my professional profile so that current students can learn about my experience.
- As an alumnus, I want to respond to connection requests so that I can build professional relationships with students.
- As an alumnus, I want to review mentorship requests so that I can guide students.
- As an alumnus, I want to publish job and internship opportunities so that I can help students find career opportunities.
- As an alumnus, I want to participate in university events so that I can remain connected with the IUB community.

### 13.3 Faculty User Stories

- As a faculty member, I want to view alumni profiles so that I can maintain academic and professional connections.
- As a faculty member, I want to create and manage authorized events so that students and alumni can participate in university activities.
- As a faculty member, I want to support mentorship activities so that students can receive academic and career guidance.

### 13.4 Administrator User Stories

- As an administrator, I want to manage user accounts so that the platform remains organized and secure.
- As an administrator, I want to verify alumni accounts so that only legitimate alumni can access alumni-specific features.
- As an administrator, I want to manage user roles and permissions so that users can access only authorized features.
- As an administrator, I want to moderate platform content so that inappropriate or misleading information can be controlled.

## 14. Project Milestones

The development of IUBLink will be organized into the following milestones:

### Milestone 1: Project Planning and Requirements Analysis

- Define the project objectives and scope.
- Identify the target users and their requirements.
- Prepare the Product Requirements Document (PRD), Software Requirements Specification (SRS), and Technical Design Document (TDD).

**Expected Deliverable:** Approved project requirements and documentation.

### Milestone 2: UI/UX Design and System Architecture

- Design the application interface and user navigation.
- Plan the frontend and backend architecture.
- Design the database structure and REST API endpoints.
- Define user roles and access permissions.

**Expected Deliverable:** UI/UX designs and system architecture plan.

### Milestone 3: User Authentication and Profile Management

- Implement user registration and login.
- Implement JWT-based authentication.
- Develop role-based dashboards.
- Implement profile creation and updating.

**Expected Deliverable:** Working authentication and user profile modules.

### Milestone 4: Core Networking Features

- Develop the alumni directory with search and filters.
- Implement connection request management.
- Implement mentorship request management.
- Apply role-based access control to relevant features.

**Expected Deliverable:** Functional alumni networking and mentorship modules.

### Milestone 5: Career Opportunities and Event Management

- Implement job and internship opportunity posting and browsing.
- Develop event creation and management.
- Implement event registration.
- Connect frontend components with backend APIs.

**Expected Deliverable:** Functional career opportunity and event management modules.

### Milestone 6: Administration, Testing, and Deployment

- Implement alumni verification and content moderation.
- Complete user and permission management.
- Test authentication, authorization, and major application features.
- Fix identified bugs and improve application reliability.
- Prepare the final project demonstration and documentation.

**Expected Deliverable:** Tested and documented IUBLink web application ready for demonstration or deployment.
