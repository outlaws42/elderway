#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import sys, os
#import pickle
import configparser
from flask_login import current_user, login_required
from app import db
from app.models import User, Teams

class ScheduleGen(object):
    def __init__(self):

        self.open_file()
        self.settings()
        self.team_info()
        self.quiz_list()

    def open_file(self):
        """
            read python dict back from the file. If it doesn't exist then it creates it.
        """
        teams_db = Teams.query.filter(Teams.user_id == current_user.id)
        self.teams_present = {}
        for team in teams_db:
            self.teams_present[team.team] = team.abbr

    def team_info(self):
        self.teams = [x for x in self.teams_present.values()]
        self.rooms = int(len(self.teams) / 3)
        self.teams_capacity = self.rooms * 3

    def group_list_items(self, list_, positions,start=0):
        """
            takes a list and groups them into sub list in the amount of positions
        """
        while start <= len(list_) - positions:
            yield list_[start:start + positions]
            start += positions

    def random_list(self, list_):
        """
            Randomizes a list
        """
        self.list_ = list_
        for iten in range(1):
            rand = random.sample(self.list_, len(self.list_))
        return rand

    def reverse_sublist(self,list_):
        for i in range(0,len(list_),2):
            list_[i][:] = list_[i][::-1]
        return list_

    # Create lists  for teams
    def quiz_list(self):
        self.quiz = []
        self.quiz_random = []
        for count in range(self.quiz_day + 5):
            temp_list = self.teams[:]
            empty_sublist = []
            self.quiz.append(temp_list)
            self.quiz_random.append(empty_sublist)

        if len(self.teams) > self.teams_capacity:
            # create a long list to create the break list from
            breakr = [items for sublist in self.quiz for items in sublist]
            #print(breakr)
            # condition to see if we have 1 or 2 break teams
            if len(self.teams) - self.teams_capacity > 1:
                # Create the break list, with 2 quiz break teams in their sub list
                self.break_ = list(self.group_list_items(breakr, 2))
                # Reverse every other sublist
                self.quiz = self.reverse_sublist(self.quiz)
            else:
                # Create the break list, with 1 quiz break team in its sub list
                self.break_ = list(self.group_list_items(breakr, 1))
                # Reverse every other sublist
                self.quiz = self.reverse_sublist(self.quiz)
            for item in range(self.quiz_day + 5):
                # Remove break teams from the quiz
                no_break = [x for x in self.quiz[item] if x not in self.break_[item]]

                #random_first_pass = self.random_list(no_break)
                #self.quiz_random[item] = self.random_list(random_first_pass)


                self.quiz_random[item] = self.random_list(no_break)
        else:
            # Reverse every other sublist
            self.quiz = self.reverse_sublist(self.quiz)
            print('self.quiz  ' + str(self.quiz))
            for item in range(self.quiz_day + 5):
                # randomize list if there  are no break teams
                self.quiz_random[item] = self.random_list(self.quiz[item])

    def get_resource_path(self,rel_path):
        dir_of_py_file = os.path.dirname(sys.argv[0])
        rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
        abs_path_to_resource = os.path.abspath(rel_path_to_resource)
        return abs_path_to_resource

    def settings(self):
        self.header_title = 'Welcome to the Columbia City quiz meet'
        self.header_on = 'no'
        self.quiz_morn = 6
        self.quiz_after = 6
        self.quiz_start_time = '09:30'
        self.quiz_lunch_length = 40
        self.date_update = '08/10/2016'
        self.quiz_day = self.quiz_morn + self.quiz_after


if __name__=='__main__':
    app = ScheduleGen()
