import pandas as pd
import random

def generate_test_csv(path="test_addresses.csv", num=50):
    streets = ["Main St", "Oak St", "Pine Ave", "Maple Dr", "Cedar Ln", "Sunset Blvd", "Elm St"]
    cities = ["Dallas", "Fort Worth", "Plano", "Arlington", "Irving", "Garland", "Frisco"]
    states = ["TX"]
    addresses = []

    for _ in range(num):
        number = random.randint(100, 9999)
        street = random.choice(streets)
        city = random.choice(cities)
        state = random.choice(states)
        address = f"{number} {street}, {city}, {state}"
        addresses.append(address)

    df = pd.DataFrame({"Address": addresses})
    df.to_csv(path, index=False)
    print(f"✅ Test CSV created at: {path}")

if __name__ == "__main__":
    generate_test_csv()
