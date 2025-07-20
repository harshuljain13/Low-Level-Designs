# Movie Ticket Booking System - Low Level Design Requirements

## Overview
Design a movie ticket booking system similar to BookMyShow or Fandango. The system should allow users to browse movies, select theaters, choose showtimes, pick seats, and complete bookings with payment processing.

**Core Challenge**: Design a scalable, thread-safe ticket booking platform that handles concurrent seat reservations, prevents double bookings, manages theater capacity, and processes payments reliably.

## Functional Requirements

### 1. Search and Filtering Process
- User browse movies by location, genre, language, rating
- Filter by show timings, price range, seat availability, theatre

### 2. Selection and Booking Process
- User selects the movie and gets a seat map showing what seats are available. Seats are categorized by pricing.
- User selects the seat and places a temporary hold on seats during booking process. (15 min timeout)
- User does the payment and confirming booking. This Generate unique booking Id for reference.

### 3. Payment Processing
- User can have multiple payment methods (Credit/Debit cards, Digital wallets, Net banking)
- User selects one of the available payment methods for booking.

**Extra Requirements to confirm**
- Refund processing for cancellations (REquirement to confirm )
- Promotional codes and discount application

### 4. Booking Management
- View booking history and current bookings
- Cancel bookings (with cancellation policy)

**Extra Requirements to confirm**
- Send booking confirmations via email/SMS

### Entities
- **Users** - Customer, Admin, Theater Manager
- **Seats**: Different categories (Premium, Regular, Recliner) with dynamic pricing
- **Movies**: Title, genre, duration, rating, language, release date, description
- **Theaters**: Name, location, contact info, screens
- **Screens**: Multiple screens per theater with different capacities and types (IMAX, 3D, Regular)
- **Shows**: Movies scheduled at specific times on specific screens

## Key Design Considerations for Interview

### 1. OOPs Principles to Demonstrate
- **Encapsulation**: Proper data hiding and access control
- **Inheritance**: Different types of seats, users, payments
- **Polymorphism**: Multiple payment methods, notification channels
- **Abstraction**: Abstract interfaces for external services

### 2. Design Patterns to Consider
- **Factory Pattern**: Creating different types of seats, bookings
- **Observer Pattern**: Notifying users about booking status changes
- **Strategy Pattern**: Different pricing strategies, payment methods
- **Command Pattern**: Booking operations with undo capability
- **State Pattern**: Booking lifecycle management

### 3. Concurrency & Threading
- Thread-safe seat reservation mechanism
- Handling race conditions in booking process


