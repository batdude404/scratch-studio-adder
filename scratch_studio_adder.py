import scratchattach as scratch3
import time
import warnings

# Hide the login warning to keep the console output clean
warnings.filterwarnings("ignore")

# ==========================================
# CONFIGURATION
# ==========================================
# USE YOUR PASSWORD AND USERNAME HERE!
USERNAME = "YOUR_USERNAME" 
PASSWORD = "YOUR_PASSWORD" 

SOURCE_PROJECT_ID =   14673585
TARGET_PROJECT_ID =  1392115446 
# ==========================================

print("Logging into Scratch...")
try:
    session = scratch3.login(USERNAME, PASSWORD)
    print("✅ Login successful!\n")
except Exception as e:
    print(f"❌ Login failed. Did you change your password? Error: {e}")
    exit()

# 1. Get the studios the SOURCE project is in
print(f"Fetching studios for source project {SOURCE_PROJECT_ID}...")
try:
    source_project = session.connect_project(SOURCE_PROJECT_ID)
    # FIX: Extract the actual integer ID using .id instead of converting the object to a string
    source_studios = [s.id for s in source_project.studios()] 
    print(f"Found {len(source_studios)} studios from the source project.")
except Exception as e:
    print(f"❌ Could not fetch source studios. Error: {e}")
    exit()

# 2. Get the studios the TARGET project is ALREADY in
print(f"Checking which studios target project {TARGET_PROJECT_ID} is already in...")
try:
    target_project = session.connect_project(TARGET_PROJECT_ID)
    # FIX: Extract the actual integer ID using .id
    already_in_studios = [s.id for s in target_project.studios()]
    print(f"Target project is already in {len(already_in_studios)} studios.\n")
except Exception as e:
    print(f"⚠️ Could not fetch target's current studios ({e}). Will attempt to add to all.\n")
    already_in_studios = []

# 3. Add the target project to the source studios (skipping duplicates)
print("--- Starting Additions ---`n")
success_count = 0
skipped_count = 0

for studio_id in source_studios:
    # CHECK: Is the project already in this studio?
    if studio_id in already_in_studios:
        print(f"⏭️ Skipped studio {studio_id} (Project is already in it).")
        skipped_count += 1
        continue # Skip to the next studio

    print(f"Adding project {TARGET_PROJECT_ID} to studio {studio_id}...", end=" ")
    
    try:
        studio = session.connect_studio(studio_id)
        studio.add_project(TARGET_PROJECT_ID)
        print("✅ Success!")
        success_count += 1
        
        # Update our local list so we don't accidentally try to add it again 
        already_in_studios.append(studio_id)
        
    except Exception as e:
        error_msg = str(e)
        if "403" in error_msg or "Forbidden" in error_msg:
            print("❌ Failed (403). You are not a curator/manager of this studio.")
        elif "429" in error_msg or "Rate" in error_msg:
            print("⚠️ Rate limited! Waiting 15 seconds...")
            time.sleep(1.5)
            try:
                studio.add_project(TARGET_PROJECT_ID)
                print("✅ Success on retry!")
                success_count += 1
            except:
                print("❌ Failed on retry.")
        else:
            print(f"❌ Failed. Error: {e}")
            
    # Sleep to prevent hitting Scratch's rate limits
    time.sleep(1.5) 

print("\n" + "="*30)
print(f"🎉 Finished!")
print(f"✅ Successfully added to: {success_count} studios")
print(f"⏭️ Skipped (already in): {skipped_count} studios")
print(f"❌ Failed/No permission: {len(source_studios) - success_count - skipped_count} studios")
