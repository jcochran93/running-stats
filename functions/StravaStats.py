from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy import stats
import math

class StravaStats:
    
    activityList = []
    runList = []

    def __init__(self, client, numberOfActivities):
        self.client = client
        self.numberOfActivities = numberOfActivities
        self.activityList = self.getActivities()
        self.runList = self.getRunList()

    def getActivities(self):
        activities = self.client.get_activities(limit=self.numberOfActivities)

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
                    longestStartDate = currDate.date()
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


    # x = np.array([])
    # y = np.array([])

    def toMiles(self, distance):
        dist = str(distance).strip(" meter")
        dist = float(dist) / 1609
        return dist 


    # # for run in activityList:
    # #     y = np.append(y, toMiles(run.distance))
    # #     x = np.append(x, toDatetime(run.start_date_local))


    def minRun(self):
    
        runList = self.runList
        
        minRun = 1000000
        for run in runList:
            if(run < minRun and run > 0):
                minRun = run
        return minRun

    def modeRun(self):
        runList = self.runList
        
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
        runList = self.runList
        
        count = 0
        for run in runList:
            count += self.toMiles(run.distance)
        return count

    def averagePace(self):
        runList = self.runList
        
        pace = (self.totalElapsedTimeInSeconds() / 60) / self.totalMiles()
        floorPace = math.floor(pace)
        seconds = (pace - floorPace ) * 60

        return f'{floorPace}:{math.floor(seconds)}'



    # totaldays = (x.max()-x.min()).days

    # totalSeconds = round(totalElapsedTimeInSeconds(activityList))
    # totalMinutes = round(totalSeconds / 60, 2)
    # totalHours = round(totalSeconds/3600, 2)

    # print(f'The shortest run: {round(minRun(y), 2)}')
    # print(f'The longest run: {round(y.max(),2)}')
    # print(f'Average run: {round(np.average(y), 2)}')
    # print(f'Median run: {round(np.median(y), 2)}')
    # print(f'Most common distance (rounded to a mile): {modeRun(y)[0]} with {modeRun(y)[1]} runs')
    # print("")
    # print(f'From {x.min().strftime("%d, %b %Y")} to {x.max().strftime("%d, %b %Y")} ({totaldays} days)')
    # print(f'You ran {len(x)} days or {round(len(x)/ totaldays, 2)* 100}% of the time.')
    # print(f'For a total of {totalSeconds} seconds, or {totalMinutes} minutes, or {totalHours} hours, or {round(totalHours / 24, 2)} days')
    # print("")
    # print(f'During that time you ran a total of {round(totalMiles(activityList), 2)} miles')
    # print("")
    # print(f'Average pace: {averagePace(activityList)} min/mile')

    # runStreak()





    # # # %%
    # # plt.figure(figsize=(50,8))
    # # plt.scatter(x,y)
    # # plt.show()

    # # # %%



