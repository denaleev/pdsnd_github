"""
Project owner: Denis Aleev
Requested by: Udacity
"""

"""
Ultra optimizer
"""

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('>Select a city from the list: "Chicago", "New York City", "Washington"\n').lower()
        if city not in CITY_DATA.keys():
            print(f'>ERROR: Unexpected input: "{city.title()}" not recognized. Try again.\n')
        else:
            break
 
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:    
        months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        month = input(f'>Select a month from January to June to explore data for {city.title()} \nNote: use "all" to don\'t apply filter\n').lower()
        if month not in months:
            print(f'>ERROR: Unexpected input: "{month.title()}" not recognized. Try again.\n')
        else:
            break        

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:    
        days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = input(f'>Select the weekday for month(s) - "{month.title()}" to explore data for "{city.title()}"\
                    \nNote: use "all" to don\'t apply filter\n').lower()
        if day not in days:
            print(f'>ERROR: Unexpected input: "{day.title()}" not recognized. Try again.\n')
        else:
            break   

    print('-'*40)
    #print(f'{city}, {month}, {day}')
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
    # load city data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


#Count number of (filtered) results
def count_results(df):
    total_results = df.shape[0]
    print(f'\nTotal records for your request: {total_results}\n')
    print('-'*40)

    
def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month == 'all':
        popular_month = df['month'].mode()[0]
        print('Most Popular Month:', popular_month)
        
    # TO DO: display the most common day of week
    if day == 'all':
        popular_day = df['day_of_week'].mode()[0]
        print('Most Popular Day:', popular_day)

    # TO DO: display the most common start hour
    
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    popular_start_end_station_pair = df.groupby(['Start Station','End Station']).size().idxmax()
    print('Most Popular Start-End Station Pair:', popular_start_end_station_pair) 
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # TO DO: display total travel time
    df["trips_durations"] = df["End Time"] - df["Start Time"]
    total_travel_time = df["trips_durations"].sum()
    print("Total Travel Time:", total_travel_time.days, "days", \
                                total_travel_time.seconds // 3600, "hrs.", \
                                total_travel_time.seconds // 60 % 60, " min.", \
                                total_travel_time.seconds % 60, " sec.")

    # TO DO: display mean travel time
    mean_travel_time = df["trips_durations"].mean()
    print("Mean Travel Time:", mean_travel_time.days, "days", \
                               mean_travel_time.seconds // 3600, "hrs.", \
                               mean_travel_time.seconds // 60 % 60, " min.", \
                               mean_travel_time.seconds % 60, " sec.")

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    if 'User Type' in df.columns:
        # TO DO: Display counts of user types
        user_types = df['User Type'].value_counts().to_string()
        print(f"Types of users and counts:\n{user_types}")
    else:
        print(f'\nNo data on types of users for "{city.title()}"')
    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts().to_string()
        print(f"\nCounts of gender:\n{gender_counts}")
    else:
        print(f'\nNo data on genders of users for "{city.title()}"')

    if 'Birth Year' in df.columns:
    # TO DO: Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        print(f"\nEarliest birth year: {earliest_birth_year}\
                \nMost recent birth year: {recent_birth_year}\
                \nMost common birth year: {common_birth_year}")
    else:
        print(f'\nNo data on years of birth for "{city.title()}"')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def raw_data(df):
    #load 5 rows of individual trip data
    raw_data = input('Would you like to view individual trip data?\nPlease select yes [y] or no [n].').lower()
    if raw_data in ("yes", "y"):
        print(df.iloc[:5])
        i = 5
        #ask for another 5 rows
        while True:
            raw_data_cont = input('\nWould you like to view another 5 records?\nEnter [y] if "yes" or any other key for "no".\n').lower()
            if raw_data_cont in ("yes", "y"):
                if (i + 5 > len(df.index) - 1):
                    print(df.iloc[i:len(df.index), :])
                    print("You've reached the end of the rows")
                    break
                else:
                    print(df.iloc[i:i+5, :])
                    i += 5
            else:
                break
                

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        count_results(df)
        time_stats(df, city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter [y] if "yes" or any other key for "no".\n')
        if restart.lower() not in ('yes', 'y'):
            break


if __name__ == "__main__":
	main()
