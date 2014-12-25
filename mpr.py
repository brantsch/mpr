#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import requests
import os

HOST = ""

def rate(newrating):
    """ Rate the currently playing song. """
    request = requests.get('http://' + HOST + "/addNewRating", params={'rating' : newrating})
    print("made request with rating " + str(newrating))

def show():
    """ Show the rating for the currently playing song. """
    request = requests.get('http://' + HOST + "/getCurrent")
    json = request.json()
    for key,value in json.items():
        print("{}: {}".format(key,value))

def show_list(count):
    """ Show a list of <count> best ratings. """
    request = requests.get("http://" + HOST + "/getRatinglist",params={"maxResults" : count})
    json = request.json()
    strings = ["\n".join(["{}: {}".format(key,repr(value)) for key, value in obj.items()]) for obj in json]
    print(("-"*20).join(strings))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="operation") # subcommand name will be stored in the "operation" attribute of the namespace returned by parse_args
    subparsers.required = True # subcommand _must_ be given

    get_subp = subparsers.add_parser('get',help="Get ratings for songs.")
    get_subp.add_argument("--best-n","-b",type=int,required=False,help="Show the n best rated songs from the database.")

    rate_subp = subparsers.add_parser('rate',help="Rate songs.")
    rate_subp.add_argument('rating', type=int, help="The rating to submit.")

    parser.add_argument('--host', type=str, action="store", default="localhost:5000", help='The host of the mpr service. Format: "host:port" ')
    args = parser.parse_args()

    HOST = args.host

    if args.operation == "rate":
        rate(args.rating)
    elif args.operation == "get":
        if args.best_n:
            show_list(args.best_n)
        else:
            show()
