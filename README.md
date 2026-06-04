# Client Manager Bot 

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [File-by-File Analysis](#file-by-file-analysis)
4. [Commands Reference](#commands-reference)
5. [How It Works](#how-it-works)
6. [Setup Instructions](#setup-instructions)
7. [Configuration Guide](#configuration-guide)

---

## Project Overview

**Client Manager** is a Telegram bot system designed to manage user access to private Telegram groups. It provides:
- User subscription management with expiration dates
- Group access control via invite links
- Payment verification system
- Broadcasting capabilities
- Contact management
- Automated group settings management

The bot uses a dual-client architecture:
- **Bot Client**: Handles user interactions and admin commands
- **User Client**: Performs automated tasks like sending messages and managing contacts

---

## Architecture

### Technology Stack
- **Framework**: Pyrogram (PyroFork)
- **Database**: MongoDB (Motor async driver)
- **Language**: Python 3.x
- **Deployment**: Heroku (based on Procfile)

### Project Structure
```
Client-Manager/
├── bot.py                 # Main bot entry point
├── config.py              # Configuration and settings
├── requirements.txt       # Python dependencies
├── helper/
│   ├── database.py        # Database operations
│   └── utils.py           # Utility functions
├── plugins/               # Bot client plugins
│   ├── commands.py        # User-facing commands
│   ├── admin.py           # Admin commands
│   ├── broadcast.py       # Broadcasting functionality
│   ├── callback.py        # Callback query handlers
│   ├── group_settings.py  # Group management
│   ├── send_req.py        # Join request handler
│   └── user_assistant.py  # User assistant features
└── user_plugins/          # User client plugins
    ├── commands.py        # User bot commands
    ├── admin.py           # User bot admin
    ├── broadcast.py       # User bot broadcast
    ├── broadcast_contact.py # Contact-based broadcast
    ├── contact_pdf.py     # Contact PDF generation
    ├── group_broadcast.py # Group member broadcast
    ├── quick_reply.py     # Quick reply management
    ├── send_group.py      # Group link generation
    ├── set_auto_del.py    # Auto-delete settings
    └── raw_test.py        # Testing utilities
```

---

## File-by-File Analysis

### 1. `bot.py` - Main Entry Point

**Purpose**: Initializes and runs the bot client and user client.

**Key Components**:
- `Bot` class extends Pyrogram `Client`
- Initializes bot with API credentials
- Starts user client for automated tasks
- Sets custom command prefixes (`.` and `/`)
- Auto-restart on errors with git pull

**How It Works**:
1. Creates bot client with name "ClientManager"
2. Loads plugins from `plugins/` directory
3. Starts user client with session string
4. Links user client to bot client
5. Sends restart notification to admins
6. Sets bot commands menu

**Key Features**:
- Custom command filter supporting both `.` and `/` prefixes
- Error handling with auto-restart
- Uptime tracking

---

### 2. `config.py` - Configuration File

**Purpose**: Central configuration for all bot settings.

**Sections**:

#### API Configuration
- `API_ID`: Telegram API ID
- `API_HASH`: Telegram API Hash
- `BOT_TOKEN`: Bot token from @BotFather
- `USER_SESSION`: User account session string
- `BOT_UN`: Bot username

#### Admin & Channels
- `ADMINS`: List of admin user IDs
- `PAYMENT_LOG`: Channel ID for payment logs
- `V_CHANNEL`: Channel ID for verification
- `REQUEST_CHANNEL`: Channel ID for join requests
- `QUICK_REPLY`: Channel ID for quick replies

#### Groups
- `GROUPS`: List of group IDs managed by bot
- `TEST_GRP`: Test group IDs

#### Media
- `PICS`: List of photo URLs for start command
- `PHOTOS`: List of photos for view-once messages

#### Database
- `DB_URL`: MongoDB connection string
- `DB_NAME`: Database name

#### Messages
- `INVALID_KEY`: Error message for invalid keys
- `USER_NOT_EXIST`: Error for non-existent users
- `USER_NOT_MATCH`: Error for user mismatch
- `LINK_USED`: Error for used links
- `LINK_SUCCESS`: Success message

#### Bot Commands Menu
- `BOT_CMD`: List of bot commands with descriptions

**Color Class**: ANSI color codes for terminal output

---

### 3. `helper/database.py` - Database Operations

**Purpose**: MongoDB database interface for user and group management.

**Database Class**:

#### User Management Methods:
- `add_user(group_id, user, days)`: Adds user with expiration date
  - Creates validity timestamp and expiration date
  - Sets `link_used` to False
  - Returns user document
  
- `check_user(id, key)`: Validates user access key
  - Checks if ObjectId is valid
  - Verifies user ID matches
  - Checks if link already used
  - Returns status message
  
- `link_used(id, status)`: Updates link usage status
  
- `is_user_exist(id, group_id)`: Checks if user exists
  
- `get_user(id, group_id)`: Retrieves user document
  
- `get_users_by_id(id)`: Gets all user entries for an ID
  
- `total_users_count()`: Counts users per group
  
- `get_all_users()`: Returns all users cursor
  
- `delete_user(id)`: Removes user from database

#### Group Management Methods:
- `add_group(group_id, title, price)`: Adds new group
- `list_groups()`: Lists all groups
- `get_group(key)`: Gets group by ObjectId
- `update_group_id(key, group_id, title, price)`: Updates group ID
- `update_group_title(key, title)`: Updates group title
- `update_group_price(key, price)`: Updates group price

**Database Collections**:
- `users`: Stores user subscriptions
- `groups`: Stores group configurations

---

### 4. `helper/utils.py` - Utility Functions

**Purpose**: Helper functions for formatting and validation.

**Functions**:

- `humanbytes(size)`: Converts bytes to human-readable format (KB, MB, GB, TB)

- `get_time(seconds)`: Formats seconds to readable time (days, hours, minutes, seconds)

- `today_date()`: Returns current date in DD-MM-YYYY format

- `get_date(days)`: Calculates expiration date
  - Returns: (timestamp, formatted_date)
  - Format: YYYY-MM-DD for timestamp, DD-MM-YYYY for display

- `get_date_for_contact(days)`: Formats date for contact names
  - Format: Month-Day-Year (e.g., "January-15-2024")

- `check_validity(saved_date)`: Checks if subscription expired
  - Returns: True if expired, False if valid

- `get_months(days)`: Converts days to years, months, days format

- `admin_check(message)`: Validates if user is admin
  - Checks chat type (group/supergroup)
  - Verifies admin status via Telegram API

- `admin_filter()`: Custom filter for admin-only commands

---

### 5. `plugins/commands.py` - User Commands

**Purpose**: Handles user-facing bot commands.

#### `/start` Command
**Usage**: `/start` or `/start Member_<key>`

**Functionality**:
- Without parameter: Shows welcome message with keyboard
- With `Member_<key>`: Validates and provides group invite link

**Process**:
1. If key provided, validates user access
2. Checks if link already used
3. Creates one-time invite link
4. Sends link to user

**Keyboard Buttons**:
- 📞 Share Contact
- ADMIN ✅
- OFFER 🎁
- 🔰 All Leak Collection
- 🔰 VIP Member
- 🔰 Normal Group
- 🔰 Mallu Only
- ✘ Close

**Error Handling**:
- Invalid key
- User mismatch
- Link already used
- Bot not admin in group

#### Close Keyboard Handler
**Usage**: Click "✘ Close" button

**Functionality**: Removes keyboard and deletes messages

---

### 6. `plugins/admin.py` - Admin Commands

**Purpose**: Administrative commands for bot management.

#### `/status` or `/stats` Command
**Usage**: `/status` (Admin only, private chat)

**Functionality**: Displays comprehensive bot statistics

**Information Shown**:
- Bot ping/latency
- Uptime
- Disk usage (total, used, free, percentage)
- RAM usage (total, used, free, percentage)
- CPU usage percentage
- Total users count
- Network stats (uploads, downloads)

**Output Format**: Markdown formatted message

#### `/restart` Command
**Usage**: `/restart` (Admin only)

**Functionality**: Restarts the bot
- Removes log.txt if exists
- Executes Python script again

#### `/update` Command
**Usage**: `/update` or `/update force` (Admin only)

**Functionality**: Updates bot from git repository
- Pulls latest code from git
- Optionally reinstalls dependencies with `force`
- Restarts bot

**Process**:
1. Removes log.txt
2. Executes `git pull`
3. If force: `pip install -r requirements.txt --force-reinstall`
4. Restarts bot

---

### 7. `plugins/broadcast.py` - Broadcasting System

**Purpose**: Broadcast messages to all users in database.

#### `/broadcast` Command
**Usage**: `/broadcast` or `/broadcast <skip_number>` (Admin only, reply to message)

**Functionality**: Sends message to all registered users

**Process**:
1. Gets all users from database
2. Optionally skips first N users
3. Sends message in batches of 20
4. Updates progress every batch
5. Handles errors (deactivated users, blocked, etc.)

**Error Handling**:
- `FloodWait`: Waits and retries
- `InputUserDeactivated`: Removes from database
- `UserIsBlocked`: Logs but keeps in database
- `PeerIdInvalid`: Removes from database

**Progress Updates**:
- Shows: Total users, Completed, Success, Failed
- Updates every 20 messages
- Final summary with completion time

**Broadcast Function**:
- Copies message to user
- Handles all error cases
- Returns True/False for success

---

### 8. `plugins/callback.py` - Callback Handlers

**Purpose**: Handles inline keyboard button callbacks.

#### Callback Types:

**`close`**: Deletes the message

**`verify+<user_id>`**: Verifies payment and sends link
- Gets user information
- Sends "Link" message to user
- Updates button to "Verified ✅"
- Logs user details

**`reject+<user_id>`**: Rejects payment
- Sends rejection message to user
- Updates button to "Rejected ❌"
- Logs user details

**Error Handling**: Shows alert on errors

---

### 9. `plugins/group_settings.py` - Group Management

**Purpose**: Admin interface for managing groups.

#### `/group_settings` Command
**Usage**: `/group_settings` (Admin only, private chat)

**Functionality**: Shows list of groups with management options

**Process**:
1. Lists all groups from database
2. Shows inline buttons for each group
3. "➕ ADD GROUP ➕" button to add new group

#### Add Group Flow:
1. Click "ADD GROUP"
2. Enter group ID (format: `-100xxxxx`)
3. Enter group title
4. Enter price in ₹
5. Group added to database

**Group Management**:
- View group details (ID, title, price, created date)
- Edit group ID
- Edit group title
- Edit group price

**Callback Data**:
- `add_group`: Start add group process
- `group+<id>`: View group details
- `idedit+<id>`: Edit group ID
- `titleedit+<id>`: Edit group title
- `priceedit+<id>`: Edit group price

---

### 10. `plugins/send_req.py` - Join Request Handler

**Purpose**: Handles channel/group join requests.

#### Join Request Handler
**Trigger**: User requests to join channel/group

**Functionality**:
1. Gets user information via user client
2. Sets auto-delete timer (7 days = 604800 seconds)
3. Logs request

**Auto-Delete**: Sets messages to auto-delete after 7 days

---

### 11. `plugins/user_assistant.py` - User Assistant Features

**Purpose**: Handles business messages and payment verification.

#### Quick Reply System
**Trigger**: Message matches "Kerala Group 😍"

**Functionality**:
- Sends scheduled messages from QUICK_REPLY channel
- Message IDs: [21, 22, 23, 24, 25, 26, 27, 28]
- Schedules with 15-second intervals
- Handles media groups

#### Payment QR Code
**Trigger**: Message matches "Payment Details kerala"

**Functionality**:
- Sends QR code images
- Message IDs: [11, 12]
- Schedules with 5-second intervals

#### Payment Screenshot Handler
**Trigger**: User sends photo in private chat

**Functionality**:
1. Gets user information
2. Forwards to verification channel
3. Adds Accept/Reject buttons
4. Caption includes user details

**User Details Shown**:
- User mention
- User ID
- Username
- Full name

---

### 12. `user_plugins/commands.py` - User Bot Commands

**Purpose**: Commands for user client (self-use).

#### `/g <group_index> <days>` Command
**Usage**: `/g 0 30` (Private, self only)

**Functionality**: Generates user subscription link

**Process**:
1. Gets group ID from Config.GROUPS[index]
2. Adds user to database with expiration
3. Adds user to contacts with expiration date in name
4. Generates bot link with user key
5. Returns link

**Contact Format**: `{expiration_date} | {user_fullname}`

**Link Format**: `https://t.me/{BOT_USERNAME}?start=Member_{database_id}`

#### `/r` Command
**Usage**: `/r` (Private, self only)

**Functionality**: Removes user from group

**Process**:
1. Gets user from database
2. Deletes user from database
3. Removes from contacts
4. Bans and unbans from group (removes from group)
5. Confirms removal

#### `/link <group_index>` Command
**Usage**: `/link 0` (Private, self only)

**Functionality**: Creates direct invite link

**Process**:
1. Gets group from Config.GROUPS[index]
2. Creates one-time invite link
3. Sends user details to payment log channel
4. Returns link

**Payment Log Includes**:
- User name, username, ID, mention
- Group title
- Direct link to user chat

#### `/add <days> <name>` Command
**Usage**: `/add 30 John` (Private, self only)

**Functionality**: Adds contact with expiration

**Process**:
1. Formats expiration date
2. Creates contact name: `{date} |Kerala {name}`
3. Adds to contacts
4. Deletes command message

#### `/sd` Command
**Usage**: `/sd` (Private, self only)

**Functionality**: Sends scheduled message

**Process**:
1. Deletes command
2. Schedules message for 1 minute later
3. Sends predefined text about main group launch

#### `/photo` Command
**Usage**: `/photo` (Private, self only)

**Functionality**: Sends view-once photos

**Process**:
1. Deletes command
2. Sends each photo from Config.PHOTOS
3. All photos are view-once

---

### 13. `user_plugins/admin.py` - User Bot Admin

**Purpose**: Admin commands for user client.

#### `/restart` Command
**Usage**: `/restart` (Self only, private chat)

**Functionality**: Restarts user client

#### `/update` Command
**Usage**: `/update` or `/update force` (Self only, private chat)

**Functionality**: Updates and restarts user client
- Same as bot admin update command
- Works for user client

---

### 14. `user_plugins/broadcast.py` - User Bot Broadcast

**Purpose**: Broadcasting via user client.

#### `/sendall` Command
**Usage**: `/sendall` or `/sendall <skip>` (Admin only, reply to message)

**Functionality**: Broadcasts to all database users via user client

**Difference from bot broadcast**:
- Uses user client instead of bot client
- Same error handling and progress tracking

---

### 15. `user_plugins/broadcast_contact.py` - Contact Broadcast

**Purpose**: Broadcasts to saved contacts.

#### `/sendx` Command
**Usage**: `/sendx` or `/sendx <skip>` (Self only, reply to message)

**Functionality**: Broadcasts to all saved contacts

**Process**:
1. Iterates through all dialogs
2. Filters private chats only
3. Checks if user is in contacts
4. Sends message to contacts
5. Batches of 10 messages
6. Progress updates

**Statistics**:
- Completed count
- Success count
- Failed count
- Skipped count
- Completion time

---

### 16. `user_plugins/contact_pdf.py` - Contact Management

**Purpose**: Contact management and PDF generation.

#### `/c2p` Command
**Usage**: `/c2p` (Self only, private chat)

**Functionality**: Converts contacts to PDF

**Process**:
1. Gets all contacts
2. Creates PDF table with:
   - Count
   - Name
   - Phone Number
   - Username
   - DC Id
   - Unique Id
3. Sends PDF document
4. Deletes PDF file

**PDF Features**:
- Dynamic column widths
- Header row with styling
- Grid borders
- Centered alignment

#### `/c_count` Command
**Usage**: `/c_count` (Self only, private chat)

**Functionality**: Shows total contact count

#### `/rmc` Command
**Usage**: `/rmc` (Self only, private chat)

**Functionality**: Removes contacts without phone numbers

**Process**:
1. Gets all contacts
2. Checks each contact for phone number
3. Deletes contacts without phone
4. Confirms completion

#### `/g2p` Command
**Usage**: `/g2p` (In any chat)

**Functionality**: Converts group members to PDF

**Process**:
1. Gets all chat members
2. Creates PDF with:
   - Count
   - Name
   - Phone
   - Joined Date
   - Username
   - DC Id
   - Unique Id
3. Sends to "me" (saved messages)
4. Deletes PDF file

---

### 17. `user_plugins/group_broadcast.py` - Group Member Broadcast

**Purpose**: Broadcasts to group members.

#### `/chat_broadcast` Command
**Usage**: `/chat_broadcast` or `/chat_broadcast <skip>` (In group/channel, reply to message)

**Functionality**: Broadcasts to all group members

**Process**:
1. Gets all chat members
2. Optionally skips first N members
3. Sends message to each member privately
4. Batches of 10 messages
5. Progress tracking

**Error Handling**: Same as other broadcast functions

**Statistics**: Shows completion, success, failed, skipped counts

---

### 18. `user_plugins/quick_reply.py` - Quick Reply Management

**Purpose**: Manages Telegram quick replies.

#### `/mkn` Command
**Usage**: `/mkn` (In any chat)

**Functionality**: Sends quick reply messages

**Process**:
1. Resolves chat peer
2. Invokes quick reply API
3. Uses shortcut_id = 7
4. Sends empty message array

#### `/get_quick_replys` Command
**Usage**: `/get_quick_replys` (Self only, private chat)

**Functionality**: Lists all quick replies

**Output Format**:
```
Quick Replies:

`7` - 'shortcut_name'
```

---

### 19. `user_plugins/send_group.py` - Group Link Generation

**Purpose**: Test group link generation.

#### `/test <group_index>` Command
**Usage**: `/test 0` (Self only, private chat)

**Functionality**: Creates test group invite link

**Process**:
1. Gets test group from Config.TEST_GRP[index]
2. Checks if user already in group
3. Creates one-time invite link
4. Returns link

**Error Handling**:
- Group not found
- Bot not admin
- User already member

#### `/test_exp <group_id>` Command
**Usage**: `/test_exp -100xxxxx` (Self only, private chat)

**Functionality**: Expires test subscription

**Process**:
1. Bans user from group
2. Notifies user of expiration
3. Removes from group

---

### 20. `user_plugins/set_auto_del.py` - Auto-Delete Settings

**Purpose**: Sets auto-delete timer for users.

#### `/set_auto` Command
**Usage**: `/set_auto` or `/set_auto <skip>` (In group/channel)

**Functionality**: Sets auto-delete for join request users

**Process**:
1. Gets all join requests
2. Optionally skips first N requests
3. Sets auto-delete timer (7 days = 604800 seconds)
4. Batches of 10
5. Progress tracking

**Auto-Delete Time**: 604800 seconds (7 days)

**Error Handling**: 
- Tries to set timer
- If fails, sets to 0 (no auto-delete)
- Handles all standard errors

---

### 21. `user_plugins/raw_test.py` - Testing Utilities

**Purpose**: Raw API testing functions.

#### `/online` Command
**Usage**: `/online` (Self only, private chat)

**Functionality**: Tests quick reply with raw API

**Process**:
1. Deletes command
2. Resolves chat peer
3. Sends message with quick reply shortcut
4. Uses shortcut_id = 7

---

## Commands Reference

### Bot Commands (User-Facing)

| Command | Usage | Description | Access |
|---------|-------|-------------|--------|
| `/start` | `/start` or `/start Member_<key>` | Start bot or validate access | Public |
| `✘ Close` | Button click | Close keyboard | Public |

### Bot Admin Commands

| Command | Usage | Description | Access |
|---------|-------|-------------|--------|
| `/status` or `/stats` | `/status` | View bot statistics | Admin, Private |
| `/restart` | `/restart` | Restart bot | Admin |
| `/update` | `/update` or `/update force` | Update bot from git | Admin |
| `/broadcast` | `/broadcast` (reply) | Broadcast to all users | Admin, Private |
| `/group_settings` | `/group_settings` | Manage groups | Admin, Private |
| `/clear_exp` | `/clear_exp` | Clear expired users | Admin |
| `/del_user` | `/del_user` | Delete user | Admin |
| `/all_users` | `/all_users` | List all users | Admin |
| `/add` | `/add` | Add user | Admin |

### User Bot Commands (Self-Use)

| Command | Usage | Description | Access |
|---------|-------|-------------|--------|
| `/g` | `/g <index> <days>` | Generate subscription link | Self, Private |
| `/r` | `/r` | Remove user from group | Self, Private |
| `/link` | `/link <index>` | Create direct invite link | Self, Private |
| `/add` | `/add <days> <name>` | Add contact | Self, Private |
| `/sd` | `/sd` | Send scheduled message | Self, Private |
| `/photo` | `/photo` | Send view-once photos | Self, Private |
| `/restart` | `/restart` | Restart user client | Self, Private |
| `/update` | `/update` or `/update force` | Update user client | Self, Private |
| `/sendall` | `/sendall` (reply) | Broadcast to all users | Admin, Private |
| `/sendx` | `/sendx` (reply) | Broadcast to contacts | Self, Private |
| `/c2p` | `/c2p` | Convert contacts to PDF | Self, Private |
| `/c_count` | `/c_count` | Count contacts | Self, Private |
| `/rmc` | `/rmc` | Remove contacts without phone | Self, Private |
| `/g2p` | `/g2p` | Convert group to PDF | Any chat |
| `/chat_broadcast` | `/chat_broadcast` (reply) | Broadcast to group members | Group/Channel |
| `/mkn` | `/mkn` | Send quick reply | Any chat |
| `/get_quick_replys` | `/get_quick_replys` | List quick replies | Self, Private |
| `/test` | `/test <index>` | Test group link | Self, Private |
| `/test_exp` | `/test_exp <group_id>` | Expire test subscription | Self, Private |
| `/set_auto` | `/set_auto` | Set auto-delete for requests | Group/Channel |
| `/online` | `/online` | Test quick reply API | Self, Private |

---

## How It Works

### User Subscription Flow

1. **Admin Generates Link**:
   - Admin uses `/g <group_index> <days>` command
   - Bot adds user to database with expiration
   - Generates unique link: `https://t.me/{BOT_USERNAME}?start=Member_{database_id}`
   - Adds user to contacts with expiration date

2. **User Accesses Link**:
   - User clicks link or sends `/start Member_<key>`
   - Bot validates:
     - Key is valid ObjectId
     - User ID matches database
     - Link not already used
   - Creates one-time invite link
   - Sends link to user

3. **Link Usage**:
   - User joins group using invite link
   - Link marked as used in database
   - Cannot be reused

4. **Expiration**:
   - Admin can check validity using database
   - Can remove expired users with `/r` command
   - User automatically removed from group

### Payment Verification Flow

1. **User Sends Payment**:
   - User sends payment screenshot as photo
   - Bot forwards to verification channel
   - Adds Accept/Reject buttons

2. **Admin Verification**:
   - Admin clicks "Accept" or "Reject"
   - If accepted: Bot sends link to user
   - If rejected: Bot sends rejection message

3. **Quick Reply System**:
   - User sends "Kerala Group 😍"
   - Bot automatically sends pre-configured messages
   - Messages scheduled with delays

### Broadcasting System

1. **Database Broadcast**:
   - Admin replies to message with `/broadcast`
   - Bot gets all users from database
   - Sends in batches of 20
   - Handles errors automatically
   - Updates progress in real-time

2. **Contact Broadcast**:
   - Admin uses `/sendx` command
   - Bot iterates through saved contacts
   - Sends to all contacts
   - Tracks progress

3. **Group Broadcast**:
   - Admin uses `/chat_broadcast` in group
   - Bot gets all group members
   - Sends privately to each member
   - Tracks statistics

### Group Management

1. **Add Group**:
   - Admin uses `/group_settings`
   - Clicks "ADD GROUP"
   - Enters group ID, title, price
   - Group saved to database

2. **Edit Group**:
   - Click on group in settings
   - Choose what to edit (ID, title, price)
   - Enter new value
   - Updated in database

---

## Setup Instructions

### Prerequisites

1. **Python 3.8+**
2. **MongoDB Database** (MongoDB Atlas or local)
3. **Telegram API Credentials**:
   - API ID and Hash from https://my.telegram.org
   - Bot token from @BotFather
   - User account session string

### Installation Steps

1. **Clone Repository**:
   ```bash
   git clone <repository-url>
   cd Client-Manager
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Settings**:
   - Edit `config.py`
   - Add your API credentials
   - Add admin user IDs
   - Configure group IDs
   - Add MongoDB connection string

4. **Get User Session String**:
   - Use Pyrogram's `generate_session.py` script
   - Or use online session generator
   - Add to `Config.USER_SESSION`

5. **Run Bot**:
   ```bash
   python bot.py
   ```

### Heroku Deployment

1. **Create Heroku App**:
   ```bash
   heroku create your-app-name
   ```

2. **Set Environment Variables** (if using env vars):
   - Add all config values as env vars
   - Update `config.py` to read from env

3. **Deploy**:
   ```bash
   git push heroku main
   ```

4. **Monitor Logs**:
   ```bash
   heroku logs --tail
   ```

---

## Configuration Guide

### Essential Configuration

#### 1. API Credentials
```python
API_ID = 12345678
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
```

#### 2. User Session
```python
USER_SESSION = "your_session_string"
```

#### 3. Admin List
```python
ADMINS = [123456789, 987654321]  # Your Telegram user IDs
```

#### 4. Database
```python
DB_URL = "mongodb+srv://user:pass@cluster.mongodb.net/"
DB_NAME = "your_database_name"
```

#### 5. Groups
```python
GROUPS = [
    -1001234567890,  # Group 1
    -1000987654321,  # Group 2
]
```

#### 6. Channels
```python
PAYMENT_LOG = -1001234567890
V_CHANNEL = -1001234567891
REQUEST_CHANNEL = -1001234567892
QUICK_REPLY = -1001234567893
```

### Optional Configuration

#### Media URLs
```python
PICS = ["https://example.com/image.jpg"]
PHOTOS = ["https://example.com/photo1.jpg"]
```

#### Custom Messages
```python
INVALID_KEY = "Your custom message"
USER_NOT_EXIST = "Your custom message"
```

---

## Security Considerations

1. **Never commit `config.py` with real credentials**
2. **Use environment variables for production**
3. **Keep session strings secure**
4. **Regularly update dependencies**
5. **Monitor bot logs for suspicious activity**
6. **Use strong MongoDB passwords**
7. **Limit admin access to trusted users**

---

## Troubleshooting

### Common Issues

1. **Bot not starting**:
   - Check API credentials
   - Verify MongoDB connection
   - Check Python version

2. **User client fails**:
   - Verify session string is valid
   - Check if user account is active
   - Ensure user client has necessary permissions

3. **Database errors**:
   - Verify MongoDB connection string
   - Check database name
   - Ensure collections exist

4. **Broadcast fails**:
   - Check if bot has permission to message users
   - Verify users haven't blocked bot
   - Check for FloodWait errors

5. **Group link creation fails**:
   - Ensure bot is admin in group
   - Check bot has "Invite Users" permission
   - Verify group ID is correct

---

## Best Practices

1. **Regular Backups**: Backup MongoDB database regularly
2. **Monitor Logs**: Check logs for errors and warnings
3. **Update Regularly**: Keep dependencies updated
4. **Test Commands**: Test commands in test group first
5. **Error Handling**: All commands have error handling
6. **Rate Limiting**: Broadcasting respects Telegram limits
7. **User Privacy**: Handle user data securely

---

## Support

For issues or questions:
1. Check logs for error messages
2. Verify configuration settings
3. Test commands individually
4. Review this manual for command usage

---

## License

This project is proprietary. All rights reserved.

---

**Last Updated**: Based on current codebase analysis
**Version**: 1.0
**Maintained By**: Development Team

