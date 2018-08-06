import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': pd.read_csv('chicago.csv'),
              'new york city': pd.read_csv('new_york_city.csv'),
              'washington': pd.read_csv('washington.csv') }

# create city, month, and day of the week lists in the global level for later uses:
cities = ['chicago', 'new york city', 'washington']
months = ['january','february','march','april','may','june','all']
days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input(str("\nWhich city would you like to explore? Please enter one of the following: chicago, new york city, washington.\n")).lower()
        if city in cities:
            break
        else:
            print("Oops! Please enter the valid city name.\n")
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input(str("\nWhich month would you like to look into? If you want to see the data for all the months, enter'all'.\n")).lower()
        if month in months:
            break
        else:
            print("Oops! Please enter the valid month.\n")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(str("\nWhich day of the week would you like to see? If you want to see the data for all the days, enter'all'.\n")).lower()
        if day in days:
            break
        else:
            print("Oops! Please enter the valid day of the week.\n")
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.DataFrame(CITY_DATA[city])
    # convert the Start & End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month
    # extract day of the week from the Start Time column to create a day column
    df['day'] = df['Start Time'].dt.weekday_name
    # extract start hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # filter by month:
    if month !='all':
        # make the month index we created be consistent with the datetime indexing
        month = months.index(month) + 1
        # use the filtered month to create a new dataframe
        df = df[df['month'] == month]
    # filter by day:
    if day !='all':
        df = df[df['day'].str.lower() == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print("The most popular month is: "+ calendar.month_name[popular_month])

    # display the most common day of week
    popular_day = df['day'].mode()[0]
    print("The most popular day is: "+ str(popular_day))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("The most popular start hour is: "+ str(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most popular start station is: "+ popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most popular end station is: "+ popular_end_station)

    # display most frequent combination of start station and end station trip
    trips = df.groupby(['Start Station','End Station']).count().sort_values('Unnamed: 0',ascending=False).index[0]
    number_of_trips = df.groupby(['Start Station','End Station']).count().sort_values('Unnamed: 0',ascending=False).iloc[0,2]
    print("The most frequent trip is: "+str(trips)+" with "+str(number_of_trips)+" trips.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['End Time'].subtract(df['Start Time'], axis=0).sum()
    print("The total travel time is: "+str(total_travel_time).split(":")[0]+" hours "
    +str(total_travel_time).split(":")[1]+" minutes "
    +str(total_travel_time).split(":")[2]+" seconds.")

    # display mean travel time
    total_trips = df.groupby(['Start Station','End Station']).size().sum()
    mean = total_travel_time/total_trips
    print("The average travel time is: "+str(pd.to_timedelta(mean)).split(":")[0]+" hours "
    +str(pd.to_timedelta(mean)).split(":")[1]+" minutes "
    +str(pd.to_timedelta(mean)).split(":")[2]+" seconds")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_ct = df.groupby(['User Type']).size().reset_index(name='count')
    print("The user types distribution is: \n"+user_types_ct.to_string(index=False)+"\n")

    # Display counts of gender. Washington does not have gender column.
    if 'Gender' in df.columns:
        gender_ct = df.groupby(['Gender']).size().reset_index(name='count')
        print("The gender distribution is:\n"+gender_ct.to_string(index=False))
    else:
        print("Gender information is not available.")

    # Display earliest, most recent, and most common year of birth. Washington does not have birth year column.
    if 'Birth Year' in df.columns:
        oldest = df.sort_values(by=['Birth Year'], ascending=True).head(1)
        print("\n"+"The earliest year of birth is: "+ str(int(oldest.iloc[0,-4])))
        youngest = df.sort_values(by=['Birth Year'], ascending=False).head(1)
        print("The most recent year of birth is: "+ str(int(youngest.iloc[0,-4])))
        common = df['Birth Year'].mode()[0]
        print("The most common year of birth is: "+ str(int(common)))
    else:
        print("\n"+"Birth year information is not available.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    # a function showing raw data upon user's request.
    # As a suggestion, you could use a loop to do this. 
    # You keep a counter with the number of rows printed 
    # and then in each iteration you print the next five ones.
    n = 0
    request = input("Do you want to see the raw data? Enter 'yes' to see the first five rows.\n")
    if request.lower() == 'yes':
        while True:
            print(df.iloc[n:n+5])
            request_2 = input("Do you want to see more? Enter 'yes' to see five more rows.\n")
            if request_2.lower() == 'yes':
                n += 5
            else: 
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
