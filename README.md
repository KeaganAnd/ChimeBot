# Chimebot
### A simple to use discord bot running on [discord.py](https://discordpy.readthedocs.io/en/stable/)
*I'd reccomend reading this on Github since Notepad doesn't support markdown*

---
```diff
- **MUST READ ME BEFORE USE**
```

# End User License Agreement (EULA) for ChimeBot

Thank you for downloading ChimeBot! Below are the terms and conditions for using, modifying, and distributing this software.

## **Usage Terms**  
By using this software, you agree to the following:

1. **No Commercial Use** – You are **NOT** allowed to sell any of the included source code, either in full or in part.  
2. **Modification Rights** – You are **free to edit or modify** the code for personal or private use.  
3. **No Unauthorized Redistribution** – You may **NOT** reupload or distribute this project **unless** you have made **significant changes**, such as adding a feature or fixing a bug.  
4. **No False Attribution** – You are **NOT** allowed to claim this source code as your own. Proper credit must be given to the original author.  
5. **No Warranty** – This software is provided **as is**, without any guarantees or liability for damages or data loss. Use at your own risk.  
6. **License Termination** – Any violation of these terms may result in the revocation of your rights to use, modify, or distribute ChimeBot.  

By using this software, you acknowledge that you have read and agreed to these terms.

---

## What ChimeBot does
Chimebot tracks a voice channel within a discord server and send announcements to a text channel of leave and join notifications. It is created to make setup as easy as possible with as little work possible.

---

## Setup

**NOTE**: [Python 3.13.2](https://www.python.org/downloads/) or newer is required to run this bot.

1. **Setting up your developer profile and application**  
   
   If you already have one, you can skip this part.  
   Since you will be setting up your own bot, you will need a Discord developer profile to connect this source code to the Discord Bot API.  

   - Go to [this link](https://discord.com/login?redirect_to=%2Fdevelopers) or search a web browser for 'Discord Developer Portal'.  
   - Then, log in with your Discord account.  
   - On the top right, click the **New Application** button.  
   - Name the bot whatever you'd like and click **Create**.  
   - You should now be in your application. Click on the **Bot** tab on the left side of the screen.  
   - Here, you can change the icon and username to whatever you'd like.  
   - Now, keep this page open while we move on to the next step.  

2. **Getting the bot running**  

   - Open your operating system's terminal.  
     - **Windows**: Press the **Windows key**, search for **cmd**, and open it.  
     - **Mac**: Open **Spotlight**, search for **terminal**, and open it.  

   - Install the Discord library:  
     - **Windows**:  
       ```bash
       pip install discord
       ```
     - **Mac**:  
       ```bash
       pip3 install discord
       ```
   
   - This step downloads the dependency for this program: the `discord.py` library.  
   - Place the downloaded zip wherever you would like to store it and extract it.  
   - Now, run the `bot.py` file in the folder.  
   - You should see a message telling you to configure your API key. Let's do that:  

     1. Go back to your **Discord Developer Portal** under the **Bot** tab.  
     2. Look for a section called **Privileged Gateway Intents**.  
        - Enable all three options underneath and click save. It should look like this
        ![](https://i.imgur.com/eRVkSiE.png)
     3. Look for the section that says **Token**, and click the **Reset Token** button.  
        **Never share this token with anyone!**  
     4. Copy the token.  
     5. Go back to your bot folder and open the newly created `Config.txt`.  
     6. In **line 2**, replace `"YOURAPIKEY"` with the key you just copied.  
