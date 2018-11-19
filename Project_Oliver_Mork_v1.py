import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington)
    city = ''
    while city not in CITY_DATA.keys():
        for keys in CITY_DATA.keys():
            print('- ', keys.title())
        city = input("Choose one of the cities above: ").lower()
        print('\n')

    # get user input for month
    month = ''
    while month not in months and month != 'all':
        for item in months:
            print('- ', item.title())
        month = input("Choose on of the months above or 'all': ").lower()
        print('\n')

    # get user input for day of week
    day = ''
    while day not in days and day != 'all':
        for item in days:
            print('- ', item.title())
        day = input("Choose one of the weekdays above or 'all': ").lower()
        print('\n')


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

    # Load city-specific data file into dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

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

def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month in case of no filter on month
    if month == 'all':
        popular_month = df['month'].mode()[0]
        print('- Most Frequent Start month:', months[popular_month-1].title())

    # display the most common day of week in case of no filter on day
    if day == 'all':
        popular_day_of_week = df['day_of_week'].mode()[0]
        print('- Most Frequent Start weekday:', popular_day_of_week)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('- Most Frequent Start Time: Between {}:00 - {}:00'.format(popular_hour,popular_hour+1))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('- Most Commonly Used Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('- Most Commonly Used End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df_sorted = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).reset_index().head(1)
    print('- Most frequent combination of start and end station (Count):')
    print(' ', df_sorted.iloc[0,0]," -> ", df_sorted.iloc[0,1], " [Count: ", df_sorted.iloc[0,2],"]")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Travel Time'] = df['End Time'] -df['Start Time']
    total_travel_time = df['Travel Time'].sum()
    print('- Total Travel Time:', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Travel Time'].mean()
    print('- Mean Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].value_counts().to_frame()
    user_count.columns = ['Count']
    user_count['Share in %'] = ((user_count['Count']/user_count['Count'].sum())*100).round(1)
    print('Count of Different User Types:')
    print(user_count,'\n')

    # Display counts of gender
    if city != 'washington':
        gender_count = df['Gender'].value_counts().to_frame()
        gender_count.columns = ['Count']
        gender_count['Share in %'] = ((gender_count['Count']/gender_count['Count'].sum())*100)
        gender_count['Share in %'] = gender_count['Share in %'].round(1)
        print('Count of Different Gender:')
        print(gender_count,'\n')

    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode())
        print('Birth Year Statistics')
        print('- Earliest Birth Year: {}\n- Most Recent Birth Year: {}\n\
        - Most Common Birth Year: {}'.format(earliest_year, most_recent_year, most_common_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    """ Displays raw data based on the chosen filters """

    print('\n Showing raw data...\n')

    answer = 'yes'
    i = 0
    j = 5
    while answer == 'yes':
        raw_data = df.iloc[i:j , : ]
        print(raw_data)
        answer = input('Enter "yes" if you want to see 5 (more) lines of raw data: ').lower()
        i += 5
        j += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        ## Statistical functions
        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        # Raw data
        show_raw_data(df)

        restart = input('\nIn case of restart please enter "yes"\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
