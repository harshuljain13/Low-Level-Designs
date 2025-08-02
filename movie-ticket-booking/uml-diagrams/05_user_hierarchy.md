# User Hierarchy UML Diagram

## Step 5: User Management System

```mermaid
classDiagram
    class User {
        <<abstract>>
        -_user_id: str
        -_name: str
        -_email: str
        -_phone: str
        -_password: str
        -_created_at: datetime
        -_status: UserStatus
        -_last_login: datetime
        +user_id: str
        +name: str
        +email: str
        +phone: str
        +status: UserStatus
        +created_at: datetime
        +last_login: datetime
        +update_name(name: str): void
        +update_phone(phone: str): void
        +set_status(status: UserStatus): void
        +record_login(): void
        +get_role()*: UserRole
        +is_active(): bool
    }
    
    class Customer {
        +get_role(): UserRole
    }
    
    class Admin {
        +get_role(): UserRole
    }
    
    class TheaterManager {
        +get_role(): UserRole
    }
    
    class UserFactory {
        +create_user(user_type: UserRole, user_id: str, name: str, email: str, phone: str, password: str): User
    }
    
    class UserRole {
        <<enumeration>>
        CUSTOMER
        ADMIN
        THEATER_MANAGER
    }
    
    class UserStatus {
        <<enumeration>>
        ACTIVE
        INACTIVE
        SUSPENDED
    }
    
    User <|-- Customer
    User <|-- Admin
    User <|-- TheaterManager
    User *-- UserRole : has
    User *-- UserStatus : has
    UserFactory ..> User : creates
```

## Description
This diagram shows the User abstract class with its concrete implementations (Customer, Admin, TheaterManager). The UserFactory uses the Factory pattern to create different types of users. Each user has a role and status, and inherits common functionality from the abstract User class. 