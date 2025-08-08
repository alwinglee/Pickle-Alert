from configuration_validator import Configuration_Validator
class Configuration:
    """
    Stores weather configuration parameters and passes them to the Configuration_Validator class for validation
    """
    def __init__(self, START_TIME, END_TIME, TOP_TIMELINE_COUNT, RAIN_CHECK_HOURS_PRIOR, DAYS_TO_SHOW):
        self.START_TIME=START_TIME
        self.END_TIME=END_TIME
        self.TOP_TIMELINE_COUNT=TOP_TIMELINE_COUNT
        self.RAIN_CHECK_HOURS_PRIOR=RAIN_CHECK_HOURS_PRIOR
        self.DAYS_TO_SHOW=DAYS_TO_SHOW
        self.duration = self.END_TIME - self.START_TIME
        self.activateValidation()
    def activateValidation(self):
        """
        Executes all configuration validations functions

        :exception: An error message will be displayed when validation conditions are not met
        """
        Configuration_Validator.validate_forecast_days(self.DAYS_TO_SHOW)
        Configuration_Validator.validate_time_range(self.START_TIME,self.END_TIME)
        Configuration_Validator.validate_timeline_fits_range(self.duration,self.TOP_TIMELINE_COUNT)
        Configuration_Validator.validate_rain_check_window(self.RAIN_CHECK_HOURS_PRIOR,self.START_TIME)