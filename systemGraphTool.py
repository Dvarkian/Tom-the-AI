# systemGraphTool.py
# A utility to facilitate graphing of ststems statistics, in a way smimlar to task manager on windows.
# Programmed by Murray Jones (murray.jones12@bigpond.com).
# Completed 17/06/2021

from ioUtils import * # Some of my handy input / ooutput utilityes

# Import required modules. Incur will install the module if it is not present.
sg = incur("PySimpleGUI") # Handles GUI component of graph.
psutil = incur("psutil")


def remap(value, leftMin, leftMax, rightMin, rightMax): # Same as thee map() function on Arduino, translates a value from a rande to a given range.
    
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    
    valueScaled = float(value - leftMin) / float(leftSpan) # Convert the left range into a 0-1 range (float)

    return rightMin + (valueScaled * rightSpan) # Convert the 0-1 range into a value in the right range.


# Define global placeholders.
lastValue = {} # Last values for each line on graph
iteration = 0 # Current program iteration.
prev_x = {} # last x-value for each line on graph 
prev_y = {} # last y-value for each line on graph 


def graphData(name, graph, value, graphSamples, stepSize=3, graphMax=100, lineColor="light blue", lineWidth=1, output=None):
    # Converts data into the contents of a PySimpleGUI Graph element
    
    global lastValue
    global iteration
    global prev_x, prev_y

    value = max(0, value) # Prevent any negative values.
    value = min(graphMax, value) # Prevent values exceeding the max. height of the graph.

    if name not in lastValue: # Set up entries for series being graphed.
        lastValue[name] = 0
        prev_x[name] = 0
        prev_y[name] = 0

    new_x, new_y = iteration, value # Assign x and y values.

    if output != None: # Print the data to a given printable PySimpleGUI element.
        output.update(str(value)[:5].strip(".") + "%")

    if name == list(lastValue.keys())[0]: # If we are graphing the first of all the series that we need to graph ...
        if iteration >= graphSamples: # Check if graph is full of data
            try:
                graph.move(-stepSize, 0) # Shift grapph over if full of data
            except:
                pass

    if iteration >= graphSamples: # Check if graph is full of data
        prev_x[name] = prev_x[name] - stepSize # Match old-x value with the shift over we have just applied.
        
    graph.draw_line((prev_x[name], prev_y[name]), (new_x, new_y), color=lineColor, width=lineWidth) # Draw the line on the PySimpleGUI Graph element.

    prev_x[name], prev_y[name] = new_x, new_y # Store new values for use in next iteration.

    if name == list(lastValue.keys())[0]: # If we are graphing the first of all the series that we need to graph ...
        iteration += stepSize if iteration < graphSamples else 0 # Increnent the iteration counter if graph is not full of data.
    
    lastValue[name] = value # Store prevous input for use next iteration.


# Define var's to hold disk read / write statistics.
disk_io = psutil.disk_io_counters()

largestRead = 0
largestWrite = 0

totalRead = disk_io.read_bytes
totalWrite = disk_io.write_bytes

# Define var's to hold network upload / download statistics.
net_io = psutil.net_io_counters()

largestSent = 0
largestRecieved = 0

totalSent = net_io.bytes_sent
totalRecieved = net_io.bytes_recv


def sysGraph(window, graph, samples, CPU="max", RAM=False, Disk=False, Net=False): # Main function to retrieve data and assemble graph.
    global largestRead, largestWrite, totalRead, totalWrite, iteration
    global largestSent, largestRecieved, totalSent, totalRecieved

    if iteration == 0: # Erase graph oon firt iteration, removes olld data if graph settings have just been changed
        graph.erase()
        

    if CPU.lower() == "max":
        # Display CPU frequency, as a percentage of maximum frequency.
        
        cpufreq = psutil.cpu_freq()
        cpuFreqPercent = remap(cpufreq.current, cpufreq.min, cpufreq.max, 0, 100)
        graphData("cpuFreq", graph, cpuFreqPercent, samples, lineColor="orange")


    if CPU == "max" or CPU == "normal" or CPU == "cores":
        # Display usage of each logical core.

        cpuColors = ["orchid1", "orchid2", "orchid3", "orchid4"]
        
        for cpu, percentage in enumerate(psutil.cpu_percent(percpu=True)): # Iterate through logical cores.
            graphData("CPU" + str(cpu), graph, percentage, samples, lineColor=cpuColors[int(cpu)])


    if CPU == "max" or CPU == "normal" or CPU == "min":
        # Display overall average of CPU usage.

        graphData("cpuTotal", graph, psutil.cpu_percent(), samples, lineColor="orchid")
        

    if RAM: # Display RAN and SWAP usage. 

        svmem = psutil.virtual_memory()
        graphData("RAM", graph, svmem.percent, samples, lineColor="orchid")

        swap = psutil.swap_memory()
        graphData("swap", graph, swap.percent, samples, lineColor="purple")
        

    if Disk: # Display disk input / output staistics.

        disk_io = psutil.disk_io_counters()

        nowRead = disk_io.read_bytes
        read = (nowRead - totalRead)
        totalRead = nowRead
        
        write = disk_io.write_bytes

        nowWrite = disk_io.write_bytes
        write = (nowWrite - totalWrite)
        totalWrite = nowWrite

        if largestRead == 0 and read == 0:
            readPercentage = 0
        else:
            largestRead = max(largestRead, read)
            readPercentage = remap(read, 0, largestRead, 0, 100)

        graphData("read", graph, readPercentage, samples, lineColor="firebrick1")

        if largestWrite == 0 and write == 0:
            writePercentage = 0
        else:
            largestWrite = max(largestWrite, write)
            writePercentage = remap(write, 0, largestWrite, 0, 100)

        graphData("write", graph, writePercentage, samples, lineColor="firebrick4")


    if Net: # Display network upload and download stats.

        net_io = psutil.net_io_counters()

        nowSent = net_io.bytes_sent
        sent = (nowSent - totalSent)
        totalSent = nowSent
        
        nowRecieved = net_io.bytes_recv
        recieved = nowRecieved - totalRecieved
        totalRecieved = nowRecieved
        
        if largestSent == 0 and sent == 0:
            sentPercentage = 0
        else:
            largestSent = max(largestSent, sent)
            sentPercentage = remap(sent, 0, largestSent, 0, 100)

        graphData("sent", graph, sentPercentage, samples, lineColor="light blue")


        if largestRecieved == 0 and recieved == 0:
            recvPercentage = 0
        else:
            largestRecieved = max(largestRecieved, recieved)
            recvPercentage = remap(recieved, 0, largestRecieved, 0, 100)

        graphData("recieved", graph, recvPercentage, samples, lineColor="blue")

    window.refresh() # Send new data to thhe application window.
