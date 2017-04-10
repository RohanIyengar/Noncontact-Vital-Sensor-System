import csv, numpy
# data0 = time (s), data1 = I channel x (DB), data2 = I channel y (deg), data3 = Q channel x (DB), data4 = I channel y (deg)
data0 = numpy.linspace(0.0, 10.0, num=21)
data1 = numpy.linspace(-48.0, -49.5, num=21)
data2 = numpy.linspace(-15.0, -20.0, num=21)
data3 = numpy.linspace(-45.0, -47.5, num=21)
data4 = numpy.linspace(15.0, 20.0, num=21)
data = zip(data0,data1,data2)
#q_data = zip(data0,data3,data4)
header = [("Label", "", ""),("Time(s)", "CH2", "CH3")]
out1 = csv.writer(open("sample_data.csv","wb"), delimiter=',',quoting=csv.QUOTE_ALL)
#i_data = [data[i] for i in [0,1,2]];
#print i_data
out1.writerows(header)
out1.writerows(data)
#out2 = csv.writer(open("q_channel.csv","wb"), delimiter=',',quoting=csv.QUOTE_ALL)
#q_data = [data[i] for i in [0,3,4]]
#print q_data
#out2.writerows(header)
#out2.writerows(q_data)