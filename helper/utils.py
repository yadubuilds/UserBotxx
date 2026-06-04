import time, asyncio 
from datetime import timedelta, date ,datetime 
from pyrogram import enums, filters
from config import Config


def humanbytes(size):
    if not size: return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'ᴋ', 2: 'ᴍ', 3: 'ɢ', 4: 'ᴛ'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'ʙ'


def get_time(seconds):
    periods = [('ᴍᴏ', 86400), ('ʜ', 3600), ('ᴍ', 60), ('ꜱ', 1)]
    result = ''
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            result += f'{int(period_value)}{period_name}'
    return result
   
 
def today_date():
    today = date.today() 
    pattern = '%d-%m-%Y'
    return today.strftime(pattern)
	
	
def get_date(days):
    today = date.today()
    ex_date = today + timedelta(days=int(days))
    pattern = '%Y-%m-%d'
    epcho = int(time.mktime(time.strptime(str(ex_date), pattern)))
    normal_date = datetime.fromtimestamp(epcho).strftime('%d-%m-%Y')
    return epcho, normal_date

def get_date_for_contact(days):
    today = date.today()
    ex_date = today + timedelta(days=int(days))
    pattern = '%Y-%m-%d'
    epcho = int(time.mktime(time.strptime(str(ex_date), pattern)))
    normal_date = datetime.fromtimestamp(epcho).strftime('%B-%d-%Y')
    return normal_date
        

def check_validity(saved_date):
    today = date.today()
    pattern = '%Y-%m-%d'
    epcho = int(time.mktime(time.strptime(str(today), pattern)))
    expired = saved_date - epcho 
    if expired > 0:
       return False 
    return True

    
def get_months(days):
    # Calculate years
    years = days // 365
    remaining_days = days % 365
    
    # Calculate months
    months = remaining_days // 30
    remaining_days = remaining_days % 30
    
    # Create the result string
    result = []
    if years > 0:
        result.append(f"{years} year{'s' if years > 1 else ''}")
    if months > 0:
        result.append(f"{months} month{'s' if months > 1 else ''}")
    if remaining_days > 0:
        result.append(f"{remaining_days} day{'s' if remaining_days > 1 else ''}")
    
    return " & ".join(result)


async def admin_check(message) -> bool:
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]: return False  
    if not message.from_user: return True
    if message.from_user.id in [777000, 1087968824]: return True
    client = message._client
    chat_id = message.chat.id
    user_id = message.from_user.id
    check_status = await client.get_chat_member(chat_id=chat_id,user_id=user_id)
    admin_strings = [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]
    if check_status.status not in admin_strings: return False
    else: return True

async def admin_filter(filt, client, message):
    return await admin_check(message)


filters.admin = filters.create(admin_filter)
