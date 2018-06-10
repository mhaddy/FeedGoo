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

If you notice that the schedule isn't operating correctly and you want to trigger the servo immediately on an ad hoc basis, do the following:

```
python man_feedgoo.py
```

The above command just calls the manual_feed() routine to call the feed_goo() routine not on a schedule. 

Both feedgoo.py and man_feedgoo.py write to feedgoo.log to /var/log/feedgoo/ directory.

## Schema - How to build this
Here's the [Parts List](https://docs.google.com/spreadsheets/d/1Oq6u6sb5ZfjovzqHFOSRNVcbzIy2-sk2-1YNxwCJh-8/edit?usp=sharing) I used to build the cat feeder along with where I purchased the item. Prices, shipping, etc. may vary but all-in, including the Pi, this project ran me CAD$125.

You'll need the schema (pardon the diagram):
![Schema](https://raw.githubusercontent.com/mhaddy/FeedGoo/master/docs/feedgoo.jpg)

## Future Versions
Refer to the [Wiki](https://github.com/mhaddy/FeedGoo/wiki)!

# Contact
Ryan Matthews<br />
http://www.maddogstudios.net<br />
mhaddy@maddogstudios.net

# Credits
Inspired by the project by similar name from David M. N. Bryan, dave@drstrangelove.net<br />
URL: http://drstrangelove.net/2013/12/raspberry-pi-power-cat-feeder-updates/

