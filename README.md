# Dice of Fire
![Dice of Fire]( https://i.imgur.com/HVvug5a.png)
**Dice of Fire** is telegram bot in which you can play various games, such as: dice, basketball, soccer, bowling, darts, slots.
The bot counts each game, and based on the data of the current game: whether the player won or not, calculates the _"percentage of the top"_. Thus, the top 10 players will go to the _"top rating"_.

## Technology in the project
![My Libraries](https://i.imgur.com/zHslATX.png)

In this project I use the following libraries: **aiogram** *(to implement this in the telegram bot)*, **python-dotenv** *(to take data from the ".env" file)*, **sqlalchemy** *(to manage from the database)*, **pendulum** *(is used to work with date-time)*.

## Interesting code
![inline_btn.py](https://i.imgur.com/bEyPpi5.png)

This file makes it easy to create an inline/reply-keyboard.
- The function *"create_markup"* has mandatory parameters: tip (write "inline" or "reply" for your needs),  row_width (number of columns) and *args. In *args you have to put lists by type: ["button name", "what it should do"].  The second list element by index can be as callback_data - you just need to write which callback_data you pass, or  resource reference in this construction - f "u3l{url}".
- The function *"create_btns"* creates buttons for the tip-keyboard based on the name.

## Bot installation
![Bot installation](https://i.imgur.com/rIFh7k5.png)

 - In order to install your bot based on this, you need to download all
   the files from here. Then create a file *".env"* and write in it this
   
       TOKEN=YOUR_BOT'S_TOKEN
 - In the *"db"* directory, the *"users.db"* file must itself be created when the bot is launched. If not,
   download this file and move it to the new directory *"db"*.
   [Download file](https://drive.google.com/file/d/1zz58bJbsp1DzmLlLIk1SkG8So7e86tul/view?usp=sharing) - [VirusTotal](https://www.virustotal.com/gui/file/763590622a3f17b8802fdf18de7f5a090a45e815178f621a9b8271a4285a7b18)
 - You also need to download the libraries you use. They are in *"requirements.txt"*.
 - In the directory *"data"* file *"config.py"* you must replace the data with your own.
    ```
    import os
	from dotenv import load_dotenv
	
	load_dotenv()
	
	BOT_TOKEN = str(os.getenv("TOKEN"))
	rate = FLOOD_TIME
	admins_id = [Admin_ID]
	support_id = [Supports_ID]
	channel_id = [Channel_ID]
	channel_username = "Channel_USERNAME"
	```
I think that's it.
## Contact
[![Contact](https://i.imgur.com/LLmDfX2.png)](https://t.me/DiceOfFire)
If you still have questions, here's
- [the bot itself](https://t.me/DiceOFire_bot)
- [the official bot's Telegram channel](https://t.me/DiceOfFire)
- [my Telegram](https://lessoleg.t.me)