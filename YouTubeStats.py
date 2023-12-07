#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os
import time

import googleapiclient
import pandas as pd
from youtube_api import YoutubeDataApi
import youtube_api.parsers as P


# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    api_key = "lkalskdjlakjsldkjasldja"
    youtube = YoutubeDataApi(key=api_key)
    # channel_name = input("Please input youtube channel name")
    username = 'cobypersin'
    searches = youtube.search(q=username, max_results=1)
    youtube_api = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
    # request = yt_api.channels().list(part="snippet,contentDetails,statistics,contentOwnerDetails", forUsername=username)
    # response = request.execute()
    df = pd.DataFrame(searches)
    channel_id = df["channel_id"][0]
    # print(channel_id)
    channel_data = youtube.get_channel_metadata(channel_id=channel_id, parser=P.parse_channel_metadata, part=["id", "snippet", "contentDetails", "statistics", "topicDetails", "brandingSettings"])
    # df = pd.DataFrame(channel_data)
    # print(channel_data)
    view_count = channel_data["view_count"]
    video_count = channel_data["video_count"]
    playlist_id_uploads = channel_data["playlist_id_uploads"]
    country = channel_data["country"]
    request = youtube_api.playlistItems().list(
        part="contentDetails",
        maxResults=25,
        playlistId=playlist_id_uploads)
    response = request.execute()
    video_ids = [item["contentDetails"]["videoId"] for item in response["items"]]
    video_published_at = [item["contentDetails"]["videoPublishedAt"] for item in response["items"]]
    for video_id in video_ids:
        data_list = []
        video_comments = youtube.get_video_comments(video_id=video_id, get_replies=True, parser=P.parse_comment_metadata,  part=['snippet'])
        print(video_comments)
        # data_list.append([channel_id, view_count, video_id, video_published_at, video_comments])
        # df = pd.DataFrame.from_records([data_list])
        # data_list.clear()
        # # if file does not exist write header
        # if not os.path.isfile(username + '.csv'):
        #     df.to_csv(username + '.csv', index=None)
        # else:  # else it exists so append without writing the header
        #     df.to_csv(username + '.csv', mode='a', index=None)


if __name__ == "__main__":
    main()

