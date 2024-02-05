# CEN4020-S24-Team-Blue
InCollege project

## Directory Map:
```
.
├── incollege
|   ├── entity              # Structures
|   ├── repository          # Data Storage Interfacing
|   ├── services            # "Business Logic"
|   ├── controllers         # User Interfacing
|   ├── exceptions          # Custom Errors
|   ├── config              # Configuration Strings
|   └── utils               # Global Utilities
└── tests
    ├── repository
    ├── services
    ├── controllers
    └── utilities
```
#### The "incollege" directory houses the general codebase.
- The "entity" directory is for classes - think "User", "Post", etc. Note that each data type gets its own repository file.
- The "repository" directory houses logic concerning data storage, e.g. file reads/writes, SQL
- The "services" directory should contain logic that lay between the repository and the controller (user). For example, password verification, data validation
- The "controllers" directory allows user interfacing. When the user submits a request, they do so through the control layer
- The "exceptions" directory simply contains any custom exception types.
- The "config" directory is for any configuration information - API tokens, backend preferences, etc.
- The "utils" directory contains all simple classless utilities. For example, a function to convert from base 2 to base 10, or one to remove spaces from a string.
#### The "tests" directory contains testing code.
- Every testable directory within the "incollege" directory will be represented here (all the ones with executing code) and should contain the resources to test every function in the entire project.
- The tests for individual functions are "unit tests" (e.g. does square(2) return 4?).
- Tests for parts of the project working together are "integration tests" (e.g. does app.login(user, pwd) successfully perform all necessary tasks to execute a login operation?). These tests are also responsible for verifying the functionality of the repository layer by simulating data and processing it.