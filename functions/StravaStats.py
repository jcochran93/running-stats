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
        self.runActivityList = activityList
        self.dailyMilesList = self.getDailyMilesList(self.runActivityList)
        self.dailyDateList = self.getDailyDateList(self.runActivityList)
                
    def longestRunStreak(self, runActivityList):

        # runList = self.runActivityList
        runList = runActivityList
        
        count = 1
        maxCount = 1
        longestStartDate = runList[0].start_date_local

        for i in range(len(runList) -1 ):
            currDate = runList[i].start_date_local
            currDate = currDate.date()
            prevDate = runList[i+1].start_date_local
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

        # runList = self.runActivityList
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

    def getDailyMilesList(self, runActivityList, startDate=date.min, endDate=date.max):
        y = np.array([])
        # self.runActivityList
        for run in runActivityList:
            if (startDate <= run.start_date_local.date() <= endDate):
                y = np.append(y, run.distance)
        return y

    def getDailyDateList(self, runActivityList, startDate=date.min, endDate=date.max):
        x = np.array([])
        # self.runActivityList
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
        
        time = 0
        for run in runList:
            if (startDate <= run.start_date_local.date() <= endDate):
                try:
                    time += run.moving_time
                except:
                    time += run.moving_time.total_seconds()
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
            pace = (self.totalElapsedTimeInSeconds(self.runActivityList, startDate, endDate ) / 60) / self.totalMiles(milesWithinRange)
            floorPace = math.floor(pace)
            seconds = (pace - floorPace ) * 60
        except:
            return "---"

        return f'{floorPace}:{math.floor(seconds)}'

    def getStatsForRange(self, startDate, endDate):
        allStats = {}

        try:
            milesWithinRange = self.getDailyMilesList(self.runActivityList, startDate, endDate)
            dailyDatesList = self.getDailyDateList(self.runActivityList, startDate, endDate)

            allStats["avg_pace"] = self.averagePace(milesWithinRange, startDate, endDate)
            allStats["streak"] = self.longestRunStreak(self.runActivityList)[0]
            allStats["shortest"] = round(self.minRun(milesWithinRange), 2)
            allStats["longest"] = round(milesWithinRange.max(),2)
            allStats["average"] = round(np.average(milesWithinRange), 2)
            allStats["median"] = round(np.median(milesWithinRange), 2)
            allStats["mode"] = self.modeRun(milesWithinRange)[0]
            allStats["modeOccurance"] = self.modeRun(milesWithinRange)[1]
            allStats["startDate"] = startDate
            allStats["endDate"] = endDate

            totaldays = (endDate - startDate).days

            totalSeconds = round(self.totalElapsedTimeInSeconds(self.runActivityList, startDate, endDate))
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
            return {"Error":"Invalid date range."}
        summary = {}

        summary["Longest Run Streak"] = f'{allstats["streak"]} days'

        summary["Shortest Run"] = f'{allstats["shortest"]} miles'
        summary["Longest Run"] = f'{allstats["longest"]} miles'
        summary["Total Miles"] = f'{allstats["totalMiles"]} miles'
        
        summary['Average Run'] = f'{allstats["average"]} miles'
        summary['Median Run'] = f'{allstats["median"]} miles'
        summary['Most common distance (rounded to a mile)']= f'{allstats["mode"]} miles {allstats["modeOccurance"]} times'

        summary['Days Ran'] = f'{allstats["totalRunningDays"]} days or {allstats["percentDays"]}% of all days'
        
        summary['Time Spent Running'] =  (f'For a total of {allstats["totalMinutes"]} minutes, or {allstats["totalHours"]} hours, or {allstats["totalOfDaysRunning"]} days')
        
        summary['Average Pace'] = (f'{allstats["avg_pace"]} min/mile')
        return summary