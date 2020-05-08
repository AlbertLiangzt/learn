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

#-----------------------------------

base_info_contents = ColumnDescriptor(name='meta_data', maxVersions=1)
other_info_contents = ColumnDescriptor(name='flags', maxVersions=1)

client.createTable('new_music_table', [base_info_contents, other_info_contents])

print client.getTableNames()

