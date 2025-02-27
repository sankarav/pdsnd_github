import time
from time import sleep

import pandas as pd
import numpy as np
from typing import List

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'nyc': 'new_york_city.csv',
              'washington': 'washington.csv' }

ALL = 'all'

MONTHS = [ALL, 'january', 'february', 'march', 'april', 'may', 'june']
DAYS = [ALL, 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

choice_city = choice_month = choice_day = None

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
    cities = list(CITY_DATA.keys())
    city = get_filter('Would you like to see data for {}? \n'.format(cities), cities)
    print_acknowledge_msg_to_user('city', city)

    # get user input for month (all, january, february, ... , june)
    month = get_filter('Would you like to filter data for month {}? \n'.format(MONTHS), MONTHS)
    print_acknowledge_msg_to_user('month', month)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_filter('Would you like to filter data for month {}? \n'.format(DAYS), DAYS)
    print_acknowledge_msg_to_user('day', day)

    print('-'*40)
    return city, month, day

def sanitize_user_input(user_input: str) -> str:
    return user_input.strip().lower() if user_input else None

def get_filter(msg: str, valid_values: List[str]) -> str:

    while True:
        original_user_input = input(msg)
        user_input = sanitize_user_input(original_user_input)

        if user_input in valid_values:
            return user_input
        else:
            print(f'Sorry [{original_user_input}] is an invalid option.')

def print_acknowledge_msg_to_user(criteria: str, value: str):
    """
    Helper method to print acknowledgement msg to console

    Args:
        (str) criteria - criteria name for which the data is to be filtered
        (str) value - user provided value
    """

    if value == ALL:
        msg = f'Skipping filter, selecting all available {criteria}s'
    else:
        msg = f'Filtering data for {criteria} = {value}'

    print(msg, end='')

    for i in range(5):
      sleep(0.25)
      print('.', end='')
    print('')

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
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != ALL:
        # use the index of the MONTHS list to get the corresponding int
        # though list index is zero based, all is at 0th index,
        # hence no need to offset index
        month = MONTHS.index(month)

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != ALL:
        # use the index of the DAYS list to get the corresponding int
        # need to fix index minus 1 as 'all' is at zeroth position
        day = DAYS.index(day) - 1
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    val_counts = df['Start Time'].dt.month_name().value_counts()
    print_stats(val_counts, 'month', top_n=0 if choice_month == ALL else 3)

    # display the most common day of week
    val_counts = df['Start Time'].dt.day_name().value_counts()
    print_stats(val_counts, 'day', top_n=0 if choice_day == ALL else 3)

    # display the most common start hour
    val_counts = df['Start Time'].dt.hour.value_counts()
    print_stats(val_counts, 'start hour')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_stats_group_line_break()

def print_stats(val_counts: pd.Series, attribute: str, top_n: int = 3):
    """
    Helper method to print various statistics to console

    Args:
        (pd.Series) val_counts - pandas series that has count to print stats from
        (str) attribute - attribute name for which the stats is to be printed
        (int) top_n - default 3
            Prints additional top_n items if its greater than zero
    """

    print_stat_line_break()

    print(f'Most popular "{attribute}" is [{val_counts.idxmax()}]\n')

    if top_n:
        print(f'Top-{top_n} popular "{attribute}" :')
        print(val_counts.head(top_n))


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    val_counts = df['Start Station'].value_counts()
    print_stats(val_counts, 'Start Station')

    # display most commonly used end station
    val_counts = df['End Station'].value_counts()
    print_stats(val_counts, 'End Station')

    # display most frequent combination of start station and end station trip
    val_counts = df[['Start Station', 'End Station']].value_counts(subset=['Start Station', 'End Station'])
    print_stats(val_counts, 'Start -> End Station combination')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_stats_group_line_break()

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'total travel time across trips = {total_travel_time}')

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print(f'average travel time for trips = {average_travel_time}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print_stats_group_line_break()

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())
    print_stat_line_break()

    if choice_city == 'washington':
        print('Gender and Birth Year data unavailable for Washington')
    else:
        # Display counts of gender
        print(df['Gender'].value_counts())
        print_stat_line_break()

        # Display earliest, most recent, and most common year of birth
        print('Earliest Year of Birth = {}'.format(int(df['Birth Year'].min())))
        print('Most recent Year of Birth = {}'.format(int(df['Birth Year'].max())))
        print('Most common Year of Birth = {}'.format(int(df['Birth Year'].value_counts().idxmax())))
        print_stat_line_break()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_stats_group_line_break()

def print_raw_data(df, chunk_size=5):
    """
    Prints raw dataframe as JSON in chunks waiting for user confirmation in between

    Args:
        (str) df - Pandas DataFrame containing city data filtered by month and day
        (int) chunk_size - default = 5
            number of items to show in each iteration
    """
    confirmation = input(f'Will you like to see the raw data used?\n'
                         f'Enter (n or no) to skip.\n'
                         f'Enter to continue.\n')
    if is_user_input_no(confirmation):
        return

    total_rows = len(df)
    num_chunks = (total_rows + chunk_size - 1) // chunk_size  # Ceiling division

    for i in range(0, total_rows, chunk_size):
        chunk = df.iloc[i:i + chunk_size]
        chunk_json = chunk.to_json(orient='records', indent=2)

        print(f"\nChunk {i//chunk_size + 1} of {num_chunks}:")
        print(chunk_json)

        # Don't ask for confirmation after the last chunk
        if i + chunk_size < total_rows:
            user_input = input("\nPress Enter to see the next chunk (or type 'q' to quit): ")
            if user_input.lower() == 'q':
                break

def print_stats_group_line_break():
    """Use it to add a line break in console after each statistic-group is printed"""
    print('-'*40)

def print_stat_line_break():
    """Use it to add a line break in console after each statistic is printed"""
    print('*'*40)

def print_run_iteration_line_break():
    """Use it to add a line break in console after each iteration"""
    print('\n'*6)
    print('%'*70)

def is_user_input_no(input: str) -> bool:
    return input.upper() in {'N', 'NO'}

def main():
    global choice_city, choice_month, choice_day
    while True:
        print_run_iteration_line_break()
        city, month, day = get_filters()
        choice_city, choice_month, choice_day = city, month, day

        to_continue = input(
            f'Data filters chosen [city={city} | month={month} | day={day}]\n'
            f'Enter (n or no) to restart.\nEnter to continue\n')

        if is_user_input_no(to_continue):
            print("That's ok. Restarting program...\n\n\n")
            continue
        else:
            print('Crunching some interesting statistics. Stay tuned....')

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        print_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if is_user_input_no(restart):
            break


if __name__ == "__main__":
	  main()
