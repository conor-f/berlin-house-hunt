import apprise
import shelve

from data_sources.ebayk import get_current_listings, AdListing


NOTIFICATIONS_SHELF = "/home/conor/Code/berlin-house-hunt/resources/cna-berlin-house-hunt-already-notified-shelf"
NTFY_TOPIC = "cna-berlin-house-hunt"


def get_ntfysh_apprise_topic(ad):
    return f"ntfy://{NTFY_TOPIC}?priority=max&click={ad.url}"


def get_notification_title(ad):
    """
    Given an AdListing, return the title string to notify with.
    """
    return f"{ad.title} - {ad.location} (€{ad.price})"


def get_notification_body(ad):
    """
    Given an AdListing, return the body string to notify with.
    """
    return f"{ad.description}"


def notify(ad):
    """
    Use Apprise to notify the ntfy.sh topic about a new ad.
    """
    apprise_client = apprise.Apprise()
    apprise_client.add(get_ntfysh_apprise_topic(ad))
    apprise_client.notify(
        title=get_notification_title(ad), body=get_notification_body(ad)
    )


def get_first_listing_with_time(listings):
    return next(filter(lambda listing: listing.upload_time, listings), None)


def should_notify_for_ad(ad):
    # Don't want to notify for listings with no time.
    if not ad.upload_time:
        return False

    with shelve.open(NOTIFICATIONS_SHELF, writeback=True) as shelf:
        if not "already_notified" in shelf:
            shelf["already_notified"] = []

        if ad.url not in shelf["already_notified"]:
            shelf["already_notified"].append(ad.url)
            return True

    return False

def main():
    listings = get_current_listings()

    # We only care about listings with actual times:
    for listing in listings:
        if should_notify_for_ad(listing):
            notify(listing)


if __name__ == "__main__":
    main()
