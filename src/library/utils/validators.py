def get_int(prompt="Please enter an ID: "):
    while True:
        try:
            value = int(input(prompt))

            if value <= 0:
                print("ID must be a positive integer.")
                continue

            return value

        except ValueError:
            print("Please enter a valid integer.")