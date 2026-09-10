# Content Agent Dashboard

## What this is
A 5-agent content system for Instagram, built for @zunimoveconveyorsystem
(industrial conveyor systems niche). Pulls real Instagram data, runs it
through 5 specialized agents, shows results on a dashboard, and reports
daily to Telegram.

## Accounts
- **Primary account:** @zunimoveconveyorsystem
- **Competitors tracked:** @panther_conveyor_belt, @lbsconveyorbeltsemmen, @farookconveyors

## The 5 Agents
1. **Ideator** — scans own + competitor posts, surfaces content ideas / gaps
2. **Hook & Script** — turns an idea into a hook + short-form script
3. **Planner** — arranges ideas/scripts into a daily posting calendar
4. **Analyst** — reads stats (likes, comments, reach, growth) and reports what's working
5. **DM Manager** — handles/triages incoming DMs (rules-based first, AI-assisted later)

## Architecture
- `scripts/` — data pulling (Apify), agent logic, Telegram sender, scheduler
- `dashboard/` — the UI showing all 5 agents + live stats
- `dashboard/data.json` — the single source of truth: real scraped IG data
- `.env` — API tokens (Apify, Telegram). NEVER hardcode tokens elsewhere.

## Data source
Apify's `instagram-scraper` actor, pulling:
- Full post history for @zunimoveconveyorsystem
- Recent posts for the 3 competitor accounts above

## Status log
- [x] Step 1: Project scaffolded
- [ ] Step 2: Pull real data via Apify
- [ ] Step 3: Build dashboard (5 agents)
- [ ] Step 4: Telegram bot
- [ ] Step 5: Automate / schedule
- [ ] Step 6: Full end-to-end proof run

## Ground rules for anyone (human or AI) working on this
- One step at a time, verify before moving on.
- Never commit or expose .env values.
- Improve existing files instead of replacing them wholesale.
