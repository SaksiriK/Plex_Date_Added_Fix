import datetime
import psutil
import time
from plexapi.server import PlexServer
from gettoken import getToken


def update_future_dates():
    # Get Plex token
    token = getToken()
    if not token:
        print("Failed to retrieve the token. Exiting.")
        return

    print(f"Authentication token: {token}")

    # Connect to Plex server
    baseurl = 'http://192.168.1.52:32400'
    try:
        plex = PlexServer(baseurl, token)
        print("Successfully connected to Plex server.")
    except Exception as e:
        print(f"Failed to connect to Plex server: {e}")
        return

    # Print starting message
    print("Starting the update process...")

    # Get all library sections
    try:
        library_sections = plex.library.sections()
        print("Available library sections:")
        for section in library_sections:
            print(f"- {section.title}")
    except Exception as e:
        print(f"Failed to retrieve library sections: {e}")
        return

    # Get the date of last week
    last_week = datetime.datetime.now().date() - datetime.timedelta(weeks=1)

    # Iterate through all library sections
    for section in library_sections:
        print(f"Entering section: {section.title}")

        # Get all items in the section
        try:
            all_items = section.all()
        except Exception as e:
            print(f"Failed to retrieve items from section {section.title}: {e}")
            continue

        # Counter to keep track of the number of records processed
        record_count = 0

        # I/O and CPU measurements for the section
        section_start_time = time.time()
        section_cpu_start = psutil.cpu_times()
        section_io_start = psutil.disk_io_counters()

        # Iterate through all items and update future dates
        for item in all_items:
            fixed = False

            # Check and update Added At
            if hasattr(item, 'addedAt') and item.addedAt and item.addedAt.date() > last_week:
                try:
                    item.edit(**{'addedAt.value': last_week})
                    print(f"Fixed future added date for: {item.title}")
                    fixed = True
                except Exception as e:
                    print(f"Failed to update added date for {item.title}: {e}")

            # Check and update Last Viewed At
            if hasattr(item, 'lastViewedAt') and item.lastViewedAt and item.lastViewedAt.date() > last_week:
                try:
                    item.edit(**{'lastViewedAt.value': last_week})
                    print(f"Fixed future last viewed date for: {item.title}")
                    fixed = True
                except Exception as e:
                    print(f"Failed to update last viewed date for {item.title}: {e}")

            # Print the fixed message if any date was fixed
            if fixed:
                print(f"Fixed item: {item.title}")

            # Increment the record count
            record_count += 1

            # Print movie name and record count every 10 records
            if record_count % 10 == 0:
                elapsed_time = time.time() - section_start_time
                cpu_end = psutil.cpu_times()
                io_end = psutil.disk_io_counters()

                print(f"Movie name: {item.title}, Records processed: {record_count}")
                print(f"Elapsed time: {elapsed_time:.2f} seconds")
                print(f"CPU times: user={cpu_end.user - section_cpu_start.user}, system={cpu_end.system - section_cpu_start.system}")
                print(f"I/O counts: read_count={io_end.read_count - section_io_start.read_count}, write_count={io_end.write_count - section_io_start.write_count}")

            # Short delay to prevent overwhelming the server
            time.sleep(0.1)

        # Final I/O and CPU measurements for the section
        section_elapsed_time = time.time() - section_start_time
        section_cpu_end = psutil.cpu_times()
        section_io_end = psutil.disk_io_counters()

        print(f"Completed section: {section.title}")
        print(f"Total records processed: {record_count}")
        print(f"Section elapsed time: {section_elapsed_time:.2f} seconds")
        print(f"Section CPU times: user={section_cpu_end.user - section_cpu_start.user}, system={section_cpu_end.system - section_cpu_start.system}")
        print(f"Section I/O counts: read_count={section_io_end.read_count - section_io_start.read_count}, write_count={section_io_end.write_count - section_io_start.write_count}")

    print("All future dates updated to last week's date.")


if __name__ == "__main__":
    update_future_dates()
