from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy import stats



def getActivities(client):
    activities = client.get_activities(limit=100)

    activityList = []
    for activity in activities:
        if( activity.type == "Run"):
            activityList.append(activity)

    return activityList
            
def toDatetime(stravaDate):
    date = str(stravaDate)
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])

    return datetime(year, month, day)

def longestRunStreak(runList):
    count = 1
    maxCount = 1
    for i in range(len(runList) -1 ):
        currDate = toDatetime(str(runList[i].start_date_local))
        prevDate = toDatetime(str(runList[i+1].start_date_local))

        dayDiff = (currDate - prevDate).days
        if(dayDiff == 0):
            continue
        if(dayDiff == 1):
            count +=1
            # print(currDate)
        else:
            if count > maxCount:
                maxCount = count
                longestStartDate = currDate.date()
            count = 1
    
    result = f"Longest Run streak: {maxCount} days"
    result += f'{longestStartDate} - {longestStartDate+ timedelta(days=maxCount-1)}'
    return result

def currentRunStreak(runList):
    count = 1
    for i in range(len(runList) -1 ):
        currDate = toDatetime(str(runList[i].start_date_local))
        prevDate = toDatetime(str(runList[i+1].start_date_local))

        dayDiff = (currDate - prevDate).days
        if(dayDiff == 0):
            continue
        if(dayDiff == 1):
            count +=1
            # print(currDate)
        else:
                longestStartDate = currDate.date()
                print(f"Current Run streak: {count} days")
                print(f'{longestStartDate} - {longestStartDate+ timedelta(days=count-1)}')
                break

def runStreak(activityList):
    currentRunStreak(activityList)
    longestRunStreak(activityList)


# %%

x = np.array([])
y = np.array([])

def toMiles(distance):
    dist = str(distance).strip(" meter")
    dist = float(dist) / 1609
    return dist 


# for run in activityList:
#     y = np.append(y, toMiles(run.distance))
#     x = np.append(x, toDatetime(run.start_date_local))


# def minRun(runList):
#     minRun = 1000000
#     for run in runList:
#         if(run < minRun and run > 0):
#             minRun = run
#     return minRun

# def modeRun(runList):
#     runs = np.array([])
#     for run in runList:
#         runs = np.append(runs, round(run))
#     return stats.mode(runs)

# def totalElapsedTimeInSeconds(runList):
#     time = 0
#     for run in runList:
#         time += run.elapsed_time.total_seconds()
#     return time

# def totalMiles(runList):
#     count = 0
#     for run in runList:
#         count += toMiles(run.distance)
#     return count

# def averagePace(runList):
#     pace = (totalElapsedTimeInSeconds(runList) / 60) / totalMiles(runList)
#     floorPace = math.floor(pace)
#     seconds = (pace - floorPace ) * 60

#     return f'{floorPace}:{math.floor(seconds)}'



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





# # %%
# plt.figure(figsize=(50,8))
# plt.scatter(x,y)
# plt.show()

# # %%



