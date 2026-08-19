# Finger Bang The Poon Tang 2.0

This is a custom discord bot used for anything I would like it to do

> Private bot for selected servers.
> 
[![License: Custom](https://img.shields.io/badge/License-Custom-blue.svg)](LICENSE.md)
[![Last commit](https://img.shields.io/github/last-commit/whxami-yokeo/FingerBangThePoonTang2.0Bot)](https://github.com/whxami-yokeo/FingerBangThePoonTang2.0Bot/commits/main)

## Features

- Moderation commands
- Server utility tools
- Welcome messages or role management
- Custom server configuration
- Voice channel support
- Word Filtering
- Music playing / downloading
- Wikipedia API access
- Reload extensions (events, commands, utils)
- Text-to-speech / translate
- Ticket system
- Database support

## Commands

[ ] = Optional\
< > = Required

| Command                                        | Description                                                                                         | Permission          |
|------------------------------------------------|-----------------------------------------------------------------------------------------------------|---------------------|
| `.help [command]`                              | Shows available commands                                                                            | Everyone            |
| `.ping`                                        | Checks whether the bot is online                                                                    | Everyone            |
| `.wiki <query>`                                | Searches Wikipedia and returns article                                                              | Everyone            |
| `.reply`                                       | Replies to the user who initiated                                                                   | Everyone            |
| `.assign`                                      | Adds 'Member' role to command author                                                                | Everyone            |
| `.unassign`                                    | Removes 'Member' role to command author                                                             | Everyone            |
| `.dm <message>`                                | Takes the message the user types, and sends it to them in a DM                                      | Everyone            |
| `.saytext <language> <message>`                | Takes the message, and language, and speaks the message to the author in a voice channel            | Everyone            |
| `.secret`                                      | Responds to the user if the user has a specific role                                                | Everyone            |
| `.si`                                          | Displays information about the server                                                               | Everyone            |
| `.ui`                                          | Displays information about the user                                                                 | Everyone            |
| `.play <query>`                                | Searches youtube for the requested song, if it is found will join a voice channel and play the song | Everyone            |
| `.q OR .queue`                                 | Displays all songs in queue to be played                                                            | Everyone            |
| `.addmember <member>`                          | Adds a member to the created ticket channel                                                         | Everyone            |
| `.join`                                        | Makes the bot join the author's voice channel                                                       | Bot Admin           |
| `.leave`                                       | Makes the bot leave the author's voice channel                                                      | Bot Admin           |
| `.moveto`                                      | Makes the bot move to the author's voice channel                                                    | Bot Admin           |
| `.pause`                                       | Pauses the currently playing song                                                                   | Bot Admin           |
| `.resume`                                      | Resumes the currently playing song                                                                  | Bot Admin           |
| `.skip`                                        | Skips the currently playing song                                                                    | Bot Admin           |
| `.stop`                                        | Stops music from playing, and clears the queue                                                      | Bot Admin           |
| `.dlsong <query>`                              | Downloads the files locally, in cases where streaming is not theoretical                            | Bot Admin           |
| `.addbannedword <word>`                        | Adds the banned word to the database, and filters all messages for the word                         | Bot Admin           |
| `.bannedwords`                                 | Shows a list of all banned words                                                                    | Bot Admin               |
| `.delbannedword <word>`                        | Deletes a banned word from the database                                                             | Bot Admin               |
| `.sendticketembed`                             | Sends the ticket creation embed                                                                     | Sever Administrator |
| `.clearactivity`                               | Clears the current activity from the bot                                                            | Bot Owner           |
| `.setactivity <activity_type> <activity_name>` | Sets the current activity to the given type and name                                                | Bot Owner           |
| `.shutdown [reason]`                           | Shuts the bot down remotely                                                                         | Bot Owner           |
| `.restart`                                     | Restarts the bot remotely                                                                           | Bot Owner           |
| `.reloadall`                                   | Reloads all dependencies for the bot (events, views, utils, and cogs)                               | Bot Owner           |
| `.reloadcmds`                                  | Reloads cogs (commands)                                                                             | Bot Owner           |
| `.reloadevents`                                | Reloads events                                                                                      | Bot Owner           |
| `.reloadutils`                                 | Reloads utils                                                                                       | Bot Owner           |
| `.reloadviews`                                 | Reloads views                                                                                       | Bot Owner           |

> Command availability may depend on server settings and Discord permissions.

## Permissions

Finger Bang The Poon Tang 2.0 may request permissions depending on enabled features. Grant only
the permissions your server needs.

| Permission               | Why it may be needed                        |
|--------------------------|---------------------------------------------|
| Administrator            | Full use of all available features/commands |

## Support

- Security vulnerabilities: See [SECURITY.md](SECURITY.md)
- Privacy questions or data-deletion requests: See [PRIVACY.md](PRIVACY.md)
- Terms of use: See [TERMS.md](TERMS.md)

Do not post bot tokens, API keys, private logs, personal data, or vulnerability
details in public issues.

## Legal

- [Privacy Policy](PRIVACY.md)
- [Terms of Service](TERMS.md)
- [Security Policy](SECURITY.md)
- [License](LICENSE.md)

This project is not affiliated with, endorsed by, or sponsored by Discord Inc.
Discord is a trademark of Discord Inc.

## Source Availability

This repository is published for display and personal educational review only.
Running, copying, modifying, redistributing, or deploying the source code is
not permitted without prior written permission. See [LICENSE.md](LICENSE.md).

## License

This source code is provided under the
[Display and Educational Use License](LICENSE.md).

You may view the repository for personal, non-commercial educational purposes
only. You may not copy, run, modify, redistribute, deploy, or use this code in
another project without prior written permission from the copyright holder.

© 2026 Eddie Menard. All rights reserved.