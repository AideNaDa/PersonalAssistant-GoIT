# PersonalAssistant-GoIT

## Commands Usage

The bot supports managing contacts and text notes. Command parameters are indicated in brackets `[ ]`. 

---

### Contact Management

| Command | Arguments | Description |
| :--- | :--- | :--- |
| **`add`** | `[name]` `<phone> <birthday> <address> <email>` | Creates a new contact. Additional parameters (birthday, address, email) are optional. **The order of the arguments does not matter.** |
| **`add`** | `[name] [phone]` and/or `[email]` | Adds another phone number and/or email to an existing contact. |
| **`find`** | `[query]` | Displays a contact card. Search works by any match: name, phone, address, email, or birthday. |
| **`edit`** | `[name] [old_phone] [new_phone]`<br>or `[old_email] [new_email]`<br>or `[new_birthday]`<br>or `[new_address]` | Edits contact details. Overwrites the birthday or address, or replaces an old phone/email with a new one. |
| **`del`** | `[name]` | Deletes the contact and all associated data completely. |
| **`del`** | `[name] [phone]` or `[email]` or `[birthday]` or `[address]` | Deletes a specific field for the selected contact (e.g., only the email or just one of the phone numbers). |
| **`show-all`** | *- no arguments -* | Displays a list of all saved contacts. |
| **`birthdays`** | `[num]` | Displays a list of contacts who have a birthday coming up in the specified number of days (`num`). |

---

### Note Management

| Command | Arguments | Description |
| :--- | :--- | :--- |
| **`add-note`** | `[title] [text] <tag>` | Creates a new note with a title and text. The tag (`tag`) is optional. |
| **`find-note`**| `[query]` | Searches for a note by its title or attached tags. |
| **`add-tag`** | `[title] [tag]` or `[tag1] [tag2]...` | Adds one or more tags to an existing note. |
| **`edit-note`**| `[title] [new_text]`<br>or `[old_tag] [new_tag]` | Changes the main text of a note or replaces an old tag with a new one. |
| **`del-note`** | `[title]` | Deletes a note by its title. |

> **Note:** Mandatory arguments are enclosed in `[like this]`, while optional ones are in `<like this>`.

