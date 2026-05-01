# Before/After Refactors

## What Makes a Great Refactor
- Smaller than the original
- More readable
- More testable
- Less coupled
- No behavior change
- One logical change per commit

## Refactor Patterns
| Smell | Before | After |
|-------|--------|-------|
| Long Method | 200-line function | 5 x 20-line functions |
| God Class | 1000-line class | 5 focused classes |
| Switch Statement | if/else chain | Polymorphism |
| Primitive Obsession | String phone number | PhoneNumber class |
| Feature Envy | Class A using Class B's data | Move method to B |

## Resources
| Resource | URL |
|----------|-----|
| Refactoring.com (Martin Fowler) | https://refactoring.com/ |
| Source Making Refactoring | https://sourcemaking.com/refactoring |
| Work Effectively with Legacy Code | https://www.goodreads.com/book/show/44919.Working_Effectively_with_Legacy_Code |
