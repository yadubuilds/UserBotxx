import logging, os, sys, asyncio, time

from pyrogram import Client, idle, filters
from config import Config, Color

# Get logging configurations
logging.getLogger().setLevel(logging.INFO)

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="ClientManager",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="plugins"),
        )

    async def start(self):
        try:
            await super().start()
            me = await self.get_me()
            self.id = me.id
            self.name = me.full_name
            self.username = me.username
            Config.BOT_UN = me.username
            self.mention = me.mention
            self.uptime = time.time()
            await self.set_bot_commands(Config.BOT_CMD) 
            
            try:
                self.User = Client(name=f"UserBot-ClientManager", session_string=Config.USER_SESSION, plugins=dict(root="user_plugins")) 
                await self.User.start()
              
                self.User.bot = self
                await self.User.send_message('me', 'Started ✓')
            except Exception as e:
                logging.error(Color.bold + f"\n\n{Color.red}User Bot Failed: {e}\n\n{Color.reset}")

            logging.info(Color.bold + f"\n\n{Color.green}@{me.username} is started......\n\n{Color.reset}")
            for id in Config.ADMINS:
                try:  await self.send_message(id, 'restarted ✓')
                except: pass
           
        except Exception as e:
            logging.error(Color.bold + f"\n\n{Color.red} {e}\n\n{Color.reset}")
            if self.is_connected: await self.send_message(5652656279, str(e))
            await asyncio.sleep(10)
            os.system('git pull')
            os.execl(sys.executable, sys.executable, "bot.py")
   
original_command = filters.command
def custom_command(commands, prefixes=None, *args, **kwargs):
    if prefixes is None:
        prefixes = ['.', '/']
    return original_command(commands, prefixes=prefixes, *args, **kwargs)

# Override the filters.command function globally
filters.command = custom_command
Bot().run()    
    
    