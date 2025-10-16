"""
UTILITIES PACKAGE

This package contains helper functions that are used across the application.
These are pure utility functions - they don't depend on Django models or business logic.

EDUCATIONAL NOTE:
Utilities are like a "toolbox" - they contain reusable tools that can be used
anywhere in your application. This is your first step toward code organization!

WHY SEPARATE UTILITIES:
1. REUSABILITY: Use the same function in multiple places
2. TESTABILITY: Test utility functions in isolation
3. CLARITY: Main code focuses on business logic, not implementation details
4. DRY PRINCIPLE: Don't Repeat Yourself

WHEN TO CREATE A UTILITY:
- Pure functions (same input → same output, no side effects)
- Functions used in multiple places
- Functions that don't depend on Django models or request context
"""
