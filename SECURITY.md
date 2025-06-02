# Security Guidelines

## Environment Variables

**NEVER commit API keys or secrets to the repository!**

### Setup Instructions:

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Add your actual API keys to `.env`:
   - OpenAI API Key
   - Anthropic API Key  
   - xAI API Key
   - Google API Key

3. The `.env` file is automatically ignored by git via `.gitignore`

## Protected Files

The following files/patterns are automatically excluded from git:
- `.env` - Environment variables with secrets
- `*.key`, `*.pem` - Certificate and key files
- `secrets/` - Any secrets directory
- `*.db`, `*.sqlite3` - Database files with user data
- `prompts.db` - Application database

## Best Practices

- Always use environment variables for sensitive data
- Never hardcode API keys in source code
- Regularly rotate API keys
- Use minimum required permissions for API keys
- Monitor API usage for unexpected activity

## Local Development

Create your `.env` file with actual values:
```bash
OPENAI_API_KEY=sk-your-actual-key
ANTHROPIC_API_KEY=sk-ant-your-actual-key
XAI_API_KEY=xai-your-actual-key
GOOGLE_API_KEY=your-google-key
```