# PersonalAssistant-GoIT

## Installation and Run

Follow these steps to download and run the assistant bot.

### 1. Install as a Python package

You can install the project as a Python package and run it from any location in your system.

Install the package

```
pip install git+https://github.com/AideNaDa/PersonalAssistant-GoIT && assistant-bot
```

After installation you can start the assistant from any directory:

```
assistant-bot
```

---

### 2. Start using the assistant

After launch you will see:

```
Assistant bot started. Type 'hello' to start or 'exit' to quit.
```

Example commands:

```
hello
add John 1234567890
add-note todo "Buy milk" shopping
show-all
show-all-note
exit
```

---

### Data Storage

All contacts and notes are saved automatically to the file:

```
data.json
```

The file will be created automatically after the first run.

---

### Uninstall as a Python package

Uninstall the package

```
pip uninstall assistant-bot
```

---

## Commands Usage

The bot supports managing contacts and text notes. Command parameters are indicated in brackets `[ ]`.

---

### Contact Management

| Command         | Arguments                                                                                                            | Description                                                                                                                                |
| :-------------- | :------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| **`add`**       | `[name]` `<phone> <birthday> <addr:"address"> <email>`                                                               | Creates a new contact. Additional parameters (birthday, addr:address, email) are optional. **The order of the arguments does not matter.** |
| **`birthdays`** | `[num]`                                                                                                              | Displays a list of contacts who have a birthday coming up in the specified number of days (`num`).                                         |
| **`del`**       | `[name]`                                                                                                             | Deletes the contact and all associated data completely.                                                                                    |
| **`del`**       | `[name] [phone]` or `[email]` or `birthday` or `address`                                                             | Deletes a specific field for the selected contact (e.g., only the email or just one of the phone numbers).                                 |
| **`edit`**      | `[name] [old_phone] [new_phone]`<br>or `[old_email] [new_email]`<br>or `[new_birthday]`<br>or `[addr:"new_address"]` | Edits contact details. Overwrites the birthday or address, or replaces an old phone/email with a new one.                                  |
| **`find`**      | `[query]`                                                                                                            | Displays a contact card. Search works by any match: name, phone, address, email, or birthday.                                              |
| **`show-all`**  | _- no arguments -_                                                                                                   | Displays a list of all saved contacts.                                                                                                     |

---

### Note Management

| Command             | Arguments                                                | Description                                                                                                   |
| :------------------ | :------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------ |
| **`add-note`**      | `[title] "[text]" <tag1> <tag2>...`                      | Creates a new note or appends text to existing note with a title and text in "". The tag (`tag`) is optional. |
| **`add-tag`**       | `[title] [tag]` or `[tag1] [tag2]...`                    | Adds one or more tags to an existing note.                                                                    |
| **`del-note`**      | `[title]`                                                | Deletes a note by its title.                                                                                  |
| **`del-note`**      | `[title] [tag1] <tag2>...`                               | Deletes a note tag by its title.                                                                              |
| **`edit-note`**     | `[title] [new_text]`<br>or `[title] [old_tag] [new_tag]` | Changes the main text of a note or replaces an old tag with a new one.                                        |
| **`find-note`**     | `[query]`                                                | Searches for a note by its title or attached tags and displays a listm of all matches.                        |
| **`show-all-note`** | _- no arguments -_                                       | Displays a list of all saved notes.                                                                           |

> **Note:** Mandatory arguments are enclosed in `[like this]`, while optional ones are in `<like this>`.
