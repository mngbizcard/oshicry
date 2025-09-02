# OshiCRY - Anime Character Appreciation Platform

## Overview

OshiCRY is a social media platform designed for anime fans to share their thoughts and feelings about their favorite characters ("oshi"). The platform allows users to create posts ("cries"), follow works, characters, and other users, and engage with a community centered around anime appreciation. Built with Flask, it features a bilingual interface (English/Japanese) and an anime-inspired purple theme design.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask web application with session-based authentication
- **Data Storage**: In-memory storage using Python dictionaries and global counters for ID generation
- **Session Management**: Flask-Session with filesystem-based storage
- **Password Security**: Werkzeug password hashing utilities
- **Routing**: Centralized route definitions in separate routes module

### Frontend Architecture
- **Template Engine**: Jinja2 templating with base template inheritance
- **Styling Framework**: Bootstrap 5 with custom CSS overrides
- **Theme**: Anime-inspired design with purple gradient color scheme
- **Icons**: Font Awesome for consistent iconography
- **Internationalization**: Built-in translation system supporting English and Japanese

### Data Models
- **User Model**: Handles authentication, user profiles, and following relationships
- **Work Model**: Represents anime series/works with metadata
- **Character Model**: Character entities linked to specific works
- **Post Model**: User-generated content with optional work/character associations

### Authentication & Authorization
- **Session-based Authentication**: Uses Flask sessions for user state management
- **Password Security**: Werkzeug generate_password_hash and check_password_hash
- **User Management**: Registration, login, logout functionality with form validation

### Application Structure
- **Modular Design**: Separate files for models, data management, routes, and application initialization
- **Template Organization**: Base template with extending child templates for different pages
- **Static Assets**: CSS and JavaScript files for styling and client-side functionality

## External Dependencies

### Frontend Libraries
- **Bootstrap 5**: UI framework for responsive design and components
- **Font Awesome**: Icon library for consistent visual elements
- **Custom CSS**: Anime-themed styling with purple gradients and hover effects

### Python Packages
- **Flask**: Core web framework
- **Flask-Session**: Session management extension
- **Werkzeug**: Password hashing and security utilities

### Development Tools
- **Logging**: Built-in Python logging for debugging
- **Debug Mode**: Flask development server with hot reload enabled

Note: The application currently uses in-memory data storage, which means data will not persist between server restarts. This architecture is suitable for development and testing but would need to be replaced with a persistent database solution for production use.