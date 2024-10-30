from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = "############:########################################"
bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()

DATABASE_PATH = "data/database.db"

ADMIN_USER_IDS = [00000000, 000000000]  # Using a tuple
ADMIN_USERNAMES = ["admin1", "admin2", "admin3"]





help_pages = [
    """
<b>❓ Help Center</b>

Need assistance? We're here to help! Here are some common questions:

-------- Q: How do I check a card? --------  
A: Go to '<i>Check Card</i>' in the main menu and follow the prompts.

========= Q: Is this service legal? =========  
A: Our bot is for educational purposes only. Always comply with local laws.

|||| Q: How accurate are the results? ||||  
A: We strive for high accuracy, but results are not guaranteed.

__===== Q: I found a bug, what should I do? __=====  
A: Please report it to our support team at <code>support@cardchecker.com</code>.

~~~~~~ Q: Can I use this service internationally? ~~~~~~  
A: Yes, but ensure you comply with the regulations of your country.
""",
    """
+++++++++ Q: What types of cards can I check? +++++++++  
A: You can check various card types, including credit and debit cards.

~~~~~ Q: Is there a fee for using this service? ~~~~~  
A: Basic checks are free; premium features may incur charges.

-------- Q: How do I contact support? --------  
A: You can reach our support team via email at <code>support@cardchecker.com</code>.

========= Q: Are my data and privacy protected? =========  
A: Yes, we take privacy seriously and adhere to data protection regulations.

|||| Q: What should I do if I forgot my password? ||||  
A: Use the 'Forgot Password' link on the login page to reset it.
""",
    """
__===== Q: Can I access my history of checks? __=====  
A: Yes, you can view your check history in your account settings.

~~~~~~ Q: What if I encounter an error during a check? ~~~~~~  
A: Try refreshing the page or contacting support if the issue persists.

+++++++++ Q: Are there any usage limits? +++++++++  
A: There may be limits on the number of checks per day for free accounts.

-------- Q: How can I provide feedback? --------  
A: We welcome feedback via disscussion boards at <code>https://github.com/Plug-Outlet/Carding-Guide-Bot/discussions</code>.

========= Q: Is there a mobile app available? =========  
A: Currently, we only offer a web-based service, but an app is in development!
""",
]