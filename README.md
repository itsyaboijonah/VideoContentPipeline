# Content Pipeline POC
Automated Video Generation project POC

This project implements an automatic content creation pipeline for social media posts in the style of text-to-speech narrated videos, as commonly seen on TikTok.

It is currently configured for scraping, parsing, and generating videos from posts on the popular professional networking app Blind.
Alternate scrapers/parsers will be configured for other sites, such as Reddit or Facebook, to enhance the variety of content sources that can be used for video generation.

Additionally, users can provide custom background animations and accompanying music for the videos.
The TTS voices for narrating the posts are generated using AWS Polly, and videos are created using MoviePy.

The end goal of this project is to automate the creation and distribution of TikTok videos targeted at users of specific internet communities. The automatic nature of this video generation makes it scalable to many such communities.
