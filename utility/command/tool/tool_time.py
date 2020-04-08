"""
Time tool object

--

Author : DrLarck

Last update : 08/04/20 by DrLarck
"""


class ToolTime:

    @staticmethod
    async def convert_time(seconds):
        """
        Convert the passed seconds into a time string of format :

        - 00d 00h 00m 00s

        OR

        - 00h 00m 00s

        OR

        - 00m 00s

        OR

        - 00s

        :param seconds: (`int`)

        --

        :return: `str`
        """

        # Init
        # Time references (in seconds)
        ref_day = 86400
        ref_hour = 3600
        ref_minute = 60
        ref_second = 1
        time_string = ""

        # Calculate the day
        day = int(seconds / ref_day)
        seconds -= ref_day * day

        # Calculate the hour
        hour = int(seconds / ref_hour)
        seconds -= ref_hour * hour

        # Calculate the minute
        minute = int(seconds / ref_minute)
        seconds -= ref_minute * minute

        # Calculate the second
        second = int(seconds / ref_second)
        seconds -= ref_second * second

        # Setup the string
        if day > 0:
            time_string += f"{day:,}d "

        if hour > 0:
            time_string += f"{hour:,}h "

        if minute > 0:
            time_string += f"{minute:,}m "

        if second > 0:
            time_string += f"{second:,}s"

        return time_string
