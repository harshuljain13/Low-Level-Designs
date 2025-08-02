# Movie Ticket Booking System - UML Diagrams

This directory contains comprehensive UML class diagrams for the Movie Ticket Booking System, broken down into logical steps for better understanding.

## 📋 Diagram Overview

### 1. **01_movie_system.md** - Movie System Classes
- **Movie** class with all properties
- **MovieLanguage** and **MovieGenre** enums
- Shows encapsulation and data modeling

### 2. **02_screen_hierarchy.md** - Screen Inheritance
- **Screen** abstract class
- **IMAXScreen** and **ThreeD** concrete implementations
- **ScreenType** enum
- Demonstrates inheritance and abstraction

### 3. **03_seat_hierarchy.md** - Seat Management
- **Seat** abstract class
- **RegularSeat**, **PremiumSeat**, **ReclinerSeat** implementations
- **SeatFactory** for object creation
- **SeatStatus** and **SeatType** enums
- Shows Factory pattern and inheritance

### 4. **04_pricing_strategy.md** - Pricing Strategy Pattern
- **PricingStrategy** abstract class
- Concrete strategies: **Default**, **Holiday**, **StudentDiscount**, **Composite**
- **PricingStrategyFactory**
- Demonstrates Strategy pattern

### 5. **05_user_hierarchy.md** - User Management
- **User** abstract class
- **Customer**, **Admin**, **TheaterManager** implementations
- **UserFactory** for user creation
- **UserRole** and **UserStatus** enums
- Shows inheritance and Factory pattern

### 6. **06_core_business_classes.md** - Core Business Logic
- **Theatre** class with screens and shows
- **Show** class with movie, screen, and pricing strategy
- **SeatLayout** for seat arrangement
- **TheatreStatus** and **ShowStatus** enums
- Shows composition and business relationships

### 7. **07_manager_classes.md** - Service Layer
- **TheatreManager** for theatre operations
- **ShowManager** for show scheduling and validation
- **BookingManager** for seat booking operations
- Demonstrates separation of concerns and composition

### 8. **08_complete_system.md** - Complete System Integration
- **Complete UML diagram** with all classes and relationships
- Shows the entire system architecture
- Demonstrates all design patterns and relationships

## 🏗️ Design Patterns Used

### 1. **Strategy Pattern**
- **PricingStrategy** for flexible pricing algorithms
- Allows runtime selection of pricing strategies
- Easy to extend with new pricing rules

### 2. **Factory Pattern**
- **SeatFactory** for creating different seat types
- **UserFactory** for creating different user types
- **PricingStrategyFactory** for creating pricing strategies
- Encapsulates object creation logic

### 3. **Abstract Class Pattern**
- **Screen**, **Seat**, **User**, **PricingStrategy** as abstract base classes
- Defines common interface and behavior
- Forces subclasses to implement specific methods

### 4. **Composition Pattern**
- **TheatreManager** uses **ShowManager**
- **Theatre** contains **Screen** and **Show** objects
- **Screen** contains **SeatLayout**
- **SeatLayout** contains **Seat** objects

## 🔗 Relationship Types

### Inheritance (Is-A)
- `IMAXScreen <|-- Screen`
- `RegularSeat <|-- Seat`
- `Customer <|-- User`
- `DefaultPricingStrategy <|-- PricingStrategy`

### Composition (Has-A / Owns)
- `Theatre *-- Screen` (Theatre owns Screens)
- `Theatre *-- Show` (Theatre owns Shows)
- `Screen *-- SeatLayout` (Screen owns SeatLayout)
- `SeatLayout *-- Seat` (SeatLayout owns Seats)

### Association (Uses)
- `Show ..> Movie` (Show uses Movie)
- `Show ..> PricingStrategy` (Show uses PricingStrategy)
- `BookingManager ..> Show` (BookingManager works with Show)
- `Seat ..> PricingStrategy` (Seat uses PricingStrategy)

### Factory (Creates)
- `SeatFactory ..> Seat` (SeatFactory creates Seats)
- `UserFactory ..> User` (UserFactory creates Users)
- `PricingStrategyFactory ..> PricingStrategy` (Factory creates Strategies)

## 📊 System Architecture

### Layer Separation
1. **Domain Layer**: Movie, Screen, Seat, User, Theatre, Show
2. **Service Layer**: TheatreManager, ShowManager, BookingManager
3. **Factory Layer**: SeatFactory, UserFactory, PricingStrategyFactory

### Responsibility Distribution
- **TheatreManager**: High-level theatre and show management
- **ShowManager**: Show scheduling and validation logic
- **BookingManager**: Seat booking and availability management

## 🎯 Key Features Demonstrated

1. **Encapsulation**: Private attributes with public properties
2. **Inheritance**: Code reuse through class hierarchies
3. **Polymorphism**: Different implementations of abstract methods
4. **Abstraction**: Abstract classes defining interfaces
5. **Single Responsibility**: Each class has one clear purpose
6. **Open/Closed Principle**: Easy to extend without modification
7. **Dependency Inversion**: High-level modules don't depend on low-level modules

## 📖 How to Use These Diagrams

1. **Start with 01_movie_system.md** to understand basic data modeling
2. **Progress through each diagram** to understand the system incrementally
3. **Use 08_complete_system.md** as a reference for the full architecture
4. **Refer to specific diagrams** when working on particular features

## 🔧 Implementation Notes

- All diagrams use **Mermaid** syntax for compatibility
- Diagrams can be viewed in GitHub, GitLab, or any Mermaid-compatible viewer
- Each diagram focuses on a specific aspect of the system
- Relationships are clearly marked with appropriate UML notation

## 📝 Usage Examples

```python
# Creating a theatre with screens and shows
theatre_manager = TheatreManager()
theatre = Theatre("T001", "Cineplex", "Mumbai", "Address", "123-456-7890", "email@cineplex.com")
theatre_manager.add_theatre(theatre)

# Adding a screen
screen = IMAXScreen("S001", "IMAX Screen 1", 100, 10, [10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
theatre_manager.add_screen("T001", screen)

# Creating and scheduling a show
movie = Movie("M001", "Avengers", 150, MovieLanguage.ENGLISH, MovieGenre.ACTION, 8.5, "2024-01-01", "Director", "Cast", "trailer.com")
show = Show("SH001", movie, screen, datetime.now(), 150, PricingStrategyFactory.create_default_strategy())
theatre_manager.add_show("T001", show)

# Booking seats
booking_manager = BookingManager()
available_seats = booking_manager.get_available_seats(show)
booking_manager.book_seat(show, available_seats[0])
```

This documentation provides a comprehensive overview of the system's architecture and design patterns. 