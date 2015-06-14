autobit
--------

A IRC/ZNC focused torrent downloader and uploader.


Planned Features
================

- [ ] Generic auto uploader function for popular trackers, simple to extend.
- [ ] IRC Based auto downloading of matched torrent filters
- [ ] IRC Notifications / Log messages
- [x] ZNC Module (python3)
- [ ] Remote adding of torrents over API

Requirements
============

- ZNC w/python3 module support compiled in. You must check, as there is a good chance
this will not be there by default on your system.
- Python 3.4+ (3.3 w/enum pkg)


Configuration
=============

Create your own settings.py (or whatever.py) file somewhere. ~/.config/autobit/settings.py is
the default location. Place any configuration overrides from the autobit/settings.py defaults
 you want in this new config file. You only need to add values that you have changed from the
 defaults. All existing values will be left as-is.

New Trackers
============

To create a new tracker, you must simply subclass the autobit.trackers.Tracker class with
your own implementation. The abc module is used to enforce the inheritance conformity, so
you must be sure to satisfy its requirements.

Contributions of new trackers must at minimum include functionality to parse IRC messages
and perform the download functionality before it will be accepted. The upload method should
raise a NotImplementedError() if the functionality is not yet implemented.
