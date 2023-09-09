from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt
import numpy as np

from scipy import stats
import math

class StravaStats:
    def __init__(self, client, afterDate):
        self.client = client
        # self.numberOfActivities = numberOfActivities
        self.afterDate = afterDate
        self.activityList = self.getActivities()
        self.runList = self.getRunActivityList(self.activityList)
        self.dailyMilesList = self.getDailyMilesList(self.runList)
        self.dailyDateList = self.getDailyDateList(self.runList)
        # self.allStats = self.getAllStats()

    def getActivities(self):
        # if (self.numberOfActivities != 0):
        #     activities = self.client.get_activities(limit=self.numberOfActivities)
        # else:
        #     activities = self.client.get_activities()

        activities = self.client.get_activities(after=self.afterDate)

        activityList = []
        for activity in activities:   
             activityList.append(activity)
        
        return activityList
    
    def getRunActivityList(self, activityList):
        activities = activityList

        runList = []
        for activity in activities:
            if( activity.type == "Run"):
                runList.append(activity)
        return runList
                
    def longestRunStreak(self, runActivityList):

        # runList = self.runList
        runList = runActivityList
        
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

    def currentRunStreak(self, runActivityList):

        # runList = self.runList
        runList = runActivityList
        
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
        dist = float(dist) / 1609.34
        return dist 

    def getDailyMilesList(self, runActivityList, startDate=date.min, endDate=date.max):
        y = np.array([])
        # self.runList
        for run in runActivityList:
            if (startDate <= run.start_date_local.date() <= endDate):
                y = np.append(y, self.toMiles(run.distance))
        return y

    def getDailyDateList(self, runActivityList, startDate=date.min, endDate=date.max):
        x = np.array([])
        # self.runList
        for run in runActivityList:
            if (startDate <= run.start_date_local.date() <= endDate):
                x = np.append(x, run.start_date_local)
        return x

    def minRun(self, runList):
    
        runList = runList
        
        minRun = 1000000
        for run in runList:
            if(run < minRun and run > 0):
                minRun = run
        return minRun

    def modeRun(self, runList):
        runList = runList
        
        runs = np.array([])
        for run in runList:
            runs = np.append(runs, round(run))
        return stats.mode(runs)

    def totalElapsedTimeInSeconds(self, runActivityList, startDate, endDate):
        runList = runActivityList
        # runList = self.runList
        
        time = 0
        for run in runList:
            if (startDate <= run.start_date_local.date() <= endDate):
                time += run.elapsed_time.total_seconds()
        return time

    def totalMiles(self, dailyMilesList):
        runList = dailyMilesList
        # runList = self.dailyMilesList
        
        count = 0
        for run in runList:
            count += run
        return count

    def averagePace(self, dailyMilesList, startDate, endDate):
        runList = dailyMilesList
        
        pace = (self.totalElapsedTimeInSeconds(self.runList, startDate, endDate ) / 60) / self.totalMiles(self.dailyMilesList)
        floorPace = math.floor(pace)
        seconds = (pace - floorPace ) * 60

        return f'{floorPace}:{math.floor(seconds)}'

    # def getAllStats(self):
        allStats = {}
        allStats["avg_pace"] = self.averagePace(self.dailyMilesList)
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
    def getStatsForRange(self, startDate, endDate):
        allStats = {}

        milesWithinRange = self.getDailyMilesList(self.runList, startDate, endDate)

        allStats["avg_pace"] = self.averagePace(milesWithinRange, startDate, endDate)
        allStats["streak"] = self.longestRunStreak(self.runList)[0]
        allStats["shortest"] = round(self.minRun(milesWithinRange), 2)
        allStats["longest"] = round(self.dailyMilesList.max(),2)
        allStats["average"] = round(np.average(milesWithinRange), 2)
        allStats["median"] = round(np.median(milesWithinRange), 2)
        allStats["mode"] = self.modeRun(milesWithinRange)[0]
        allStats["modeOccurance"] = self.modeRun(milesWithinRange)[1]
        allStats["startDate"] = startDate
        allStats["endDate"] = endDate

        # allStats["startDate"] = self.dailyDateList.min().strftime("%d, %b %Y")
        # allStats["endDate"] = self.dailyDateList.max().strftime("%d, %b %Y")


        totaldays = (self.dailyDateList.max()-self.dailyDateList.min()).days
        totaldays = (endDate - startDate).days

        totalSeconds = round(self.totalElapsedTimeInSeconds(self.runList, startDate, endDate))
        totalMinutes = round(totalSeconds / 60, 2)
        totalHours = round(totalSeconds/3600, 2)

        allStats["totalDays"] = totaldays
        allStats["totalRunningDays"] = len(self.dailyDateList)
        allStats["percentDays"] = round(len(self.dailyDateList)/ totaldays, 2)* 100
        allStats["totalSeconds"] = totalSeconds
        allStats["totalMinutes"] = totalMinutes
        allStats["totalHours"] = totalHours
        allStats["totalOfDaysRunning"] = round(totalHours / 24, 2)
        allStats["totalMiles"] = round(self.totalMiles(milesWithinRange), 2)

        return allStats
    
    def summaryStringForRange(self, startDate, endDate):
        allstats = self.getStatsForRange(startDate, endDate)

        summary = []

        summary.append( (f'The longest run streak is {allstats["streak"]}.'))
        summary.append( (f'The shortest run: {allstats["shortest"]}'))
        summary.append( (f'The longest run: {allstats["longest"]}'))
        summary.append( (f'Average run: {allstats["average"]}'))
        summary.append( (f'Median run: {allstats["median"]}'))
        summary.append( (f'Most common distance (rounded to a mile): {allstats["mode"]} with {allstats["modeOccurance"]} runs'))
        summary.append( (f'From {allstats["startDate"]} to {allstats["endDate"]} ({allstats["totalDays"]} total days)'))
        summary.append( (f'You ran {allstats["totalRunningDays"]} days or {allstats["percentDays"]}% of the time.'))
        summary.append( (f'For a total of {allstats["totalMinutes"]} minutes, or {allstats["totalHours"]} hours, or {allstats["totalOfDaysRunning"]} days'))
        summary.append( (f'During that time you ran a total of {allstats["totalMiles"]} miles'))
        summary.append( (f'Average pace: {allstats["avg_pace"]} min/mile'))
        # summary += "<br>"
        return summary