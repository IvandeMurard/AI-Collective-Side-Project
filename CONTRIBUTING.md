# Contributing to AI Collective Side Project

Thank you for contributing to our AI Collective project! Here are the guidelines to help us work together effectively.

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/IvandeMurard/AI-Collective-Side-Project.git
   cd AI-Collective-Side-Project
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

## Development Workflow

### Branch Strategy
- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/feature-name` - Individual feature branches

### Making Changes
1. Create a new branch from `develop`
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

3. Push and create a Pull Request
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Adding tests

## Code Review Process

1. All changes must go through Pull Requests
2. At least one team member must review before merging
3. Ensure all tests pass before requesting review
4. Address feedback promptly

## Questions?

Feel free to create an issue or reach out to any team member!
