# ToxBot command docs

## `config`

##### Permissions required: `manage_guild`

Explanation of the config settings:

- `prefix` is the bot's prefix for your guild
- `logs` is the channel if that the bot should log its actions to
- `muted_role` is the role that should be applied to users to mute them
- `ignore` is lists of users/roles/etc to exclude from filtering
  - by default bots and anyone with global `manage_messages` permission (mods) are ignored
- `levels` are the detection levels that should trigger certain events (values accepted are between 0 and 1)
- `mutes` are the durations for how long users should be muted for each category. The longest mute will be selected from the triggered categories. Set to 0 to disable mutes for that catgeory.

### `config reset`

Reset the config back to the default configuration. In YAML format the default config looks like:

```yaml
prefix: "!"

logs: null

muted_role: null

ignore:
  users: []
  roles: []
  channels: []
  categories: []
  bots: true
  mods: true

levels:
  alert:
    toxic: 0.997
    severe_toxic: 0.99
    obscene: 0.997
    insult: 0.997
    threat: 0.997
    identity_hate: 0.8
  delete:
    toxic: 0.999
    severe_toxic: 0.999
    obscene: 0.999
    insult: 0.999
    threat: 0.999
    identity_hate: 0.85
  mute:
    toxic: 0.9995
    severe_toxic: 0.9995
    obscene: 0.9995
    insult: 0.9995
    threat: 0.9995
    identity_hate: 0.85

mutes:
  toxic: 1200 # 20 minutes
  severe_toxic: 2400 # 40 minutes
  obscene: 1200 # 20 minutes
  insult: 1200 # 20 minutes
  threat: 1200 # 20 minutes
  identity_hate: 7200 # 2 hours

dm_on: delete
```

## `config prefix [newPrefix: str]`

Updates the bot's guild prefix if given a new prefix, or sets it to `!` if no prefix is given.

## `config logs [newChannel]`

Updates the bot's log channel for your guild. Removes the log channel if no channel is given. Must be a text channel in your guild.

## `config mute [newMutedRole]`

Updates the bot's muted role for your guild. Removes the muted role if no role is given. Must be a role in your guild.

## `config ignore [<category> [*newValues]]`

Updates the bot's ignore ignore list for the given category. If no args are given resets to the default config. `users`, `roles`, `channels`, and `categories` take mentions or IDs, `bots` and `mods` take either `true` or `false`. If a category is provided but no values are given it resets to the default config for that category.

## `config levels [<action> [<category> [newValue]]]`

Updates the level required for a given action to trigger. If no args are given resets all actions' values to the default config. If no category is given it resets the values for all categories in the given action. If no new value is given it resets the value for the given action-category. Action must be one of `alert`, `delete`, `mute`. Category must be one of `toxic`, `severe_toxic`, `obscene`, `insult`, `threat`, or `identity_hate`. New value must be a number between 0 and 1, 1 essentially disables the action.

## `config mutes [<category> [newValue]]`

Updates how long mutes should last for each detection category. If no category is given resets to the default config. If no new value is given it resets the given category to the default. If the value is set to 0 it disables mutes. Numbers under 30 seconds will be considered as 0. This value is only in seconds.

## `config dm [newAction]`

Updates the action required for the bot to DM a user about the action performed. If no new action is provided resets to the default config. New action must be one of `alert`, `delete`, or `mute`.

DM messages:

- `alert`: "Your message ({message_link}) has been detected for toxicity. Please be careful not to repeat this behaviour."
- `delete`: "Your message in {guild_name} has been deleted as it was detected for toxicity. Please be careful not to repeat this behaviour."
- `mute`: "You have been muted for {time} automatically in {guild_name} for toxicity. Please be careful not to repeat this behaviour."

##### Note: custom DM messages are a planned feature but are not currently implemented.

---

### `cases <member>`
##### Permissions required: `manage_messages`

Display recent cases for the given member.

### `case <caseid>`
##### Permissions required: `manage_messages`

Display info for a specific case ID.

### `delcase <caseid>`
##### Permissions required: `manage_guild`

Delete a case by case ID.

### `delcases <member>`
##### Permissions required: `manage_guild`

Delete all cases for a member.

### `about`
##### Permissions required: `manage_messages`

Display information about the bot.