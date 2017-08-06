# FeedGoo
2
Raspberry Pi-powered cat feeder written in Python that operates a high-torque servo-powered cereal dispenser (the kind you find in hotels) to deposit food down a pipe into a bowl to a smiling cat.
3
​
4
To run the script, do the following: 
5
​
6
```
7
python feedgoo.py
8
```
9
​
10
And it'll wait until the scheduled times to operate the servo. I recommend adding the script to your crontab @reboot so even if your Pi loses power, upon start-up, it'll resume the feeding schedule. To do that, add the following line to your crontab:
11
​
12
```
13
@reboot python /home/mhadpi/FeedGoo/v1/feedgoo.py &
14
```
15
​
16
Uses [schedule](https://github.com/dbader/schedule) to operate the servo at the designated times. Very powerful scheduler that doesn't rely on cron.
17
​
18
If you notice that the schedule isn't operating correctly and you want to trigger the servo immediately on an ad hoc basis, do the following:
19
​
20
```
21
python man_feedgoo.py
22
```
23
​
24
The above command just calls the manual_feed() routine to call the feed_goo() routine not on a schedule. 
25
​
26
Both feedgoo.py and man_feedgoo.py write to feedgoo.log to /var/log/feedgoo/ directory.
27
​
28
## Future Versions
29
Refer to the [Wiki](https://github.com/mhaddy/FeedGoo/wiki)!
30
​
31
# Contact
32
Ryan Matthews<br />
33
http://www.maddogstudios.net<br />
34
mhaddy@maddogstudios.net
35
​
36
# Credits
37
Heavily inspired by the project by similar name from David M. N. Bryan, dave@drstrangelove.net<br />
38
URL: http://drstrangelove.net/2013/12/raspberry-pi-power-cat-feeder-updates/
39
​
40
