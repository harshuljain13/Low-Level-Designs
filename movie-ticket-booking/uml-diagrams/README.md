# Movie Ticket Booking System - UML Diagrams

This directory contains comprehensive UML class diagrams for the Movie Ticket Booking System in both Markdown and PNG formats.

## 📁 Files Overview

### 📄 Markdown Files (Mermaid Source)
- **`01_movie_system.md`** - Movie class and enums
- **`02_screen_hierarchy.md`** - Screen inheritance hierarchy  
- **`03_seat_hierarchy.md`** - Seat management with Factory pattern
- **`04_pricing_strategy.md`** - Strategy pattern for pricing
- **`05_user_hierarchy.md`** - User management with inheritance
- **`06_core_business_classes.md`** - Core business classes (Theatre, Show, SeatLayout)
- **`07_manager_classes.md`** - Service layer manager classes
- **`08_complete_system.md`** - Complete system integration

### 🖼️ PNG Image Files
- **`01_movie_system.png`** - Movie system visualization
- **`02_screen_hierarchy.png`** - Screen hierarchy visualization
- **`03_seat_hierarchy.png`** - Seat hierarchy visualization
- **`04_pricing_strategy.png`** - Pricing strategy visualization
- **`05_user_hierarchy.png`** - User hierarchy visualization
- **`06_core_business_classes.png`** - Core business classes visualization
- **`07_manager_classes.png`** - Manager classes visualization
- **`08_complete_system.png`** - Complete system visualization

### 🔧 Mermaid Source Files (.mmd)
- **`01_movie_system.mmd`** - Mermaid source for movie system
- **`02_screen_hierarchy.mmd`** - Mermaid source for screen hierarchy
- **`03_seat_hierarchy.mmd`** - Mermaid source for seat hierarchy
- **`04_pricing_strategy.mmd`** - Mermaid source for pricing strategy
- **`05_user_hierarchy.mmd`** - Mermaid source for user hierarchy
- **`06_core_business_classes.mmd`** - Mermaid source for core business classes
- **`07_manager_classes.mmd`** - Mermaid source for manager classes
- **`08_complete_system_simplified.mmd`** - Mermaid source for complete system

### 🛠️ Utility Files
- **`generate_images.sh`** - Script to regenerate all PNG images
- **`README.md`** - This documentation file

## 🎯 How to Use

### Viewing Diagrams
1. **PNG Images**: Open any `.png` file to view the diagram
2. **Markdown Files**: View in GitHub/GitLab to see interactive Mermaid diagrams
3. **Mermaid Files**: Use with Mermaid-compatible tools for editing

### Regenerating Images
```bash
# Make the script executable
chmod +x generate_images.sh

# Generate all PNG images
./generate_images.sh
```

### Individual Image Generation
```bash
# Generate a specific diagram
mmdc -i 01_movie_system.mmd -o 01_movie_system.png

# Generate with custom theme
mmdc -i 01_movie_system.mmd -o 01_movie_system.png -t dark
```

## 🏗️ Design Patterns Demonstrated

### 1. **Strategy Pattern** (04_pricing_strategy)
- Flexible pricing algorithms
- Runtime strategy selection
- Easy extension with new pricing rules

### 2. **Factory Pattern** (03_seat_hierarchy, 05_user_hierarchy)
- Encapsulated object creation
- Type-safe instantiation
- Centralized creation logic

### 3. **Abstract Class Pattern** (02_screen_hierarchy, 03_seat_hierarchy, 05_user_hierarchy)
- Common interfaces and behavior
- Forced implementation of specific methods
- Code reuse through inheritance

### 4. **Composition Pattern** (07_manager_classes)
- Service layer relationships
- Separation of concerns
- Loose coupling between components

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

## 📊 System Architecture

### Layer Separation
1. **Domain Layer**: Movie, Screen, Seat, User, Theatre, Show
2. **Service Layer**: TheatreManager, ShowManager, BookingManager
3. **Factory Layer**: SeatFactory, UserFactory, PricingStrategyFactory

### Responsibility Distribution
- **TheatreManager**: High-level theatre and show management
- **ShowManager**: Show scheduling and validation logic
- **BookingManager**: Seat booking and availability management

## 🎯 Key Features

1. **Encapsulation**: Private attributes with public properties
2. **Inheritance**: Code reuse through class hierarchies
3. **Polymorphism**: Different implementations of abstract methods
4. **Abstraction**: Abstract classes defining interfaces
5. **Single Responsibility**: Each class has one clear purpose
6. **Open/Closed Principle**: Easy to extend without modification
7. **Dependency Inversion**: High-level modules don't depend on low-level modules

## 📝 Usage Examples

### Viewing in Different Tools
- **GitHub/GitLab**: Markdown files render Mermaid diagrams automatically
- **VS Code**: Install Mermaid extension for live preview
- **Mermaid Live Editor**: Copy `.mmd` content for editing
- **Documentation**: Use PNG files in presentations and documents

### Customization
- Edit `.mmd` files to modify diagrams
- Use `generate_images.sh` to regenerate PNG files
- Customize themes with Mermaid CLI options

## 🔧 Technical Details

### Image Generation
- **Tool**: Mermaid CLI (mmdc)
- **Format**: PNG with transparent background
- **Resolution**: High quality for documentation
- **Size**: Optimized for web and print

### File Organization
- **Source**: `.mmd` files contain Mermaid syntax
- **Documentation**: `.md` files contain descriptions
- **Output**: `.png` files for easy viewing
- **Scripts**: Shell scripts for automation

This directory provides a complete visual representation of the Movie Ticket Booking System architecture, suitable for documentation, presentations, and development reference. 