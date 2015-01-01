
import os
import time
import random
import itertools

def Main():
    total_distance = 0				# variable to store total distance of a complete route 
    nOfCity = 10				# variable to represent the number of cities
    route = [0] * (nOfCity+1)		        # 1-dimensional array to store a complete route 
    distances = [None] * nOfCity		# 2-dimensional array of adjacency matrix to store all the distances
	
    fin = open( os.path.dirname(os.path.abspath(__file__)) + "/10Cities.txt", "r")	        # data file open
    fout = open( os.path.dirname(os.path.abspath(__file__)) +"/result2.txt","w")		# result file open

    str_buffer = fin.readline()                                                 # File I/O
    str_buffer = str_buffer.split(' ')                                          # split string 
    
    for  i in range( nOfCity):		                                        # constructing adjacency matrix to represent distances between cities
        distances[i] = [None] * nOfCity                                         ######### do not modify this file I/O
        for j in range( nOfCity):                                               ######### do not modify this file I/O
            distances[i][j] = int(str_buffer[i*10+j])	                        # copying distances from data file to matix		
    fin.close()                                                                 ######### do not modify this file I/O


    total_distance = getInitialRoute(nOfCity,distances,route)	                # setting up the initial route (fixed) 
    print("Initial route: ",route)
    print("Total_distance of initial route", total_distance) 
    total_distance = SAHillClimbing(nOfCity,distances,route,total_distance)       # solving the problem by hill climbing 
	
    fout.write(str(total_distance))                                             # writing the total_distance found on file "result.txt"
    for i in range( nOfCity):                                                   # writing the route found on file "result.txt"
        #print(route[i])
        fout.write(str(route[i])+"\n")



    print ("total_distance = ", total_distance)
                                    # printing the total_distance found on the monitor

	
def SAHillClimbing(nOfCity,distances,route,total_distance):

    route_buffer =[0]*10
    t= time.time()
    print("hill climbing started")
    while(1):
       
        print(str(total_distance))

        route_it = itertools.combinations(route[1:10],2)
        route_combinations = []

        for i in route_it:
            route_combinations.append(i)




        cities_to_swap = (1,1)
        best_total_distance = total_distance #trouble was brought by best_total_distance
        for k in route_combinations:
            route_copy = route[:]
            x1 = route_copy.index(k[0])
            x2 = route_copy.index(k[1])

            holder = route_copy[x1]
            route_copy[x1] = route_copy[x2]
            route_copy[x2] = holder

            new_total_distance = 0
            for i in range (0, 10):
                new_total_distance += distances[route_copy[i]][route_copy[i+1]]


            if(new_total_distance<best_total_distance):
                best_total_distance = new_total_distance
                cities_to_swap = k


        if(best_total_distance<total_distance):
            x1 = route.index(cities_to_swap[0])
            x2 = route.index(cities_to_swap[1])

            holder = route[x1]
            route[x1] = route[x2]
            route[x2] = holder
            total_distance = best_total_distance

        else:
            break




        ######################################
        ##                                  ##
        ##      FILL IN THE CODE HERE       ##
        ##   (SA hill climbing algorithm)   ##
        ##                                  ##
        ######################################
     
    print("hill climbing finished")
    print("Execution time: ", str(time.time() - t)) # print the execution time 
    print("Route: ", route)                         # print the route
    print("Total distance: ",str(total_distance))   # print the total distance
    
    return total_distance                           # return the total_distance found

    
def getInitialRoute(nOfCity, distances, route):
    isVisit = [0]* nOfCity                          # list to check if salesman visited city i 
    start = 0                                       # city 0 is fixed as the start city and the ending city 
    isVisit[start] = 1                              # isVisit[i] == 1 means that salesman visited the city i before
    total_distance = 0                              # sum of the distances in the route


    count = 1
    while(count < 10):
        j = random.randint(1,9)
        if(isVisit[j] ==0):                         # generate random route 
            route[count] = j                        
            isVisit[j] =1
            count = count +1

    for i in range (0, 10):
        total_distance += distances[route[i]][route[i+1]]                   # compute the final distance of the completed route  
    return total_distance                                                   # return the final distance
	
	
Main()
