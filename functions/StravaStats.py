from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy import stats
import math

class StravaStats:
    
    activityList = []
    runList = []

    dailyMilesList = np.array([])
    dailyDateList = np.array([])

    allStats = {}

    def __init__(self, client, numberOfActivities):
        self.client = client
        self.numberOfActivities = numberOfActivities
        self.activityList = self.getActivities()
        self.runList = self.getRunList()
        self.dailyMilesList = self.getDailyMilesList()
        self.dailyDateList = self.getDailyDateList()
        self.allStats = self.getAllStats()

    def getActivities(self):
        if (self.numberOfActivities != 0):
            activities = self.client.get_activities(limit=self.numberOfActivities)
        else:
            activities = self.client.get_activities()

        activityList = []
        for activity in activities:   
             activityList.append(activity)
        
        return activityList
    
    def getRunList(self):
        activities = self.activityList

        runList = []
        for activity in activities:
            if( activity.type == "Run"):
                runList.append(activity)
        return runList
                
    def longestRunStreak(self):

        runList = self.runList
        
        count = 1
        maxCount = 1
        longestStartDate = runList[0].start_date_local

        for i in range(len(runList) -1 ):
            currDate = runList[i].start_date_local
            currDate = currDate.date()
            prevDate = runList[i+1].start_date_local
            prevDate = prevDate.date()

            dayDiff = (currDate - prevDate).days
            if(dayDiff == 0):
                continue
            elif(dayDiff == 1):
                count +=1
            elif(dayDiff > 1):
                if count > maxCount:
                    maxCount = count
                    longestStartDate = currDate
                count = 1
            
        # TODO: Test if this works for continuous streak
        maxCount = max(count, maxCount)

        return maxCount, longestStartDate

    def currentRunStreak(self):

        runList = self.runList
        
        count = 1
        for i in range(len(runList) -1 ):
            currDate = self.toDatetime(str(runList[i].start_date_local))
            prevDate = self.toDatetime(str(runList[i+1].start_date_local))

            dayDiff = (currDate - prevDate).days
            if(dayDiff == 0):
                continue
            if(dayDiff == 1):
                count +=1
                # print(currDate)
            else:
                    longestStartDate = currDate.date()
                    break
        return count, longestStartDate

    def toMiles(self, distance):
        dist = str(distance).strip(" meter")
        dist = float(dist) / 1609
        return dist 

    def getDailyMilesList(self):
        y = np.array([])
        for run in self.runList:
            y = np.append(y, self.toMiles(run.distance))
        return y

    def getDailyDateList(self):
        x = np.array([])
        for run in self.runList:
            x = np.append(x, run.start_date_local)
        return x

    def minRun(self):
    
        runList = self.dailyMilesList
        
        minRun = 1000000
        for run in runList:
            if(run < minRun and run > 0):
                minRun = run
        return minRun

    def modeRun(self):
        runList = self.dailyMilesList
        
        runs = np.array([])
        for run in runList:
            runs = np.append(runs, round(run))
        return stats.mode(runs)

    def totalElapsedTimeInSeconds(self):
        runList = self.runList
        
        time = 0
        for run in runList:
            time += run.elapsed_time.total_seconds()
        return time

    def totalMiles(self):
        runList = self.dailyMilesList
        
        count = 0
        for run in runList:
            count += run
        return count

    def averagePace(self):
        runList = self.dailyMilesList
        
        pace = (self.totalElapsedTimeInSeconds() / 60) / self.totalMiles()
        floorPace = math.floor(pace)
        seconds = (pace - floorPace ) * 60

        return f'{floorPace}:{math.floor(seconds)}'

    def getAllStats(self):
        allStats = {}
        allStats["avg_pace"] = self.averagePace()
        allStats["streak"] = self.longestRunStreak()[0]
        allStats["shortest"] = round(self.minRun(), 2)
        allStats["longest"] = round(self.dailyMilesList.max(),2)
        allStats["average"] = round(np.average(self.dailyMilesList), 2)
        allStats["median"] = round(np.median(self.dailyMilesList), 2)
        allStats["mode"] = self.modeRun()[0]
        allStats["modeOccurance"] = self.modeRun()[1]
        allStats["startDate"] = self.dailyDateList.min().strftime("%d, %b %Y")
        allStats["endDate"] = self.dailyDateList.max().strftime("%d, %b %Y")

        totaldays = (self.dailyDateList.max()-self.dailyDateList.min()).days

        totalSeconds = round(self.totalElapsedTimeInSeconds())
        totalMinutes = round(totalSeconds / 60, 2)
        totalHours = round(totalSeconds/3600, 2)

        allStats["totalDays"] = totaldays
        allStats["totalRunningDays"] = len(self.dailyDateList)
        allStats["percentDays"] = round(len(self.dailyDateList)/ totaldays, 2)* 100
        allStats["totalSeconds"] = totalSeconds
        allStats["totalMinutes"] = totalMinutes
        allStats["totalHours"] = totalHours
        allStats["totalOfDaysRunning"] = round(totalHours / 24, 2)
        allStats["totalMiles"] = round(self.totalMiles(), 2)

        return allStats
                                       
        
                                           
                                           # # # %%
    # # plt.figure(figsize=(50,8))
    # # plt.scatter(x,y)
    # # plt.show()

    # # # %%



