#!/usr/local/bin/python

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from hbase import Hbase
from hbase.ttypes import *

transport = TSocket.TSocket('master', 9090)
transport = TTransport.TBufferedTransport(transport)

protocol = TBinaryProtocol.TBinaryProtocol(transport)

client = Hbase.Client(protocol)

transport.open()

#--------------------

tableName = 'new_music_table'

scan = TScan()
id = client.scannerOpenWithScan(tableName, scan, None)
result = client.scannerGetList(id, 10)

for r in result:
	print 'the row is: ', r.row

	for k, v in r.columns.items():
		print '\t'.join([k, v.value])



