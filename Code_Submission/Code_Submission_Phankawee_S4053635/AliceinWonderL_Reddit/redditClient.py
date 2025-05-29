#
# COSC2671 Social Media and Network Analytics
# @author Jeffrey Chan, RMIT University, 2023
#

import sys
import praw


def redditClient():
    """
        Setup Reedit API authentication.
        Replace username, secrets and passwords with your own.

        @returns: praw Reedit object
    """

    try:
        #
        # TODO: you specify with your details
        #
        clientId = "clentId"
        clientSecret = "clientSecret"
        password = "password"
        userName = "userName"
        userAgents = 'script:get_potential_subreddit:v1.0 (by /u/userName)'

        redditClient = praw.Reddit(client_id = clientId,
                                   client_secret = clientSecret,
                                   password = password,
                                   username = userName,
                                   user_agent = userAgents)
        redditClient.read_only = True
    except KeyError:
        sys.stderr.write("Key or secret token are invalid.\n")
        sys.exit(1)


    return redditClient

if __name__ == "__main__":
    client = redditClient()
    try:
        # This should print your Reddit username if authentication is successful
        print("Authenticated as:", client.user.me())
    except Exception as e:
        print("Error during authentication:", e)