from pyrogram.types import BotCommand as cmd


class Config:
    API_ID = int(22384016)
    API_HASH = "788d6dd08d04d540420a5d51486e7717"
    BOT_TOKEN = "8615735108:AAEwxvikna4Ooqgqx68A2dDS7NP1GSmzigw"
    BOT_UN = "Kidu_Manager_Bot"
    USER_SESSION = "BAHuvsUAPy4y1r89ki4g5jYOw-XDdH3ZlehWn4qqV-wtkQRTGwmhlFehIMZ9Bqwc2GdSL_7EGwqeTyORxxDlMGeeiN77Ek6TAE0uGfJIw4hID2y8kda-vcqXmUGmjBOApeDyFM5fdKNlDXe3DtwsI3q7L6KIr7bvQ-OC8_kE7hr-A2zlLs5MwyWVqUHITTdQfLYrAVBYJDdUxmm2NT28eDjJHmAHMlV_xYxbeJmDJ00TiNXENTsZOpTZxcOO_URQWZX68MzcrMzesnAPumXkY6TIRDwxj0_As5iWB9z5qyoecwRjygQDMBLG6dzk776Ghg2PV9HPSsDpI2v5b1U9cg6arsXXTgAAAAHFV-cQAA"
    
    ADMINS = [97874787, 8414390244, 7605839632]
    DB_URL = "mongodb+srv://XL1:XL1@xl1.kje85.mongodb.net/?appName=XL1"
    DB_NAME = "Cluster0"
    
    PAYMENT_LOG = int(-1003463007143)
    V_CHANNEL = int(-1003652023623)
    REQUEST_CHANNEL = int(-1002591208971)
    QUICK_REPLY = int(-1003315850874)

    GROUPS = [
        -1002348461967,
    ]
    
    TEST_GRP = [
        -1002339989552, #main (0)
    ]
    
    
    PICS = [
        "https://envs.sh/NQ_.jpg"
    ]
    
    PHOTOS = [
        "https://envs.sh/NQp.jpg",
        "https://envs.sh/NQT.jpg",
        "https://envs.sh/NQA.jpg"
    ]
    
    INVALID_KEY = "The Key Is Invalid!"
    USER_NOT_EXIST = "User ID Not Exist In Db"
    USER_NOT_MATCH = "User Not Match. You Try To Forge The Link"
    LINK_USED = "Your Link Is Already Taken"
    LINK_SUCCESS = "True"

    BOT_CMD = [
        cmd("start", "start the bot"),
        cmd("status", "admin only"),
        cmd("add", "admin only"),
        cmd('group_settings', 'admin only'),
        cmd("clear_exp", "admin only"),
        cmd("del_user", "admin only"),
        cmd("all_users", "admin only"),
        cmd("update", "admin only"),
        cmd("broadcast", "admin only"),
    ]
    
    

class Txt:
    START_TEXT = """Hai {}
    
Choose The Group You Wnat. And Enjoy...."""          

        
    REQ_TEXT = """mallu videos - /start"""
    
    STATS = """--**ʙᴏᴛ ꜱᴛᴀᴛꜱ 🤖**--
ʙᴏᴛ ᴩɪɴɢ: {ping}
ᴜᴩᴛɪᴍᴇ: {uptime}

--**ꜱᴇʀᴠᴇʀ 📡**--
ᴛᴏᴛᴀʟ ᴅɪꜱᴋ: {total}
ᴜꜱᴇᴅ ᴅɪꜱᴋ: {used} ({disk_usage}%)
ꜰʀᴇᴇ ᴅɪꜱᴋ: {free}
ᴛᴏᴛᴀʟ ʀᴀᴍ: {t_ram}  
ᴜꜱᴇᴅ ʀᴀᴍ: {u_ram} ({ram_usage}%)
ꜰʀᴇᴇ ʀᴀᴍ: {f_ram}
ᴄᴩᴜ ᴜꜱᴀɢᴇ: {cpu_usage}% 

--**ᴏᴛʜᴇʀ ᴏɴᴇ ✨️**--
ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ: {total_users}

ᴜᴩʟᴏᴀᴅꜱ: {recv}  
ᴅᴏᴡɴʟᴏᴀᴅꜱ: {sent} """

 
class Color:
    reset = '\033[0m'       # Reset all attributes
    bold = '\033[01m'       # Bold text
    underline = '\033[04m'  # Underlined text

    # Foreground colors
    black = '\033[30m'      # Black
    red = '\033[31m'        # Red
    green = '\033[32m'      # Green
    yellow = '\033[33m'     # Yellow
    blue = '\033[34m'       # Blue
    magenta = '\033[35m'    # Magenta
    cyan = '\033[36m'       # Cyan
    white = '\033[37m'      # White

    # Bright foreground colors
    bright_black = '\033[90m'   # Bright Black
    bright_red = '\033[91m'     # Bright Red
    bright_green = '\033[92m'   # Bright Green
    bright_yellow = '\033[93m'  # Bright Yellow
    bright_blue = '\033[94m'    # Bright Blue
    bright_magenta = '\033[95m' # Bright Magenta
    bright_cyan = '\033[96m'    # Bright Cyan
    bright_white = '\033[97m'   # Bright White

    # Background colors
    bg_black = '\033[40m'    # Black background
    bg_red = '\033[41m'      # Red background
    bg_green = '\033[42m'    # Green background
    bg_yellow = '\033[43m'   # Yellow background
    bg_blue = '\033[44m'     # Blue background
    bg_magenta = '\033[45m'  # Magenta background
    bg_cyan = '\033[46m'     # Cyan background
    bg_white = '\033[47m'    # White background

    # Bright background colors
    bg_bright_black = '\033[100m'   # Bright Black background
    bg_bright_red = '\033[101m'     # Bright Red background
    bg_bright_green = '\033[102m'   # Bright Green background
    bg_bright_yellow = '\033[103m'  # Bright Yellow background
    bg_bright_blue = '\033[104m'    # Bright Blue background
    bg_bright_magenta = '\033[105m' # Bright Magenta background
    bg_bright_cyan = '\033[106m'    # Bright Cyan background
    bg_bright_white = '\033[107m'   # Bright White background
    
    
