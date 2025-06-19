# Unify Berkeley Hackathon

AI agent with browser automation - uses your existing Chrome browser with all your current logins and tabs.

## Quick Start

First update the `.env` file with `OPENAI_API_KEY`. 
Update the `resume.txt` or `resume.pdf` files with your own resume, adjust the job posting you want to apply for, and adjust the prompts in `planning_agent.py` or `computer_agent.py` to craft the best cold email for the job you want to apply for.
Now you can run the following.

```bash
# Install dependencies
uv sync

# If you want to run your local Chrome, run the bash script
./start_chrome_debug.sh

# To run the Agents
uv run -m specialized_agents.planning_agent
```

## Details

The agent connects to your existing Chrome browser via Chrome DevTools Protocol (CDP):

1. Start Chrome with remote debugging enabled on port 9222
2. Agent automatically connects to your existing Chrome session
3. All your current tabs, logins, and extensions remain intact
4. If connection fails, falls back to launching Playwright browser

## Chrome Debug Port

### macOS/Linux:
```bash
# Find Chrome path
which google-chrome || which chrome

# Start Chrome with debug port
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222
```

### Windows:
```bash
# Start Chrome with debug port (adjust path as needed)
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

## Environment

Required:
```env
OPENAI_API_KEY=your_key_here
```

Optional:
```env
CHROME_DEBUG_PORT=9222  # Change debug port if needed
```

## Troubleshooting

- Chrome must be running with remote debugging enabled
- Default debug port is 9222 - change if port is in use
- If connection fails, agent falls back to Playwright browser
