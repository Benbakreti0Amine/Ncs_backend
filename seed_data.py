import random
from faker import Faker
from users.models import User
from report.models import Report
from alert.models import Alert

fake = Faker()

# Constants
NUM_USERS = 10
REPORTS_PER_USER = 15
SHARED_LOCATION_COUNT = 10

# Helper function to create random latitude and longitude
def generate_random_location():
    latitude = round(random.uniform(-90, 90), 6)
    longitude = round(random.uniform(-180, 180), 6)
    return latitude, longitude

# Seed users
def seed_users():
    print("Creating users...")
    users = []
    for _ in range(NUM_USERS):
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password="password123",
            latitude=fake.latitude(),
            longitude=fake.longitude(),
        )
        users.append(user)
    print(f"Created {len(users)} users.")
    return users

# Seed reports and alerts
def seed_reports_and_alerts(users):
    print("Creating reports and alerts...")
    for user in users:
        shared_latitude, shared_longitude = user.latitude, user.longitude

        # Create reports for the user
        for _ in range(REPORTS_PER_USER):
            # Decide if the report should share the user's location
            if random.randint(1, REPORTS_PER_USER) <= SHARED_LOCATION_COUNT:
                latitude, longitude = shared_latitude, shared_longitude
            else:
                latitude, longitude = generate_random_location()

            # Create the report
            report = Report.objects.create(
                title=fake.sentence(),
                description=fake.text(),
                severity=random.choice(["Low", "Medium", "High", "Critical"]),
                latitude=latitude,
                longitude=longitude,
                user=user,
            )

            # Create an associated alert
            Alert.objects.create(
                report=report,
                message=f"Alert for report: {report.title}",
            )
    print("Reports and alerts created successfully.")

# Main seeding function
def seed_data():
    users = seed_users()
    seed_reports_and_alerts(users)

# Execute the script
if __name__ == "__main__":
    seed_data()
