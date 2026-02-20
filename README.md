## *curiousSearch* ##
​
**curiousSearch** is a specialized OSINT tool designed to bridge the gap between complex Google Dorking and intuitive investigation. Its main goal is to simplify the usage of advanced search operators through a minimalist and efficient Dark Mode interface.

### License ###

**curiousSearch** is licensed under the MIT license. Refer to [license.txt](license.txt) for more information.

### Installation ###

You need [python 3.10+](https://www.python.org/downloads/).

Then follow these simple steps: 
```
mkdir curiousSearch
cd curiousSearch
python3 -m venv venv
source venv/bin/activate
cd venv
git clone https://github.com/camael-off/curiousSearch.git
cd curiousSearch
pip install -r requirements.txt
python3 curiousSearch.py
```

Or use docker :
```
docker build -t curioussearch:latest .
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix curioussearch:latest
```

## Description
**curiousSearch** is a specialized OSINT tool designed to bridge the gap between complex Google Dorking and intuitive investigation. Its main goal is to simplify the use of advanced search operators through a minimalist and efficient Dark Mode interface.

This documentation will help you familiarize yourself with all the features of curiousSearch.

![GUI](./images/1.png)

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
___

## PRESETS 

You can save you dork query with the save button. Every presets are located in the profiles.json file. 

### Usage/Help ###
___

​Core Features :<br/><br/>
&emsp;- Multi-Engine Support: Generate powerful queries for 5 different search engines simultaneously.<br/> <br/>
&emsp;​- Keyword Mastery: Easily include or exclude specific keywords to refine your results.<br/> <br/>
&emsp;​- Deep File Filtering: Native support for common extensions (PDF, TXT, LOG, SQL, ENV) and custom filetype search.<br/> <br/>
&emsp;​- Pre-configured Modes: Quick access to specialized searches:<br/>
&emsp;​&emsp;• Open Server & Directory Listing.<br/> 
&emsp;​&emsp;• Configuration & Sensitive Files.<br/> 
&emsp;​&emsp;• Onion link finder<br/>
&emsp;​&emsp;• S3 bucket and clouds.<br/>
&emsp;​&emsp;• Configuration files.<br/><br/>
&emsp;​- Temporal Precision: Search within a precise date, a specific interval, or an "all-time" range.<br/><br/> 
&emsp;​- Targeted Scoping:<br/>
&emsp;&emsp;​• Social Media: Built-in filters for over 100 platforms.<br/>
&emsp;&emsp;​• Tech & Cloud: Specialized search for documentation and cloud storage.<br/>
&emsp;&emsp;• Custom Domains: Filter by specific websites or exclude unwanted domains.<br/>
&emsp;&emsp;​• Expert Geolocation Filters: Include or exclude results by continents or specific country TLDs.<br/> <br/>
&emsp;​- Profiles: Save, export, and share your custom research setups.<br/> <br/>
&emsp;​- Multilingual: Full support for both French and English.<br/> <br/>
&emsp;​- Privacy First: No data collection. Your investigations remain yours alone.<br/> <br/> 

Use Cases :<br/><br/>
&emsp;​- Cybersecurity: Reconnaissance for Bug Bounty and Penetration Testing.<br/> 
&emsp;​- Investigation: Digital forensics and OSINT research.<br/> 
&emsp;​- Journalism: Fact-checking and sourcing hidden information.<br/> 
&emsp;​- Personal Use: Advanced filtering for precise information gathering.<br/> <br/> 

### Support ###
Support the project on [BuyMeACoffee](https://buymeacoffee.com/camael)<br/> 
​Special thanks to everyone who shared feedback and ideas to make this project possible!<br/> 
