# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nlp.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tnlp.proto\"+\n\x14MatchScenarioRequest\x12\x13\n\x0buser_prompt\x18\x01 \x01(\t\"?\n\x15MatchScenarioResponse\x12\x15\n\rscenario_name\x18\x01 \x01(\t\x12\x0f\n\x07root_id\x18\x02 \x01(\t\".\n\x17\x45xtractArgumentsRequest\x12\x13\n\x0buser_prompt\x18\x01 \x01(\t\"\'\n\x08\x41rgument\x12\r\n\x05value\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\"\x89\x01\n\x18\x45xtractArgumentsResponse\x12;\n\targuments\x18\x01 \x03(\x0b\x32(.ExtractArgumentsResponse.ArgumentsEntry\x1a\x30\n\x0e\x41rgumentsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x32\x95\x01\n\nNLPService\x12>\n\rMatchScenario\x12\x15.MatchScenarioRequest\x1a\x16.MatchScenarioResponse\x12G\n\x10\x45xtractArguments\x12\x18.ExtractArgumentsRequest\x1a\x19.ExtractArgumentsResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nlp_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_EXTRACTARGUMENTSRESPONSE_ARGUMENTSENTRY']._loaded_options = None
  _globals['_EXTRACTARGUMENTSRESPONSE_ARGUMENTSENTRY']._serialized_options = b'8\001'
  _globals['_MATCHSCENARIOREQUEST']._serialized_start=13
  _globals['_MATCHSCENARIOREQUEST']._serialized_end=56
  _globals['_MATCHSCENARIORESPONSE']._serialized_start=58
  _globals['_MATCHSCENARIORESPONSE']._serialized_end=121
  _globals['_EXTRACTARGUMENTSREQUEST']._serialized_start=123
  _globals['_EXTRACTARGUMENTSREQUEST']._serialized_end=169
  _globals['_ARGUMENT']._serialized_start=171
  _globals['_ARGUMENT']._serialized_end=210
  _globals['_EXTRACTARGUMENTSRESPONSE']._serialized_start=213
  _globals['_EXTRACTARGUMENTSRESPONSE']._serialized_end=350
  _globals['_EXTRACTARGUMENTSRESPONSE_ARGUMENTSENTRY']._serialized_start=302
  _globals['_EXTRACTARGUMENTSRESPONSE_ARGUMENTSENTRY']._serialized_end=350
  _globals['_NLPSERVICE']._serialized_start=353
  _globals['_NLPSERVICE']._serialized_end=502
# @@protoc_insertion_point(module_scope)
