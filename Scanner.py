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
    scanSingleTCPPort(hostIP, port)


def scanSingleTCPPort(hostIP, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    print('------------------------')
    if sock.connect_ex((hostIP, port)):
        print('TCP port ' + str(port) + ' is closed')
        return('TCP port ' + str(port) + ' is closed')
        
    else:
        print('TCP port ' + str(port) + ' is open!!!!!!!!!!!!')
        return('TCP port ' + str(port) + ' is open!!!!!!!!!!!!')
    print('------------------------')
    
def scanSingleUDPPort(hostIP, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    print('------------------------')
    if sock.connect_ex((hostIP, port)):
        print('UDP port ' + str(port) + ' is closed')
        return('UDP port ' + str(port) + ' is closed')
        
    else:
        print('port ' + str(port) + ' is open!!!!!!!!!!!!')
        return('port ' + str(port) + ' is open!!!!!!!!!!!!')
    print('------------------------')
    



def TCPscanPorts(host):   
    #define port range
    minPort = int(input('Please specify a beginning port for a range that you would like to scan on ' + host + ': '))
    maxPort = int(input('Please specify the last port in the range that you would like to scan on ' + host + ': '))
    
    portList = createArray(minPort, maxPort)
    responseList = []
    for port in portList:   
        response = scanSingleTCPPort(host, port)
        responseList.append(response)
    return responseList


def UDPScanPorts(host):
    minPort = int(input('Please specify a beginning port for a range that you would like to scan on ' + host + ': '))
    maxPort = int(input('Please specify the last port in the range that you would like to scan on ' + host + ': '))
    
    portList = createArray(minPort, maxPort)
    responseList = []
    for port in portList:   
        response = scanSingleUDPPort(host, port)
        responseList.append(response)
    return responseList

def createArray(minPort, maxPort):
    portList = []
    for i in range(minPort, (maxPort+1)):
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
        hostIP = socket.gethostbyname(host) #Comment this line out if hosts.txt contains IP Addresses instead of domain names, and pass host to TCPScanPorts instead of hostIP
        resultsList.append('IP Address: ' + hostIP)
        resultsList.append('\n')
        results = TCPscanPorts(hostIP) #pass in host instead if you want to use IP Addresses instead of hostnames
        results2 = UDPScanPorts(hostIP)
        for i in results:
            resultsList.append(i)
        for i in results2:
            resultsList.append(i)
    print (resultsList)
    #create PDF file
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 14) 
    for i in range(0, len(resultsList)):
        pdf.cell(200,10,txt = str(resultsList[i]), ln=i, align = "C")
    print(pdf.output)
    pdf.output("results.pdf")

        
def getHostList():
    file1 = open("hosts.txt", "r")
    hostList = file1.readlines()
    for i in range(0, len(hostList)):
        hostList[i] = hostList[i].replace('\n', '')
    print(hostList)
    ScanHosts(hostList)


#getUserInput() #this works
getHostList()
