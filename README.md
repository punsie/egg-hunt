# Egg-Hunt-Discord-Bot
A Python Discord Bot example for organising egg hunt events

##### Requirements:
```sh
pip install -r requirements.txt
```
<br />
![image](https://user-images.githubusercontent.com/20566000/230964831-a90575b1-b2ca-4f5c-bf6d-01cedf0cc68a.png)
<br />
# How to start
First you have to modify all variables to suit your needs in configuration.py. <br />

* discord_server_id is the discord server ID <br />
* egg_hunt_admin is the ID of the discord member who can run the command <br />
* DISCORD_TOKEN <br />
* announcement_channel is the channel from where you will run the command <br />
* channel_id_1, channel_id_2, channel_id_3, channel_id_4 - channel IDS where the bot will post eggs

*The code assumes you have some images to go with the Egg Hunt event: <br />
Create a folder called assets and add egg_red.png, egg_blue.png, egg_yellow.png, egg_grey.png, egg_purple.png, egg_green.png <br />
You also need an announcement image egghunt_announcement_image.png.* <br /> <br />

Participants have to react to the initial announcement message. After every reaction by default there is another 60 seconds cooldown while the announcement message waits for others to join by reacting to the message. You can modify the timeout_after_someone_reacts variable.  <br /> <br />

Every participant is inserted into a dictionary called eggs. A participant has to be the first to react to the Egg emoji on the egg messages (after the bot) in order to claim an egg point. <br />
