import random
import re

class Facts:
    async def read_facts(self, guild, lang):
        try:
            for channel in guild.channels:
                if channel.name == "nrc":
                    message = await channel.fetch_message(channel.last_message_id)
                    if message.attachments:
                        for attach in message.attachments:
                            await attach.save(str.lower(attach.filename))
                        if lang == "ru":
                            with open('facts_ru.txt', 'r', encoding='utf-8') as file:
                                return random.choice(str.split(file.read(), '\n'))
                        elif lang == "en":
                            with open('facts_en.txt', 'r', encoding='utf-8') as file:
                                return random.choice(str.split(file.read(), '\n'))
                    else:
                        await message.add_reaction('⚠️')
        except:
            print(f'Проблемы с чтением фактов!')

    def find_fact(self, msg):
        english = re.findall(r'\bfact(s)?\W*\b', msg)
        russian = re.findall(r'\bфакт(а|у|ом|е|ы|ов|ам|ами|ах|о)?\W*\b', msg)
        if english:
            return 'en'
        elif russian:
            return 'ru'
        else:
            return False
