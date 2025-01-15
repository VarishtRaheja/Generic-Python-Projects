`import pandas as pd
`

# Reading the csv file as a dataframe
`df = pd.read_csv("hotels.csv")
df_cards = pd.read_csv("cards.csv",dtype=str).to_dict(orient="records")
df_security = pd.read_csv("card_security.csv",dtype=str)`

`class Hotel:
    def __init__(self,user_id):
        self.user_id = user_id
        self.name = df.loc[df['id']==self.user_id,"name"].squeeze(`)

    def book(self):
        """ Book a hotel by changing its availability to 'no' post-booking. """
        df.loc[df['id'] == self.user_id, 'available'] = 'no'
        df.to_csv("hotels.csv",index=False)

    def available(self):
        """ Checks if hotel is available. """

        availability = df.loc[df['id'] == self.user_id,'available'].squeeze()
        if availability == "yes":
            return f"Hotel with id {self.user_id} is available"
        else:
            return "Please choose a different hotel."

    # This is just to reset availability
    @classmethod
    def reset_availability(cls):
        if "no" in df['available'].values:
            df.loc[df['available'] == "no", 'available'] = "yes"
            df.to_csv("hotels.csv",index=False)


`class Reservation:
    """ Reserving the customer details for the booking. """
    def __init__(self,customer_name:str, hotel_object:str):
        self.customer_name = customer_name
        self.hotel = hotel_object
`
        # assert customer_age > 18, "Your age must be more than 18 years."

    def generate_booking(self):
        content = f""" Thank you for your reservation!
                        Here are your booking details.
                        Name: {self.customer_name}
                        Hotel name: {self.hotel} """
        return content


`class CreditCard:`

    def __init__(self,card_number):
        self.card_number = card_number

    def validate(self,holder_name,expiration_date,cvc):
        card_data = {"number":self.card_number,"holder":holder_name,"expiration":expiration_date,"cvc":cvc}
        if card_data in df_cards:
            return True
        else:
            return False

`class SecureCard(CreditCard):
    def __init__(self,card_number):
        # Call super function for accessing credit card method/attrs.
        super().__init__(card_number=card_number)`

    def authenticate(self,given_password):
        password = df_security.loc[df_security['number']==self.card_number,"password"].squeeze()
        if given_password == password:
            return True
        else:
            return False

`class Spa(Hotel):
    def book_spa(self,massage):
        if self.available():
            if massage == "yes":
                return "Your massage is booked!"
            else:
                return "No massage booked."
`

# Call reset function
`Hotel.reset_availability()`


# Creating the app loop.
```print("Hotels available are: \n")
print(df)
hotel_id = int(input("Enter id of hotel to book -----> "))
hotel_instance = Hotel(hotel_id)
spa_massage = Spa(hotel_instance.user_id)

if hotel_instance.available():
    credit_card = SecureCard(card_number="1234")
    if credit_card.validate(holder_name="JOHN SMITH",expiration_date="12/26",cvc="123"):
        if credit_card.authenticate("mypass"):
            hotel_instance.book()
            name = input("Enter your name -------> ")
            customer_reservation = Reservation(customer_name=name,hotel_object=hotel_instance.name)
            massage = input("Would you like a massage? ")
            print(customer_reservation.generate_booking())
            print(spa_massage.book_spa(massage))
        else:
            print("Card was not authenticated.")
    else:
        print("There was an issue with your payment!")
else:
    print("Hotel is fully booked!")```