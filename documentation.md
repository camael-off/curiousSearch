# curiousSearch documentation
## Description
**curiousSearch** is a specialized OSINT tool designed to bridge the gap between complex Google Dorking and intuitive investigation. Its main goal is to simplify the use of advanced search operators through a minimalist and efficient Dark Mode interface.

This documentation will help you familiarize yourself with all the features of curiousSearch.

![GUI](./images/1.png)

**Documentation chapters:**
- Basics
- Keywords
- Search Engines
- File Types
- Modules
- Date & Range
- Sites
- Expert Filters
- Actions
- Profiles
___
## BASICS

This tool generates dorks based on your parameters. You can leave categories blank; for example, if no options in the File Type widget are selected, all file types will be shown.
___

## KEYWORDS
![keyword](./images/2.png)

This widget allows you to search for specific keywords.
```
🟩 : Include keyword
🟥 : Exclude keyword
✖️ : Remove a specific keyword
➕ : Add a keyword field
```
You can select all keywords or reset the selection.

___
## SEARCH ENGINES

![search engine](./images/3.png)

This widget allows you to use different search engines. This is important because indexing varies significantly between them. It is common to obtain different results between Google and Bing, for example. Sometimes the generated dork will not work on every search engine if it is too complex.
___
## FILE TYPES

![file type](./images/4.png)

This widget allows you to search for precise file types. You can add custom extensions.
```
🟩 : Include file type
🟥 : Exclude file type
✖️ : Remove a specific file type
➕ : Add a file type field
```
You can also select extensions from the list, select all, or reset the selection.

___

## MODULES
![metier](./images/5.png)

This widget allows you to use different built-in functions, such as:

- **Google Images Mode**
- **Open Servers**
- **Logs Stealer**
- **Onion Targeting**
- **S3 Buckets & Clouds**
- **Config Files**

**Selecting these options is optional for running an investigation.**

### Google Images Mode:

When this mode is selected, only Google will be used for the dork. Other search engines remain disabled until the mode is turned off.

![google image 1](./images/6.png)

These filters use the TBS feature:

**Type:** Clipart, Lineart, GIF, Face.
**Color:** Full color, Black and white, Transparent, Red, Green, Blue.
**Size:** Icon, Medium, Large.
**Resolution:** VGA, 2MP, 8MP.
**Rights:** Commercial, Creative Commons.

You can also paste an image URL in the **Reverse Search** field to find similar pictures across different engines.
___

### Open Servers:

curiousSearch can search for open servers available without authentication.

![open server](./images/7.png)

![files](./images/8.png)

___

### Logs Stealer:

This option is a preset to search for passwords and logins in logs, SQL, and ENV files.

![logs](./images/9.png)

___

### Onion Targeting:

This option is useful for finding `.onion` links related to specific keywords.

![logs](./images/9_1.png)
___
### S3 Buckets & Clouds:

This option searches for data in these cloud provider websites:
- s3.amazonaws.com
- storage.googleapis.com
- blob.core.windows.net

![s3](./images/10.png)
![cloud](./images/11.png)

___

### Config Files:

This option allows you to search for `.env`, `.yaml`, and `.json` files used in databases or AWS.
![config](./images/12.png)

___
___

## DATE & RANGE

![date](./images/13.png)

This widget allows you to define the time period for your results. Ensure "All time" is unchecked to choose custom date filters.
___
## SITES
![site](./images/14.png)

Apply filters to specific websites or platforms.
```
🟩 : Include a website
🟥 : Exclude a website
✖️ : Remove a website
➕ : Add a website field
```

Categories include: **All, Social, Tech, and Custom**. You can modify these via the `sites.json` file.
___

## EXPERT FILTERS:

Enable powerful advanced operators:

- **Exact match**
- **In body / title / URL / Links**
- **Similar**
- **Archive** (Wayback Machine)

**Geographic Filtering:**

![countries](./images/15.png)
```
🟩 : Include a continent/country
🟥 : Exclude a continent/country
✖️ : Remove a continent/country
➕ : Add a continent/country
```
This filter is based on country TLDs.
___

## ACTIONS 

Launch the investigation or copy the dork to your clipboard.

**Shortcuts:** `Enter` to launch, `Ctrl + C` to copy.

Support the project on [Buy Me a Coffee](https://buymeacoffee.com/camael).
