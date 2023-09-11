from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt
import numpy as np

from scipy import stats
import math

class DatabaseActivities:
    def __init__(self) -> None:
        pass
class StravaActivities:
    def __init__(self, client) -> None:
        self.client = client
    
    def getActivities(self, activityType="Run", afterDate=None, limit=None, beforeDate=None):
        
        activities = self.client.get_activities(before=beforeDate, after=afterDate, limit=limit)

        activityList = []
        for activity in activities:   
             activityList.append(activity)
        
        filteredList = []
        for activity in activityList:
            if( activity.type == activityType):
                filteredList.append(activity)
        return filteredList
    

class StravaStats:
    def __init__(self, activityList):
        self.runList = activityList
        self.dailyMilesList = self.getDailyMilesList(self.runList)
        self.dailyDateList = self.getDailyDateList(self.runList)
                
    def longestRunStreak(self, runActivityList):

        # runList = self.runList
        runList = runActivityList
        
        count = 1
        maxCount = 1
        longestStartDate = runList[0].start_date

        for i in range(len(runList) -1 ):
            currDate = runList[i].start_date
            currDate = currDate.date()
            prevDate = runList[i+1].start_date
            prevDate = prevDate.date()

            dayDiff = abs((currDate - prevDate).days)
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
            currDate = self.toDatetime(str(runList[i].start_date))
            prevDate = self.toDatetime(str(runList[i+1].start_date))

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

    # def toMiles(self, distance):
    #     dist = str(distance).strip(" meter")
    #     dist = float(dist) / 1609.34
    #     return dist 

    def getDailyMilesList(self, runActivityList, startDate=date.min, endDate=date.max):
        y = np.array([])
        # self.runList
        for run in runActivityList:
            if (startDate <= run.start_date.date() <= endDate):
                y = np.append(y, run.distance)
        return y

    def getDailyDateList(self, runActivityList, startDate=date.min, endDate=date.max):
        x = np.array([])
        # self.runList
        for run in runActivityList:
            if (startDate <= run.start_date.date() <= endDate):
                x = np.append(x, run.start_date)
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
        
        time = 0
        for run in runList:
            if (startDate <= run.start_date.date() <= endDate):
                time += run.moving_time
        return time

    def totalMiles(self, dailyMilesList):
        runList = dailyMilesList
        # runList = self.dailyMilesList
        
        count = 0
        for run in runList:
            count += run
        return count

    def averagePace(self, dailyMilesList, startDate, endDate):
        milesWithinRange = dailyMilesList
        try:
            pace = (self.totalElapsedTimeInSeconds(self.runList, startDate, endDate ) / 60) / self.totalMiles(milesWithinRange)
            floorPace = math.floor(pace)
            seconds = (pace - floorPace ) * 60
        except:
            return "---"

        return f'{floorPace}:{math.floor(seconds)}'

    def getStatsForRange(self, startDate, endDate):
        allStats = {}

        try:
            milesWithinRange = self.getDailyMilesList(self.runList, startDate, endDate)
            dailyDatesList = self.getDailyDateList(self.runList, startDate, endDate)

            allStats["avg_pace"] = self.averagePace(milesWithinRange, startDate, endDate)
            allStats["streak"] = self.longestRunStreak(self.runList)[0]
            allStats["shortest"] = round(self.minRun(milesWithinRange), 2)
            allStats["longest"] = round(milesWithinRange.max(),2)
            allStats["average"] = round(np.average(milesWithinRange), 2)
            allStats["median"] = round(np.median(milesWithinRange), 2)
            allStats["mode"] = self.modeRun(milesWithinRange)[0]
            allStats["modeOccurance"] = self.modeRun(milesWithinRange)[1]
            allStats["startDate"] = startDate
            allStats["endDate"] = endDate

            totaldays = (endDate - startDate).days

            totalSeconds = round(self.totalElapsedTimeInSeconds(self.runList, startDate, endDate))
            totalMinutes = round(totalSeconds / 60, 2)
            totalHours = round(totalSeconds/3600, 2)

            allStats["totalDays"] = totaldays
            allStats["totalRunningDays"] = len(dailyDatesList)
            allStats["percentDays"] = round(len(dailyDatesList)/ totaldays, 2)* 100
            allStats["totalSeconds"] = totalSeconds
            allStats["totalMinutes"] = totalMinutes
            allStats["totalHours"] = totalHours
            allStats["totalOfDaysRunning"] = round(totalHours / 24, 2)
            allStats["totalMiles"] = round(self.totalMiles(milesWithinRange), 2)
        except:
            return 0
        
        return allStats
    
    def summaryStringForRange(self, startDate, endDate):
        allstats = self.getStatsForRange(startDate, endDate)
        if (allstats == 0):
            return ["Invalid date range."]
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