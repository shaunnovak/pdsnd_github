# MODULE INFO
""" Udacity nd104 Project 2: Explore US Bikeshare Data

Uses Python to understand U.S. bikeshare data. Calculate statistics and
builds an interactive environment where a user chooses the data and filter
for a dataset to analyze.
"""

__version__ = '1.0'
__author__ = 'Shaun Novak'

# LIBRARIES
import time
import numpy as np
import pandas as pd
import os


# Plain text to filenames for city data sets
cities_data = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

# months_list tuple to turn num into a name
months_list = ('january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december')


# MODULE FUNCTIONS

def clear_screen():
    """ Clears terminal based on OS. Fails quitely if other OS. """
    try:
         # Windows
        os.system('cls')

        # Linux / OSX
        os.system('clear')
    except:
        pass

def load_data(city, month, day):
    """Loads data based on user-set filters for city, month, and day.

    Key function that builds the dataframe used by time_stats, station_stats,
    trip_stats, and user_stats. Filters are manually selected by user via
    user_interface.

    Args:
        city (str): name of city to analyze
        month (str): name of month to filter by, or 'all' (default) for 
            no filter.
        day (str): name of day of week to filter by, or 'all' (default) 
            for no filter.

    Returns:
        df - Pandas DataFrame for city, filtered by month and day.
    """
    
    # Loads CSV matching user city name in cities_data
    df = pd.read_csv(cities_data[city])

    # Converts the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extracts month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month

    # Extract day from the Start Time column to create a day column
    df['day'] = df['Start Time'].dt.weekday_name

    # Filters month by index int if user entered specific month
    if month != 'all':
        month = months_list.index(month) + 1

        # Filters by month in place
        df = df[df['month'] == month]

    # Filters day of week by name if user entered specific day
    if day != 'all':
        # Filters by day, in place
        df = df[df['day'] == day.title()]

    # Filtered Panda DataFrame returned with formatted time, and month,
    # day, hour columns added
    return df

def section_header(section):
    """Formats section headers
    
    Creates ascii box around full upper-case section name, with a leading
    and trailing newline. 

    Args: 
        section(str) - text to put inside ascii box

    Returns:
        None
    """
    
    # Creates '=" bars above and below based on length of section
    print('\n' + ('-'*60) + '\n')
    print(" " + ("=" * (len(section) + 4)))
    print(" | {} |".format(section).upper())
    print(" " + ("=" * (len(section) + 4) + "\n"))

def time_stats(df):
    """ Prints the "Most Common" month, day, and hour of travel for selected
    city.

    Args:
        df (dataframe) - city-specific, filter-adjusted, dataframe from
        load_data().

    Returns:
        None
    """
    
    section_header('time stats')
    
    # Finds the most common month by int in the returned dataframe, then 
    # matches to it's readable name
    common_month = months_list[(df['month'].mode()[0] - 1)]
    print(" Most Common Month:  {}".format(common_month).title())

    # Finds most common weekday name in the returned dataframe
    common_day = df['Start Time'].dt.weekday_name.mode()[0]
    print(" Most Common Day: {}".format(common_day).title())
    
    # Finds most common start hour of trips, formated through time lib
    common_hour = df['Start Time'].mode().dt.hour[0]
    
    # Formats hour to 12 hour output, adds AM / PM
    if common_hour < 12:
        converted_hour = "{}am".format(common_hour)
    else:
        converted_hour = "{}pm".format(common_hour - 12)

    print(" Most Common Starting Hour:  {}".format(converted_hour))

def station_stats(df):
    """ Print "most common" starting station, end station, and station pairs
    
    Args:
        df (dataframe) - city-specific, filter-adjusted, dataframe from
        load_data().
    
    Returns:
        None
    """

    section_header('station and route stats')

    # Most common starting point
    print(" Most Common Starting Station:  [{}]".format(df['Start Station'].mode()[0]))

    # Most common end point
    print(" Most Common End Station: [{}]".format(df['End Station'].mode()[0]))
        
    # Groups all start / end combos by descending order and assigns variables
    # for formatting from the first row of cells. 
    route_combos = df.groupby(
        ['Start Station', 'End Station']).size().sort_values(ascending=False)
    start_route = route_combos.index[0][0]
    end_route = route_combos.index[0][1]
    route_count = route_combos[0]
    print(" Most Common Route:")
    print("    [{}] ==> [{}], ({} Trips).".format(start_route, end_route, route_count))

