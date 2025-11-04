class Configuration_Validator:
    """
    Validates weather configuration parameters
    """

    def validate_forecast_days(self, days_to_show):
        """
        Validates the parameter days_to_show to ensure it is within the minimum (1 day) and maximum (14 days) range
        Note: The WeatherAPI free account only allows up to a maximum of three forecast days to be displayed
s
        :param days_to_show: The number of forecast days to display

        :exception: An error message if the condition is not met
        """
        if not (1 <= days_to_show <= 14):
            raise Exception(f"- CAN ONLY FORECAST BETWEEN 1 AND 14 DAYS")

    def validate_time_range(self, start_time, end_time):
        """
        Validates that the start_time and end_time are within the allowed range and ensures that end_time is greater
        than start_time

        :param start_time: The beginning hour of the analysis period
        :param end_time: The ending hour of the analysis period

        :exception: An error message if the condition is not met
        """
        if not (0 <= start_time <= 23) or not (1 <= end_time <= 24):
            raise Exception("- INVALID TIME. ENTER THE HOUR IN 24-HOUR FORMAT (0-24) AS A WHOLE NUMBER")
        if end_time <= start_time:
            raise Exception(f"- END TIME MUST BE AFTER START TIME")

    def validate_timeline_fits_range(self, duration, top_timeline_count):
        """
        Ensures that the number of hours displayed in the timeline report does not exceed the total duration of the
        analysis period

        :param duration: The time difference (in hours) between the ending and starting time
        :param top_timeline_count: The number of hours to display in the timeline report

        :exception: An error message if the condition is not met
        """
        if duration < top_timeline_count:
            raise Exception(f"- TIMELINE COUNT TOO LONG (MAX {duration} HOURS)")

    def validate_rain_check_window(self, rain_check_hours_prior, start_time):
        """
        Validates that the rain check window occurs on the same day and before the analysis start time

        :param rain_check_hours_prior: The number of hours before start_time to check for rain
        :param start_time: The beginning hour of the analysis period

        :exception: An error message if the condition is not met.
        """
        if rain_check_hours_prior > start_time or start_time - rain_check_hours_prior < 0:
            raise Exception(f"- RAIN CHECK PERIOD MUST BE SAME DAY AND BEFORE START TIME")
