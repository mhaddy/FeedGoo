# FeedGoo
Raspberry Pi-powered cat feeder written in Python that operates a high-torque servo-powered cereal dispenser (the kind you find in hotels) to deposit food down a pipe into a bowl to a smiling cat.

To run the script, do the following: 

```
python feedgoo.py
```

And it'll wait until the scheduled times to operate the servo. I recommend adding the script to your crontab @reboot so even if your Pi loses power, upon start-up, it'll resume the feeding schedule. To do that, add the following line to your crontab:

```
@reboot python /home/mhadpi/FeedGoo/v1/feedgoo.py &
```

Uses [schedule](https://github.com/dbader/schedule) to operate the servo at the designated times. Very powerful scheduler that doesn't rely on cron.

Writes to feedgoo.log to /var/log/feedgoo/ directory.

## Future Versions
1. Twitter integration for feed notifications (leverage log file)
2. Hook into the python Astral library to identify sunrise and sunset to feed your cat at that time. 
3. Suggest something!

# Contact
Ryan Matthews<br />
http://www.maddogstudios.net<br />
mhaddy@maddogstudios.net

# Credits
Heavily inspired by the project by similar name from David M. N. Bryan, dave@drstrangelove.net<br />
URL: http://drstrangelove.net/2013/12/raspberry-pi-power-cat-feeder-updates/