def trip_stats(df):
    """ Print average and total trip durations for given filters
    
    Args:
        df (dataframe) - city-specific, filter-adjusted, dataframe from
        load_data().
    
    Returns:
        None
    """

    section_header('trip stats')

    # Converts average of all trop duration to minues (from seconds)
    avg_trip = df['Trip Duration'].mean() / 60
    print(" Average Trip Duration:  {:,.2f} minutes.".format(avg_trip))
    
    # Converts sum of all trop duration to minutes (from seconds)
    total_trip = df['Trip Duration'].sum() / 60
    print(" Total of all trips:  {:,.2f} minutes.".format(total_trip))

def user_stats(df, city):
    """ Prints user stats such as count, gender, and age info.
    
    Args:
        df (dataframe) - city-specific, filter-adjusted, dataframe from
        load_data().
        city (str) - check for city input in case user asks for missing data.
    
    Returns:
        None
    """

    section_header('user stats')

    # User counts with .to_string to remove dtype return
    print(" User Types:")
    print(df['User Type'].value_counts().to_string())

    # Excluse gender and birth-year stats from Washington output
    if city.lower() != 'washington':
        # Gender counts with .to_string to remove dtype return
        print("\n Gender Counts:")
        print(df['Gender'].value_counts().to_string())

        # Age and birth year of oldest customer, using current year to math age
        print("\n Oldest Customer Born: {:.0f}, Age: {:.0f}".format(df['Birth Year'].min(),
            time.gmtime()[0] - df['Birth Year'].min()))

        # Age and birth year of youngest customer, using current year to math age
        print(" Youngest Customer Born: {:.0f}, Age: {:.0f}".format(df['Birth Year'].max(),
            time.gmtime()[0] - df['Birth Year'].max()))

        # Most common birth year and age of customers, based on current year
        print(" Most Common Birth Year: {:.0f}, Age: {:.0f}".format(df['Birth Year'].mode()[0],
            time.gmtime()[0] - df['Birth Year'].mode()[0]))

