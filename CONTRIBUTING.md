# Contributing

Thanks for helping improve API Tracker.

## Local setup

1. Clone the repository
2. Create a Python virtual environment
3. Install backend dependencies with `pip install -r requirements.txt`
4. Install frontend dependencies with `cd frontend && npm install`
5. Run the backend and frontend locally

## Development guidelines

- Keep the app local-first
- Do not add persistence for prompts, responses, or API keys
- Prefer small, focused pull requests
- Add or update tests for behavior changes
- Keep UI changes consistent with the existing dashboard style

## Useful commands

```bash
pytest -q
cd frontend
npm run test -- --run
npm run build
```

## Pull requests

- Describe the change clearly
- Link related issues if any
- Include screenshots for UI changes
- Mention any migration or data impact

## Contribution policy

- Changes should go through pull requests
- Enable branch protection rules in GitHub so direct pushes to `main` are blocked
- Require at least one review before merge
- Maintainers can review and merge once checks pass
