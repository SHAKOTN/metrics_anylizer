from consumer.message_validator import is_valid_consumer_message


def test_is_valid_consumer_message__valid():
    assert is_valid_consumer_message(
        {
            'metadata': '{"affectedNode":"LX0005","affectedEquipment":"RRU-B1B3-S1-2",'
                        '"affectedSite":"LX0005","alarmCategory":"UNKNOWN","alarmGroup":'
                        '"003--1143982548-SubNetwork=Zagreb,MeContext=LX0005,ManagedElement=LX0005,'
                        'Equipment=1,FieldReplaceableUnit=RRU-B1B3-S1-2-1460077","alarmCSN":"1460077",'
                        '"alarmID":"9175147","alarmMO":"SubNetwork=Zagreb,MeContext=LX0005,'
                        'ManagedElement=LX0005,Equipment=1,FieldReplaceableUnit=RRU-B1B3-S1-2",'
                        '"alarmNotificationType":"Minor","alarmLastSeqNo":"1460077",'
                        '"alarmEventTime":"2020-01-24T09:23:03+02:00","vnocAlarmID":"ERA005"}'
        }
    )

    assert is_valid_consumer_message(
        # Message without failed equipment
        {
            'metadata': '{"affectedNode":"LX00016","affectedSite":"LX00016",'
                        '"alarmCategory":"FAULT","alarmGroup":"003--936265541-SubNetwork=Osijek,MeContext=LX00016'
                        'ManagedElement=LX00016,ENodeBFunction=1,NbIotCell=sandrovac-1469856","alarmCSN":"1469856",'
                        '"alarmID":"9175114","alarmMO":"SubNetwork=Osijek,MeContext=LX00016,ManagedElement=LX00016,'
                        'ENodeBFunction=1,NbIotCell=sandrovac","alarmNotificationType":"Major",'
                        '"alarmLastSeqNo":"1469856",'
                        '"alarmEventTime":"2020-01-24T09:23:03+02:00","vnocAlarmID":"ERA015"}'}
    )
    assert is_valid_consumer_message(
        # Message without failed equipment
        {
            'metadata': '{"affectedNode":"LX00016","affectedSite":"LX00016",'
                        '"alarmCategory":"FAULT","alarmGroup":"003--936265541-SubNetwork=Osijek,MeContext=LX00016'
                        'ManagedElement=LX00016,ENodeBFunction=1,NbIotCell=sandrovac-1469856","alarmCSN":"1469856",'
                        '"alarmID":"9175114","alarmMO":"SubNetwork=Osijek,MeContext=LX00016,ManagedElement=LX00016,'
                        'ENodeBFunction=1,NbIotCell=sandrovac","alarmNotificationType":"Major",'
                        '"alarmLastSeqNo":"1469856",'
                        '"alarmEventTime":"2020-01-24T09:23:03+02:00","vnocAlarmID":"ERA015"}'}
    )


def test_is_valid_consumer_message__invalid():
    assert not is_valid_consumer_message(
        {
            'metadata': '{"affectedNode":"LX0005",'
                        '"affectedSite":"LX0005","alarmCate":"UNKNOWN","alarmGroup":'
                        '"003--1143982548-SubNetwork=Zagreb,MeContext=LX0005,ManagedElement=LX0005,'
                        'Equipment=1,FieldReplaceableUnit=RRU-B1B3-S1-2-1460077","alarmCSN":"1460077",'
                        '"alarmID":"9175147","alarmMO":"SubNetwork=Zagreb,MeContext=LX0005,'
                        'ManagedElement=LX0005,Equipment=1,FieldReplaceableUnit=RRU-B1B3-S1-2",'
                        '"alarmNotificationType":"Minor","alarmLastSeqNo":"1460077",'
                        '"alarmEventTime":"2020-01-24T09:23:03+02:00","vnocAlarmI":"ERA005"}'
        }
    )
