# Telegram-bot for rehearsal room
Telegram-bot based on aiogram3 and Google Sheets API V4.

The bot collected basic information in order to start using the rehearsal room, it also serves to book a rehearsal room, view free slots. All changes are recorded in a google spreadsheet.

The architecture of the code is based on the construction of the aiogram library, its own entities, which appeared in addition to the basic ones, are in the "core" package; all handlers, dialog systems (presented as finite automata) are presented in the adapters package; interaction with the storage system is presented in the "store" package and all displays for buttons and timetable are presented in the "view" module.
