# Todoist Task Printer

This project fetches tasks from Todoist, formats them using Claude AI, and sends the formatted output to a thermal printer via PrinterBot.

## How It Works

1. **Environment Setup**:
   - The script uses environment variables for API tokens and printer shortcode.
   - Required variables: `TODOIST_API_TOKEN`, `CLAUDE_API_KEY`, `PRINTER_SHORTCODE`

2. **Fetching Data from Todoist**:
   - Retrieves projects and tasks from Todoist API.
   - Filters tasks based on priority (2, 3, or 4) and completion status.

3. **Organizing Tasks**:
   - Groups tasks by project.
   - Sorts tasks within each project by priority (highest first).

4. **Formatting with Claude AI**:
   - Sends the organized task list to Claude AI.
   - Claude formats the tasks into a JSON structure suitable for printing.

5. **Printing via PrinterBot**:
   - Sends the formatted JSON to PrinterBot's webhook.
   - PrinterBot processes the JSON and prints the tasks.

## Requirements

- Python 3.x
- Required Python packages: `requests`, `python-dotenv`, `anthropic`
- Hardware:
  - [Rongta Thermal Receipt Printer](https://www.amazon.com/gp/product/B0C9QLPSFS/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
  - [USB to Serial Cable](https://www.amazon.com/gp/product/B00NH11KIK/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1)
  - Raspberry Pi 4 (imaged with pbot.img)

## Setup

1. Install required packages:
   ```
   pip install requests python-dotenv anthropic
   ```

2. Create a `.env` file in the project root with the following:
   ```
   TODOIST_API_TOKEN=your_todoist_token
   CLAUDE_API_KEY=your_claude_api_key
   PRINTER_SHORTCODE=your_printerbot_shortcode
   ```

3. Set up the hardware:
   - Purchase and set up the [Rongta Thermal Receipt Printer](https://www.amazon.com/gp/product/B0C9QLPSFS/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
   - Connect the printer to your Raspberry Pi 4 using the [USB to Serial Cable](https://www.amazon.com/gp/product/B00NH11KIK/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1)
   - Image your Raspberry Pi 4 with the pbot.img file from [this Dropbox link](https://www.dropbox.com/s/qozhg9th5vjngih/pbot.img?dl=0)

4. Set up the Raspberry Pi:
   - After imaging the Raspberry Pi, plug it in and wait 5-6 minutes for the PrinterBot WiFi to appear.
   - Connect to the PrinterBot WiFi using the password "password".
   - Input your home network WiFi information.
   - Provide your email address (required to obtain your printer shortcode).
   - Wait for the setup process to complete and note down your printer shortcode.

5. Run the script:
   ```
   python main.py
   ```

## Output

The script will print status messages to the console, including Claude's formatted response and any errors encountered during execution.

## Note

Ensure you have active accounts and valid API keys for Todoist, Anthropic (Claude), and PrinterBot before running the script.