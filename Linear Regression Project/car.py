# Function to get user input for the features
def get_user_input():
    user_data = {}

    # Prompt for categorical features
    user_data['fueltype'] = input("Enter fuel type (gas/diesel): ")
    user_data['aspiration'] = input("Enter aspiration (std/turbo): ")
    user_data['carbody'] = input("Enter car body style (sedan/hatchback/wagon/convertible): ")
    user_data['drivewheel'] = input("Enter drive wheel type (fwd/rwd/4wd): ")
    
    # Prompt for numerical features
    user_data['wheelbase'] = float(input("Enter wheelbase (inches): "))
    user_data['carlength'] = float(input("Enter car length (inches): "))
    user_data['carwidth'] = float(input("Enter car width (inches): "))
    user_data['curbweight'] = float(input("Enter curb weight (lbs): "))
    user_data['enginetype'] = input("Enter engine type (dohc/litree/sohc): ")
    user_data['cylindernumber'] = input("Enter number of cylinders (two/four/six/eight): ")
    user_data['enginesize'] = float(input("Enter engine size (cu.in.): "))
    user_data['boreratio'] = float(input("Enter bore ratio (inches): "))
    user_data['horsepower'] = float(input("Enter horsepower: "))

  
    user_data['brand_category'] = input("Enter brand category (e.g., compact, midsize, etc.): ")
    user_data['mileage'] = float(input("Enter mileage (mpg): "))

    return user_data

new_data = get_user_input()
new_data = pd.DataFrame([new_data])

# Apply the preprocessor to transform the new data
new_data_transformed = preprocessor.transform(new_data)

# Make a prediction using the model
prediction = model.predict(new_data_transformed)
print("Predicted Price:", prediction)