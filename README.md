# BellaBot
Just a small Discord bot for my friends and I

## Setup & Running Locally

### Prerequisites
- Python 3.8 or higher
- A Discord bot token ([create one here](https://discord.com/developers/applications))

### Installation

#### 1. Clone the repository
```bash
git clone <repository-url>
cd BellaBot
```

#### 2. Create a virtual environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Set up environment variables

Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env  # macOS/Linux
copy .env.example .env  # Windows Command Prompt
```

Then edit the `.env` file and add your Discord bot token:
```
DISCORD_BOT_TOKEN=your_token_here
```

#### 5. Run the bot
```bash
python main.py
```

### Deactivating the virtual environment
When you're done, deactivate the virtual environment:
```bash
deactivate
```
