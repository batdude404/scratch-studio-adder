# Scratch Studio Adder

An automated Python script built with [scratchattach](https://github.com/TimMcCool/scratchattach) that copies all studio memberships from a source Scratch project to a target Scratch project.

---

## What It Does

Manually adding a Scratch project to dozens or hundreds of studios is tedious. This script automates the entire process:
1. **Authenticates** with your Scratch account securely using your credentials.
2. **Scans the Source Project** (`SOURCE_PROJECT_ID`) to fetch a complete list of all the studios it has been added to.
3. **Scans the Target Project** (`TARGET_PROJECT_ID`) to check which studios it is *already* a member of (avoiding duplicate work and redundant API requests).
4. **Adds the Target Project** to every studio where the source project is present, provided you have manager or curator permissions.
5. **Handles Rate Limits & Permissions:** Automatically catches `403 Forbidden` errors (when you aren't a curator/manager of a specific studio) and handles `429 Rate Limit` errors gracefully with built-in delays (`time.sleep`).

---

## How to Set It Up and Run It

### Prerequisites

Make sure you have Python installed on your system. You will need to install the `scratchattach` library.

Open your terminal or command prompt and run:
```bash
pip install scratchattach
```

### Configuration & Code Customization

To make the script work for your specific account and projects, you need to edit the configuration variables inside `scratch_studio_adder.py`:

1. Open `scratch_studio_adder.py` in any code editor or text editor.
2. Locate the **CONFIGURATION** section near the top of the file:
   ```python
   # ==========================================
   # CONFIGURATION
   # ==========================================
   # USE YOUR PASSWORD AND USERNAME HERE!
   USERNAME = "YOUR_USERNAME" 
   PASSWORD = "YOUR_PASSWORD" 

   SOURCE_PROJECT_ID =   14673585
   TARGET_PROJECT_ID =  1392115446 
   # ==========================================
   ```
3. **Update your details:**
   * Replace `"YOUR_USERNAME"` with your actual Scratch username.
   * Replace `"YOUR_PASSWORD"` with your actual Scratch password.
   * Replace `SOURCE_PROJECT_ID` with the ID of the project whose studio list you want to copy. (You can find a project's ID in its URL, e.g., `scratch.mit.edu/projects/14673585/`).
   * Replace `TARGET_PROJECT_ID` with the ID of the project you want to add into those studios.

### Running the Script

Once you have saved your changes to `scratch_studio_adder.py`, execute the script from your terminal:
```bash
python scratch_studio_adder.py
```

---

## Important Notes & Troubleshooting

* **Curator/Manager Permissions:** You can only add projects to studios where your Scratch account has curator or manager rights. If the script encounters a studio where you lack permission, it will log a `403` error and safely skip to the next studio.
* **Rate Limits:** Scratch enforces rate limits on automated requests. The script includes a 1.5-second pause between requests and handles temporary rate-limiting (`429`) automatically.
