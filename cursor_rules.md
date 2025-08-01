# Cursor Project Rules (Organized)

## 1. Naming Conventions

- Use `snake_case` for variable and function names to follow Python conventions.  
- Capitalize class names using `CamelCase` to distinguish them from other identifiers.  
- Use expressive, unambiguous variable names even if they're longer — clarity beats brevity.  

---

## 2. Code Structure and Layout

- Limit lines to 79 characters to improve readability across editors and environments.  
- Separate top-level functions and classes with two blank lines for clarity.  
- Keep modules focused; if a file exceeds about 300 lines, consider splitting it up.  

---

## 3. Documentation and Readability

- Include a module-level docstring at the top of every file describing its purpose.  
- Write a docstring for every public function, class, and method using [PEP 257](https://peps.python.org/pep-0257/) conventions.  
- Use docstrings, comments, and clear naming to make your code self-explanatory and maintainable.  

---

## 4. Type Safety and Clarity

- Add type annotations to all function parameters and return types for clarity and maintainability.  

---

## 5. Error Handling

- Prefer exceptions over return codes to indicate errors, and always raise specific exception types.  
- Never use `bare except:` blocks — always catch specific exceptions.  

---

## 6. Resource and Security Management

- Use `with` statements for file operations and context-managed resources to avoid leaks.  
- Don’t hardcode credentials, API keys, or secrets — use environment variables or secret managers.  

---

## 7. Logging and Debugging

- Avoid `print()` for logging — use the `logging` module with appropriate log levels.  

---

## 8. Code Cleanliness and Simplicity

- Avoid deep nesting (more than 3 levels) by using early returns or helper functions.  
- Avoid magic numbers by assigning them to named constants with meaningful names.  
- Avoid importing unused modules or symbols to reduce cognitive overhead.  
- Avoid using `*` imports to maintain clarity over namespace contents.  

---

## 9. Idiomatic Python

- Use list comprehensions instead of manual loops for simple list transformations.  

---

## 10. Testing

- Include at least one unit test for each public function or class using a framework like `pytest`.  
- Name test functions starting with `test_` and clearly indicate what they verify.  

---

## 11. Import Organization

- Organize imports into standard library, third-party, and local sections, in that order.  