def user_filters():
    """ Asks for user input and gets month and hour filters for specific
    city data.

    Can select single day, single month, or "all" for either. 
    Args:
        None

    Returns:
        city (str): simple city name to load data via cities_data dict
        month (str): plain english month
        day (str): plain english day
    """
    # Sets default args for filters
    city = 'NONE!'
    month = 'all'
    day = 'all'
    
    # Sets error to empty so it prints as just a new line at first
    menu_input_error = ''

    def print_filters():
        """Terminal header listing current filters."""
        
        print('\n' + '-'*60)
        print(" FILTERS = City: {} | Month: {} | Day: {}".format(
            city.title(), month.title(), day.title()))
        print('-'*60)

    def city_filter():
        """Handles display and input of city data filters
        
        Args:
            None

        Returns:
            user_city_filter (str): user-entered city name that matches a city
                name from cities_data index
        """

        # Sets error to empty so it prints as just a new line at first
        city_input_error = ''

        while True:
            clear_screen()
            print_filters()
            print(city_input_error + '\n')

            # Populates list of selectable cities from cities_data index
            print(" CITIES - Data is available for these places: ")
            for city_index in cities_data.keys():
                print("    - {}".format(city_index).title())
            
            user_city_filter = input("\n Enter city to analyze: ")

            # Checks user input against cities list
            if user_city_filter.lower() in cities_data.keys():
                return user_city_filter.lower()
            else:
                city_input_error = ("\n *** UNRECOGNIZED CITY, PLEASE TRY "
                    "AGAIN ***") 
    
    def month_filter():
        """Handles input of month filter from user.

        Special note, data missing for Jul-Dec, default to "all" if any of
        those months are selected. 

        Args:
            None

        Returns:
            user_month_filter (str): user-entered month name that matches a 
            month name from months tuple.
        """

        month_input_error = ''

        while True:
            clear_screen()
            print_filters()
            print(month_input_error + '\n')
            
            user_month_filter = input(" MONTH - Please enter name of month to"
            " filter by: ")
            
            # Returns users-entered month name, if matches months tuple
            if user_month_filter.lower() in months_list:
                # Sets filter to 'all' if user selects missing Jul - Dec range
                if user_month_filter in months_list[6:]:
                    print("\n ***July through December data missing, "
                        "defaulting to 'All'.***")
                    input("Press ENTER to continue")
                    return 'all'
                else:
                    return user_month_filter.lower()
            elif user_month_filter.lower() == 'all':
                return 'all'
            else:
                month_input_error = ("\n *** UNRECOGNIZED MONTH PLEASE TRY "
                    "AGAIN ***")

    def day_filter():
        """Handles input for day-of-the-week filter from user.

        Args:
            None

        Returns:
            user_day_filter (str): user-entered day name that matches
            a day list tuple
        """
        days_of_week = ('monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday')

        day_input_error = ''

        while True:
            clear_screen()
            print_filters()
            print(day_input_error)
            
            user_day_filter = input("\n DAY OF THE WEEK - Please enter name of the Day to filter by: ")
            
            # Returns users-entered month name, if matches months tuple
            if user_day_filter.lower() in days_of_week:
                return user_day_filter.lower()
            elif user_day_filter.lower() == 'all':
                return 'all'
            else:
                day_input_error = ("\n *** UNRECOGNIZED DAY PLEASE TRY AGAIN ***")

    # Main menu for filter inputs that only breaks loop if successful "Analyze" or quits
    while True:
        clear_screen()
        print_filters()
        print(menu_input_error + '\n')
        
        print(" Welcome to the Bikeshare data analysis.\n\n"
            " NOTE: City data MUST be set to analyze.\n"
            "      Month and Day default to 'all' if not set.\n")
        print(
            "   1.  [C]ity\n"
            "   2.  [M]onth\n"
            "   3.  [D]ay of the week\n"
            "   4.  [A]nalyze\n"
            "   5.  [E]xit / [Q]uit \n")  

        user_input = input("Input selection as Word, # or [L]etter: ")

        # Checks input against a list of acceptable inputs for each option
        if user_input.lower() in ["1", "c", "city", "cities"]:
            city = city_filter()

        # Month
        elif user_input.lower() in ["2", "m", "month"]:
            month = month_filter()

        # Day
        elif user_input.lower() in ["3", "d", "day"]:
            day = day_filter()

        # Analyze
        elif user_input.lower() in ["4", "a", "analyze"]:
            # Don't progress if no city data set
            if city == 'NONE!':
                print("\n *** NO CITY DATA SELECTED! SELECT CITY BEFORE ANALYZING! ***")
            else:
                # Exit while statement and return city, month, and day args
                break

        # Exit program
        elif user_input.lower() in ["5", "e", "x", "q", "exit", "quit"]:
            print(" Exiting...")
            exit()

        # catch-all for unrecognized input
        else:
            menu_input_error = ("\n *** UNRECOGNIZED INPUT! PLEASE TRY AGAIN! ***")

    return city, month, day

def main():
    while True:
        clear_screen()
        city, month, day = user_filters()
        df = load_data(city, month, day)
        
        clear_screen()

        print("\n *** Showing results for: \n    {}, {}, {}".format(
            city, month, day).title())
        
        time_stats(df)
        input("\n \n Press ENTER to continue...")
        
        station_stats(df)
        input("\n \n Press ENTER to continue...")

        trip_stats(df)
        input("\n \n Press ENTER to continue...")

        user_stats(df, city)

        # Exits 
        restart = input('\n \n DONE! Shall we go again? [Y]es/[N]o: ')
        if restart.lower() in ["y", "yes", "sure", "why not", "ya", "restart"]:
            continue
        elif restart.lower() in ["no", "n", "stop", "quit", "exit"]:
            print ("\n See ya!")
            break
        else:
            print("\n Not sure what you meant by '{}'... Assuming you wanted"
                " to quit!".format(restart))
            break

if __name__ == '__main__':
    main()