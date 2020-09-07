"""Config parser

--

@author DrLarck

@update 07/09/20 by DrLarck"""

import asyncio
import json


class ConfigParser:

    @staticmethod
    async def get_config_for(key):
        """Get the config value for the passed key

        @param str key

        --

        @return value from the config.json file or None if not found"""

        value = None

        # Open the configuration file
        configuration = open("config.json", 'r')

        # Get the json file data
        data = json.load(configuration)

        # Split the key
        key = key.split()
        
        # Get the value
        for i in range(len(key)):
            await asyncio.sleep(0)

            # Save the previous key
            # iterate until we find the information
            data  = data[key[i]] 
        
        # Fetch the last value found
        value = data

        # Close the configuration file
        configuration.close()

        return value
