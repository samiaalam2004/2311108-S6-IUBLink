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
