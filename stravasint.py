import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

cookies = {
    ...
}

headers = {
    ...
}

# Function to search by name


def search_by_name():
    first_name = input("Enter the first name: ")
    last_name = input("Enter the last name: ")
    full_name = f"{first_name} {last_name}"

    params = {
        'utf8': '✓',
        'text': full_name,
        'page': 1  # Start at the first page
    }

    all_athlete_details = []

    while True:
        response = requests.get('https://www.strava.com/athletes/search',
                                params=params, cookies=cookies, headers=headers, verify=False)
        soup = BeautifulSoup(response.content, 'html.parser')

        for div in soup.find_all('div', class_='athlete-details'):
            name_div = div.find('div', class_='text-headline')
            if name_div:
                a_tag = name_div.find('a')
                name = a_tag.text.strip()
                profile_link = a_tag.get('href')
            else:
                name, profile_link = None, None

            location_div = div.find('div', class_='location')
            location = location_div.text.strip() if location_div else None

            follow_div = div.find('div', class_='follow-action')
            athlete_id = follow_div.get(
                'data-athlete-id') if follow_div else None

            all_athlete_details.append({
                "name": name,
                "profile_link": profile_link,
                "location": location,
                "athlete_id": athlete_id
            })

        next_page_elem = soup.find('li', class_='next_page')
        if not next_page_elem or next_page_elem.has_attr('disabled'):
            break

        params['page'] += 1

    for athlete in all_athlete_details:
        print(athlete)

# Function to search by athlete's ID


def search_by_id():
    athlete_id = input("Enter the athlete's ID number: ")
    url = f"https://www.strava.com/athletes/{athlete_id}"

    response = requests.get(url, cookies=cookies,
                            headers=headers, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')

    athlete_name_element = soup.find('h1', class_='text-title1 athlete-name')
    location_icon_element = soup.find(
        'div', class_='app-icon icon-location icon-xs mr-sm')
    location_text = location_icon_element.find_next_sibling(
        text=True) if location_icon_element else None

    club_elements = soup.select('div.avatar.avatar-club[original-title]')
    club_names = [club.get('original-title') for club in club_elements]

    if athlete_name_element:
        print(f"Athlete's Name: {athlete_name_element.text}")
    else:
        print("Couldn't find the athlete's name on the page.")

    if location_text:
        print(f"Location: {location_text.strip()}")
    else:
        print("Couldn't find the location on the page.")

    if club_names:
        print("\nClubs:")
        for club_name in club_names:
            print(f"- {club_name}")
    else:
        print("No clubs found for this athlete.")


# Main execution
print("Choose an option:")
print("1. Search by name")
print("2. Search by ID")

choice = input("Enter 1 or 2: ")

if choice == "1":
    search_by_name()
elif choice == "2":
    search_by_id()
else:
    print("Invalid choice!")
