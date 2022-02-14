import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'newyork': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:ain
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nPlease Enter the name of the following cities '
                     'to explore its data (chicago, new york, washington) : \n').lower().strip()
        if city in CITY_DATA.keys():
            break

        print('\nwrong entry, Please try again\n')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nWould you want to filter data by month?\n '
                      ',if yes please enter the month as follows(january, february, march, april, may, june) '
                      ',if no enter all :\n').lower().strip()
        if month in months:
            break
        if month == 'all':
            break
        print('\nwrong entry, Please try again\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nWould you want to filter data by day ?\n '
                    ',if yes please enter the day as follows(monday, tuesday, ... sunday)'
                    ',if no enter all.\n').lower().strip()

        if day in days:
            break
        if day == 'all':
            break
        print('\nwrong entry, Please try again\n')

    print('-' * 40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month and count
    most_common_month = df['month'].mode()[0]
    most_common_month_count = df[df['month'] == most_common_month]['month'].count()
    print('\nthe most common month : {}  and count : {} '.
          format(most_common_month, most_common_month_count))

    # display the most common day of week and count
    most_common_day_of_week = df['day_of_week'].mode()[0]
    most_common_day_of_week_count = df[df['day_of_week'] == most_common_day_of_week]['day_of_week'].count()
    print('\nthe most common day of week : {}   and count : {} '.
          format(most_common_day_of_week, most_common_day_of_week_count))

    # display the most common start hour and count
    most_common_start_hour = df['hour'].mode()[0]
    most_common_start_hour_count = df[df['hour'] == most_common_start_hour]['hour'].count()
    print('\nthe most common start hour : {}  and count : {}'.
          format(most_common_start_hour, most_common_start_hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('\nthe most commonly used start station : ', most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('\nthe most commonly used end station :', most_common_end_station)

    # display most frequent combination of start station and end station trip
    start_station_and_end_station =\
        df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).head(1)
    print('\nthe most frequent combination of start station and end station trip :\n ', start_station_and_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time_min = df['Trip Duration'].sum()
    print('\nTotal travel time : ', total_travel_time_min)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nMean travel time : ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    unique_counts_of_user_types = df.groupby(['User Type'])['User Type'].count()
    print('\nCounts of user types(Unique) :\n ', unique_counts_of_user_types)

    if 'Gender' in df.columns:
        # Display counts of gender
        unique_counts_of_gender = df.groupby(['Gender'])['Gender'].count()
        print('\nCounts of gender(Unique) :\n ', unique_counts_of_gender)

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        df['Birth Year'] = pd.to_numeric(df['Birth Year'])
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print('\nearliest year of birth :  ', earliest_year)
        print('\nmost recent year of birth :  ', most_recent_year)
        print('\nmost common year of birth :  ', most_common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def browse_data(df):

    next_count = 5
    priv_count = 0
    while True:
        print(df.iloc[priv_count:next_count])
        res = input('\nEnter Next if you want to get next 5 row else you will exit ?\n').lower().strip()
        if res == 'next':
            priv_count = next_count
            next_count = next_count + 5
        if res != 'next':
            break


def main():
    while True:
        city, month, day = get_filters()
        print('Filter : ', city, month, day)
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        browse_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').strip()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
