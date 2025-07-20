from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
from typing import Optional

class UserRole(Enum):
    """
    Enum for user roles.
    
    OOP Principle: Encapsulation
    - Encapsulates role constants in a type-safe way
    - Prevents invalid role values and provides clear API
    """
    CUSTOMER = "customer"
    ADMIN = "admin"
    THEATER_MANAGER = "theater_manager"

class UserStatus(Enum):
    """
    Enum for user status.
    
    OOP Principle: Encapsulation
    - Encapsulates status constants, preventing magic strings
    - Provides type safety and clear state management
    """
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class User(ABC):
    """
    Abstract base class for all user types.
    
    OOP Principles Demonstrated:
    1. ABSTRACTION: Abstract class defines common interface without implementation details
       - Abstract method get_role() forces subclasses to implement their specific behavior
       - Hides complex internal state management from clients
    
    2. ENCAPSULATION: Private attributes with controlled access
       - Private attributes (prefixed with _) prevent direct access
       - Public properties provide controlled read access
       - Validation methods ensure data integrity
    
    3. INHERITANCE: Base class for specialized user types
       - Common functionality (role management) defined once
       - Subclasses inherit common behavior and add specialized features

    4. OPEN/CLOSED PRINCIPLE: Extends without modifying
       - Adds new user type without changing existing User class
       - System is open for extension, closed for modification

    5. LISKOV SUBSTITUTION PRINCIPLE: Can replace User
       - Behaves correctly in all contexts expecting User
       - Maintains contract defined by parent class
    
    Why this design?
    - Single source of truth for common user behavior
    - Ensures all user types have consistent interface
    - Easy to add new user types without modifying existing code
    """
    
    def __init__(self, user_id: str, name: str, email: str, phone: str, password: str):
        """
        Initialize user with basic information.
        
        OOP Principle: Encapsulation
        - Constructor validates and encapsulates user data
        - Sets up private attributes with proper defaults
        """
        self._user_id = user_id
        self._name = name
        self._email = email
        self._phone = phone
        self._password = password
        self._created_at = datetime.now()
        self._status = UserStatus.ACTIVE
        self._last_login = None
    
    # Getters demonstrate ENCAPSULATION
    @property
    def user_id(self) -> str:
        """
        Get user ID (read-only).
        
        OOP Principle: Encapsulation
        - Provides controlled read access to private attribute
        - Prevents external modification of critical identifier
        """
        return self._user_id
    
    @property
    def name(self) -> str:
        """
        Get user name.
        
        OOP Principle: Encapsulation
        - Controlled access to private data
        """
        return self._name
    
    @property
    def email(self) -> str:
        """
        Get user email.
        
        OOP Principle: Encapsulation
        - Provides read access while protecting internal state
        """
        return self._email
    
    @property
    def phone(self) -> str:
        """
        Get user phone.
        
        OOP Principle: Encapsulation
        - Safe access to private attribute
        """
        return self._phone
    
    @property
    def status(self) -> UserStatus:
        """
        Get user status.
        
        OOP Principle: Encapsulation
        - Returns enum type ensuring type safety
        """
        return self._status
    
    @property
    def created_at(self) -> datetime:
        """
        Get creation timestamp (read-only).
        
        OOP Principle: Encapsulation
        - Immutable access to creation time
        """
        return self._created_at
    
    @property
    def last_login(self) -> Optional[datetime]:
        """
        Get last login timestamp.
        
        OOP Principle: Encapsulation
        - Safe access to optional private attribute
        """
        return self._last_login
    
    # Setters with validation demonstrate ENCAPSULATION with DATA INTEGRITY
    def update_name(self, name: str) -> None:
        """
        Update user name with validation.
        
        OOP Principle: Encapsulation
        - Controlled modification with business rule enforcement
        - Validates input before updating private attribute
        - Protects object invariants (name must be valid)
        """
        if not name or len(name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters long")
        self._name = name.strip()
    
    def update_phone(self, phone: str) -> None:
        """
        Update user phone with validation.
        
        OOP Principle: Encapsulation
        - Ensures data integrity through validation
        - Centralized business logic for phone number rules
        """
        if not phone or len(phone) < 10:
            raise ValueError("Invalid phone number")
        self._phone = phone
    
    def set_status(self, status: UserStatus) -> None:
        """
        Set user status.
        
        OOP Principle: Encapsulation
        - Controlled state management
        - Type safety through enum parameter
        """
        self._status = status
    
    def record_login(self) -> None:
        """
        Record user login timestamp.
        
        OOP Principle: Encapsulation
        - Encapsulates login tracking logic
        - Updates private state through controlled method
        """
        self._last_login = datetime.now()
    
    @abstractmethod
    def get_role(self) -> UserRole:
        """
        Get user role - must be implemented by subclasses.
        
        OOP Principle: Abstraction
        - Abstract method forces subclasses to provide implementation
        - Defines contract without specifying implementation
        - Enables polymorphism (all users have get_role() method)
        
        Why abstract?
        - Each user type has different role
        - Cannot provide meaningful default implementation
        - Ensures all subclasses define their role
        """
        pass
    
    def is_active(self) -> bool:
        """
        Check if user account is active.
        
        OOP Principle: Encapsulation
        - Encapsulates business logic for "active" determination
        - Hides internal status representation from clients
        """
        return self._status == UserStatus.ACTIVE
    
    def __str__(self) -> str:
        """
        String representation for debugging.
        
        OOP Principle: Polymorphism
        - Each subclass will have different role in string representation
        - Calls polymorphic get_role() method
        """
        return f"{self.get_role().value.title()}: {self._name} ({self._email})"
    
    def __repr__(self) -> str:
        """
        Developer-friendly representation.
        
        OOP Principle: Polymorphism
        - Uses class name dynamically (__class__.__name__)
        - Same method works for all subclasses
        """
        return f"{self.__class__.__name__}(id={self._user_id}, name={self._name})"


class Customer(User):
    """
    Customer user type - can browse and book movies.
    
    OOP Principles Demonstrated:
    1. INHERITANCE: Inherits from User base class
       - Gets all common functionality (authentication, status management)
       - Adds customer-specific behavior
    
    2. POLYMORPHISM: Implements abstract method differently
       - Provides customer-specific implementation of get_role()
       - Can be used anywhere User is expected
    
    Why separate class?
    - Customers have specific behaviors and attributes
    - May need customer-specific methods in future
    - Clear separation of concerns
    """
    
    def __init__(self, user_id: str, name: str, email: str, phone: str, password: str):
        """
        Initialize customer.
        
        OOP Principle: Inheritance
        - Calls parent constructor to set up common attributes
        - Extends parent initialization if needed
        """
        super().__init__(user_id, name, email, phone, password)
    
    def get_role(self) -> UserRole:
        """
        Return customer role.
        
        OOP Principle: Polymorphism
        - Concrete implementation of abstract method
        - Same method signature as parent, different behavior
        - Enables treating all users uniformly while getting specific roles
        """
        return UserRole.CUSTOMER


class Admin(User):
    """
    Admin user type - can manage system-wide operations.
    
    OOP Principles Demonstrated:
    1. INHERITANCE: Specialized user type
       - Inherits common user functionality
       - Represents different user category with same interface
    
    2. POLYMORPHISM: Specific role implementation
       - Same method interface as other users
       - Returns admin-specific role
    
    Design Benefits:
    - Admins can be treated as Users in generic contexts
    - Type system can distinguish between user types when needed
    - Easy to extend with admin-specific functionality
    """
    
    def __init__(self, user_id: str, name: str, email: str, phone: str, password: str):
        """
        Initialize admin user.
        
        OOP Principle: Inheritance
        - Leverages parent class initialization
        - Could add admin-specific setup here if needed
        """
        super().__init__(user_id, name, email, phone, password)
    
    def get_role(self) -> UserRole:
        """
        Return admin role.
        
        OOP Principle: Polymorphism
        - Same method signature, admin-specific implementation
        - Supports uniform treatment of all user types
        """
        return UserRole.ADMIN


class TheaterManager(User):
    """
    Theater Manager user type - can manage specific theaters.
    
    OOP Principles Demonstrated:
    1. INHERITANCE: Extends User base class
       - Reuses common user functionality
       - Adds theater management context
    
    2. POLYMORPHISM: Unique role implementation
       - Implements get_role() for theater manager context
       - Maintains User interface contract
    """
    
    def __init__(self, user_id: str, name: str, email: str, phone: str, password: str):
        """
        Initialize theater manager.
        
        OOP Principle: Inheritance
        - Calls parent constructor for common setup
        - Ready for theater-specific attributes if needed
        """
        super().__init__(user_id, name, email, phone, password)
    
    def get_role(self) -> UserRole:
        """
        Return theater manager role.
        
        OOP Principle: Polymorphism
        - Specific implementation for theater manager
        - Enables role-based functionality throughout system
        """
        return UserRole.THEATER_MANAGER


class UserFactory:
    """
    Factory class to create different types of users.
    
    Design Pattern: FACTORY PATTERN
    
    OOP Principles Demonstrated:
    1. ENCAPSULATION: Hides object creation complexity
       - Clients don't need to know specific constructors
       - Centralizes creation logic and validation
    
    2. SINGLE RESPONSIBILITY: Only responsible for user creation
       - Separates creation logic from business logic
       - Easy to modify creation process without affecting users
    
    3. OPEN/CLOSED: Easy to extend with new user types
       - Can add new user types without modifying existing code
       - Follows dependency inversion (depends on abstractions)
    
    Benefits:
    - Consistent validation across all user types
    - Single place to modify creation logic
    - Type safety through enum-driven creation
    - Easy to add new user types
    
    Alternative Design Patterns Considered:
    - Builder: Good for complex objects with many optional parameters
    - Abstract Factory: Overkill for simple user creation
    - Simple Factory chosen for clarity and simplicity
    """
    
    @staticmethod
    def create_user(user_type: UserRole, user_id: str, name: str, email: str, phone: str, password: str) -> User:
        """
        Create user based on user type with basic required information.
        
        OOP Principles:
        1. FACTORY PATTERN: Centralizes object creation
           - Single method to create any user type
           - Hides instantiation complexity from clients
        
        2. TYPE SAFETY: Uses enum for user type
           - Prevents invalid user type creation
           - Compile-time checking of user types
        
        Parameters:
            user_type: Enum specifying which user type to create
            user_id, name, email, phone, password: Common user attributes
        
        Returns:
            User: Concrete user instance (Customer, Admin, or TheaterManager)
        
        Raises:
            ValueError: If validation fails or unsupported user type
        """
        # Validate basic inputs - demonstrates ENCAPSULATION of validation logic
        UserFactory._validate_basic_inputs(user_id, name, email, phone, password)
        
        # Factory logic - demonstrates POLYMORPHISM
        if user_type == UserRole.CUSTOMER:
            return Customer(user_id, name, email, phone, password)
        
        elif user_type == UserRole.ADMIN:
            return Admin(user_id, name, email, phone, password)
        
        elif user_type == UserRole.THEATER_MANAGER:
            return TheaterManager(user_id, name, email, phone, password)
        
        else:
            raise ValueError(f"Unsupported user type: {user_type}")
    
    @staticmethod
    def _validate_basic_inputs(user_id: str, name: str, email: str, phone: str, password: str) -> None:
        """
        Validate basic user inputs.
        
        OOP Principles:
        
        1. DRY PRINCIPLE: Centralized validation
           - All user types use same validation
           - Single place to update validation rules
        
        Why private method?
        - Implementation detail, not part of public interface
        - May change validation logic without affecting clients
        - Encapsulates complex validation rules
        """
        if not user_id or not user_id.strip():
            raise ValueError("User ID cannot be empty")
        
        if not name or len(name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters long")
        
        if not email or '@' not in email:
            raise ValueError("Invalid email format")
        
        if not phone or len(phone) < 10:
            raise ValueError("Invalid phone number")
        
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        

if __name__ == "__main__":
    print("...Testing UserFactory...")
    user = UserFactory.create_user(UserRole.CUSTOMER, 
                                   "1", "John Doe", 
                                   "john.doe@example.com", 
                                   "1234567890", "password")
    admin = UserFactory.create_user(UserRole.ADMIN, 
                                   "1", "John Doe", 
                                   "john.doe@example.com", 
                                   "1234567890", "password")
    theater_manager = UserFactory.create_user(UserRole.THEATER_MANAGER, 
                                   "1", "John Doe", 
                                   "john.doe@example.com", 
                                   "1234567890", "password")
    print(user)
    print(admin)
    print(theater_manager)