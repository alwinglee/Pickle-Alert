from configuration_validator import Configuration_Validator


class Configuration:
    """
    Stores weather configuration parameters and passes them to the Configuration_Validator class for validation
    """
    def __init__(self, start_time, end_time, top_timeline_count, rain_check_hours_prior, days_to_show):
        self.start_time = start_time
        self.end_time = end_time
        self.top_timeline_count = top_timeline_count
        self.rain_check_hours_prior = rain_check_hours_prior
        self.days_to_show = days_to_show
        self.duration = self.end_time - self.start_time
        self.activate_validation()

    def activate_validation(self):
        """
        Executes all configuration validations functions

        :exception: An Exception will be displayed when validation conditions are not met
        """
        validator = Configuration_Validator()
        validator.validate_forecast_days(self.days_to_show)
        validator.validate_time_range(self.start_time, self.end_time)
        validator.validate_timeline_fits_range(self.duration, self.top_timeline_count)
        validator.validate_rain_check_window(self.rain_check_hours_prior, self.start_time)
