# FeedGoo
Raspberry Pi-powered cat feeder written in Python that operates a high-torque servo-powered cereal dispenser (the kind you find in hotels) to deposit food down a pipe into a bowl to a smiling cat. Pics are posted to Twitter, of course. Uses [Cronitor](https://www.cronitor.io) to monitor whether feedings are occurring per schedule.

Add the following line to your crontab (adjust timing as necessary) to schedule your feedings:

```
20 10,22 * * * /home/USER/FeedGoo/v1/man_feedgoo.py
```

If you notice that the schedule isn't operating correctly and you want to trigger the servo immediately on an ad hoc basis, do the following (future versions will include hooks to IFTTT):

```
python man_feedgoo.py
```

Both feedgoo.py and man_feedgoo.py write to feedgoo.log to /var/log/feedgoo/ directory.

## Integrations
There are two services that are called in this script - Twython to post images to Twitter, and Cronitor to monitor the feeding schedule (and alert you if the cat hasn't been fed). You'll need to sign-up for services on both, and then add your Twitter App Key/App Secret/Access Token/Access Token Secret, and Cronitor REST hash to configvars.py.

## Schema - How to build this
Here's the [Parts List](https://docs.google.com/spreadsheets/d/1Oq6u6sb5ZfjovzqHFOSRNVcbzIy2-sk2-1YNxwCJh-8/edit?usp=sharing) I used to build the cat feeder along with where I purchased the item. Prices, shipping, etc. may vary but all-in, including the Pi, this project ran me CAD$125.

You'll need the schema (pardon the diagram):
![Schema](https://raw.githubusercontent.com/mhaddy/FeedGoo/master/docs/feedgoo.jpg)

## Finished Product
When you're done, you could end up with something like this! I mounted the cereal dispenser on an old piece of poplar, and used a router to make room in the back of the wood for the Pi and breadboard when mounted on a wall.

![Finished Product](https://raw.githubusercontent.com/mhaddy/FeedGoo/master/docs/IMG_1687.JPG)

![Back of Wood](https://raw.githubusercontent.com/mhaddy/FeedGoo/master/docs/feedgoo-back.JPG)

### Sidebar
> Initially I had used [schedule](https://github.com/dbader/schedule) to operate the servo at designated times, which is a very powerful scheduler that doesn't rely on cron (if, for example, you didn't have permission to access it). However, after much testing, it wasn't reliable so I've resorted to cron and **no longer use feedgoo.py**.

> I've left the code in the repo if someone wants to take it from here. If you choose the feedgoo.py route, add the following to your crontab and it'll wait until the scheduled times to operate the servo (set to configvars.py). Doing so also ensures that during a power outage, upon start-up, it'll resume the feeding schedule.

```
@reboot python /home/mhadpi/FeedGoo/v1/feedgoo.py &
```

## Future Versions
Refer to the [Wiki](https://github.com/mhaddy/FeedGoo/wiki)!

# Contact
Ryan Matthews<br />
https://ryansb.io<br />
iam@ryansb.io

# Credits
Inspired by the project by similar name from David M. N. Bryan, dave@drstrangelove.net<br />
URL: http://drstrangelove.net/2013/12/raspberry-pi-power-cat-feeder-updates/

