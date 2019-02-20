# imports
from instapy import InstaPy
from instapy.util import smart_run
from instapy import set_workspace
import schedule
import time

import random

# To use for a new account, import datetime and set start day of
# year to current day to warm up account until 500 daily followers
# -------------------------
# Used for follow calculation
# start_day_of_year = 267
# follow_multiplier = 15
# day_of_year = datetime.datetime.now().timetuple().tm_yday
# year = datetime.datetime.now().timetuple().tm_year

insta_username = 'weedlyshop'
insta_password = 'Hayastan7'

hashtag_categories = ['weed', 'reefer', 'weedporn', 'joint', 'kusharmy']

hashtags = ['stonedsociety', 'weedhead', 'kushsociety', 'kushlife', 'reefersdaily', 'marijuanamovement', 'weedlife',
           'kusharmy', 'kush', 'weedporn', 'marijuanagram', 'stonedtothebone', 'stoned', 'weedly', 'tobacco',
           'smokingweed', 'reefer', 'weed', 'marijuana', 'pipe']
targeted_hashtags = ['marijuana', 'weedporn', 'stoned', 'marijuanamovement', 'weedlife', 'kushlife', 'pipe',
                     'smokingweed', 'marijuanagram', 'tobacco', 'kusharmy', 'reefer']

peak_daily_follows = 500
peak_hourly_follows = 31

peak_daily_likes = 2000
peak_hourly_likes = 125

# if year == 2018 and (day_of_year - start_day_of_year) * follow_multiplier + peak_daily_follows <= 500:
#     peak_daily_follows += (day_of_year - start_day_of_year) * follow_multiplier
#
# peak_hourly_follows = int(peak_daily_follows / 16)
#
# peak_daily_likes = int(peak_daily_follows * 4)
# peak_hourly_likes = int(peak_daily_likes / 16)


def job():
    # get an InstaPy session!
    # set headless_browser=True to run InstaPy in the background
    set_workspace("/root/InstaPyWeedly")

    session = InstaPy(username=insta_username,
                      password=insta_password,
                      headless_browser=True,
                      multi_logs=True,
                      disable_image_load=True,
                      bypass_suspicious_attempt=True)

    with smart_run(session):
        """ Activity flow """
        print('Peak daily follows: ' + str(peak_daily_follows))
        print('Peak hourly follows: ' + str(peak_hourly_follows))
        print('Peak daily likes: ' + str(peak_daily_likes))
        print('Peak hourly likes: ' + str(peak_hourly_likes))

        # settings
        session.set_quota_supervisor(enabled=True,
                                     sleep_after=["likes", "follows", "unfollows", "server_calls_d"],
                                     sleepyhead=True,
                                     stochastic_flow=True,
                                     peak_likes=(peak_hourly_likes, None),
                                     peak_follows=(peak_hourly_follows, peak_daily_follows),
                                     peak_unfollows=(None, peak_daily_follows),
                                     peak_server_calls=(None, 4900))
        session.set_relationship_bounds(enabled=True,
                                        potency_ratio=-1.1,
                                        delimit_by_numbers=True,
                                        max_followers=5050,
                                        max_following=5555,
                                        min_followers=35,
                                        min_following=40)
        session.set_delimit_liking(enabled=True,
                                   max=250,
                                   min=1)

        # actions
        session.set_user_interact(amount=2,
                                  randomize=True,
                                  percentage=100,
                                  media=None)
        session.set_do_follow(enabled=True,
                              percentage=100,
                              times=2)
        session.set_smart_hashtags(hashtags,
                                   limit=6,
                                   sort='top',
                                   log_tags=True)
        session.like_by_tags(amount=random.randint(50, 100),
                             use_smart_hashtags=True,
                             interact=True)

        # Finally unfollow users that were followed 4 days ago
        session.unfollow_users(amount=int(peak_daily_follows),
                               InstapyFollowed=(True, "all"),
                               style="FIFO",
                               unfollow_after=3 * 24 * 60 * 60,
                               sleep_delay=600)


job()

# schedule.every().day.at('8:00').do(job)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
