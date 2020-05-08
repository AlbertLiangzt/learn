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

#------------------
tableName = 'new_music_table'
rowKey = '1001'

mutations = [Mutation(column = 'meta_data:name', value = 'lvdeshui'), \
		Mutation(column = 'meta_data:tag', value = 'comedy'), \
		Mutation(column = 'flags:is_valid', value = 'TRUE')]

client.mutateRow(tableName, rowKey, mutations, None)

