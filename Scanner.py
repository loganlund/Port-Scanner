import socket
import threading
from queue import Queue
from datetime import datetime

#pip install fpdf
from fpdf import FPDF

#this is loganspage.com '138.197.201.164'  

print_lock = threading.Lock()
q = Queue()


def getUserInput():
    #user input URL 
    host = input('Specify a URL to scan: ')
    hostIP = socket.gethostbyname(host) #get IPv4 address of host to scan
    print(hostIP) #print ip address of URL

    #user specifies port to scan
    port = int(input('Specify a port to scan: '))
    scanSinglePort(hostIP, port)


def scanSinglePort(hostIP, port):
    listOfPorts = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    print('------------------------')
    if sock.connect_ex((hostIP, port)):
        print('port ' + str(port) + ' is closed')
        listOfPorts.append('port ' + str(port) + ' is closed')
        
    else:
        print('port ' + str(port) + ' is open!!!!!!!!!!!!')
        listOfPorts.append('port ' + str(port) + ' is open!!!!!!!!!!!!')
    print('------------------------')
    return listOfPorts



def TCPscanPorts(host):   
    #define port range
    minPort = int(input('Please specify a beginning port for a range that you would like to scan: '))
    maxPort = int(input('Please specify the last port in the range that you would like to scan: '))
    
    portList = createArray(minPort, maxPort)
    responseList = []
    for port in portList:   
        response = scanSinglePort(host, port)
        responseList.append(response)
    return responseList


        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock.settimeout(5)
        # print('------------------------')
        # print('scanning port ' + str(port) + ' on host ' + host + " IP Address: " + socket.gethostbyname(host))
        # if sock.connect_ex((host, port)):
        #     print('port ' + str(port) + ' is closed')
        # else:
        #     print('port ' + str(port) + ' is open!!!!!!!!!!!!!!')
        # print('------------------------')




def createArray(minPort, maxPort):
    portList = []
    for i in range(minPort, maxPort):
        portList.append(i)
    print(portList)
    return portList


#uncomment this for threading

# def threader():
#     while True:
#         worker = q.get()
#         TCPscanPorts(worker)
#         q.task_done()
        
# for x in range(2): #change to 60 or something
#     t = threading.Thread(target=threader)
#     t.daemon = True
#     t.start()

# for worker in range(1,100):
#     q.put(worker)

# q.join()

def ScanHosts(hostList):
    resultsList = []
    for host in hostList:
        resultsList.append(host + '\n')
        hostIP = socket.gethostbyname(host)
        resultsList.append('IP Address: ' + hostIP)
        results = TCPscanPorts(hostIP)
        resultsList.append(results)
    
    #create PDF file
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 14) 

    for i in resultsList:
        pdf.cell(200,10,txt = i)
    
    pdf.output('results.pdf')

        
def getHostList():
    file1 = open("hosts.txt", "r")
    hostList = file1.readlines()
    for i in range(0, len(hostList)):
        hostList[i] = hostList[i].replace('\n', '')
    print(hostList)
    ScanHosts(hostList)


#getUserInput() #this works
getHostList()
