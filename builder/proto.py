import static.proto_pb2 as FLY_BOOK_PROTO

from protobuf_to_dict import protobuf_to_dict
from utils.fly_book_utils import generate_request_cid


class ProtoBuilder:
    @staticmethod
    def build_send_message_request_proto(sends_text, request_id, chatId):
        cid_1 = generate_request_cid()
        cid_2 = generate_request_cid()

        Packet = FLY_BOOK_PROTO.Packet()
        Packet.payloadType = 1
        Packet.cmd = 5
        Packet.cid = request_id

        PutMessageRequest = FLY_BOOK_PROTO.PutMessageRequest()
        PutMessageRequest.type = 4
        PutMessageRequest.chatId = chatId
        PutMessageRequest.cid = cid_1
        PutMessageRequest.isNotified = 1
        PutMessageRequest.version = 1

        PutMessageRequest.content.richText.elementIds.append(cid_2)
        PutMessageRequest.content.richText.innerText = sends_text
        PutMessageRequest.content.richText.elements.dictionary[cid_2].tag = 1

        TextProperty = FLY_BOOK_PROTO.TextProperty()
        TextProperty.content = sends_text
        PutMessageRequest.content.richText.elements.dictionary[cid_2].property = TextProperty.SerializeToString()

        Packet.payload = PutMessageRequest.SerializeToString()
        return Packet

    @staticmethod
    def build_search_request_proto(request_id, query):
        request_cid = generate_request_cid()
        Packet = FLY_BOOK_PROTO.Packet()
        Packet.payloadType = 1
        Packet.cmd = 11021
        Packet.cid = request_id

        UniversalSearchRequest = FLY_BOOK_PROTO.UniversalSearchRequest()
        UniversalSearchRequest.header.searchSession = request_cid
        UniversalSearchRequest.header.sessionSeqId = 1
        UniversalSearchRequest.header.query = query
        UniversalSearchRequest.header.searchContext.tagName = 'SMART_SEARCH'

        EntityItem_1 = FLY_BOOK_PROTO.EntityItem()
        EntityItem_1.type = 1
        # EntityItem_1.filter.userFilter.isResigned = 1
        # EntityItem_1.filter.userFilter.haveChatter = 0
        # EntityItem_1.filter.userFilter.exclude = 1

        EntityItem_2 = FLY_BOOK_PROTO.EntityItem()
        EntityItem_2.type = 2
        EntityFilter = FLY_BOOK_PROTO.EntityItem.EntityFilter()
        EntityItem_2.filter.CopyFrom(EntityFilter)

        EntityItem_3 = FLY_BOOK_PROTO.EntityItem()
        GroupChatFilter = FLY_BOOK_PROTO.GroupChatFilter()
        EntityItem_3.type = 3
        EntityItem_3.filter.groupChatFilter.CopyFrom(GroupChatFilter)

        EntityItem_4 = FLY_BOOK_PROTO.EntityItem()
        EntityItem_4.type = 10
        EntityFilter = FLY_BOOK_PROTO.EntityItem.EntityFilter()
        EntityItem_4.filter.CopyFrom(EntityFilter)

        UniversalSearchRequest.header.searchContext.entityItems.append(EntityItem_1)
        UniversalSearchRequest.header.searchContext.entityItems.append(EntityItem_2)
        UniversalSearchRequest.header.searchContext.entityItems.append(EntityItem_3)
        UniversalSearchRequest.header.searchContext.entityItems.append(EntityItem_4)
        UniversalSearchRequest.header.searchContext.commonFilter.includeOuterTenant = 1
        UniversalSearchRequest.header.searchContext.sourceKey = 'messenger'
        UniversalSearchRequest.header.locale = 'zh_CN'
        SearchExtraParam = FLY_BOOK_PROTO.SearchExtraParam()
        UniversalSearchRequest.header.extraParam.CopyFrom(SearchExtraParam)
        Packet.payload = UniversalSearchRequest.SerializeToString()
        return Packet

    @staticmethod
    def decode_search_response_proto(message):
        userAndGroupIds = []
        Packet = FLY_BOOK_PROTO.Packet()
        Packet.ParseFromString(message)
        Packet = protobuf_to_dict(Packet)
        if 'payload' in Packet:
            payload = Packet['payload']
            UniversalSearchResponse = FLY_BOOK_PROTO.UniversalSearchResponse()
            UniversalSearchResponse.ParseFromString(payload)
            UniversalSearchResponse = protobuf_to_dict(UniversalSearchResponse)
            Packet['payload'] = UniversalSearchResponse
            for result in UniversalSearchResponse['results']:
                if result['type'] == 1:
                    userAndGroupIds.append({
                        'type': 'user',
                        'id': result['id']
                    })
                elif result['type'] == 3:
                    userAndGroupIds.append({
                        'type': 'group',
                        'id': result['id']
                    })

        return Packet, userAndGroupIds


    @staticmethod
    def build_create_chat_request_proto(request_id, chatId):
        Packet = FLY_BOOK_PROTO.Packet()
        Packet.payloadType = 1
        Packet.cmd = 13
        Packet.cid = request_id

        PutChatRequest = FLY_BOOK_PROTO.PutChatRequest()
        PutChatRequest.type = 1
        PutChatRequest.chatterIds.append(chatId)
        Packet.payload = PutChatRequest.SerializeToString()
        return Packet

    @staticmethod
    def decode_create_chat_response_proto(message):
        chatId = None
        Packet = FLY_BOOK_PROTO.Packet()
        Packet.ParseFromString(message)
        Packet = protobuf_to_dict(Packet)
        if 'payload' in Packet:
            payload = Packet['payload']
            PutChatResponse = FLY_BOOK_PROTO.PutChatResponse()
            PutChatResponse.ParseFromString(payload)
            PutChatResponse = protobuf_to_dict(PutChatResponse)
            Packet['payload'] = PutChatResponse
            chatId = PutChatResponse['chat']['id']
        return Packet, chatId

    @staticmethod
    def decode_receive_msg_proto(message):
        fromId = None
        ChatId = None
        ReceiveTextContent = ''
        print(1)

        Frame = FLY_BOOK_PROTO.Frame()
        Frame.ParseFromString(message)
        Frame = protobuf_to_dict(Frame)
        print(2)
        payload = Frame['payload']
        Packet = FLY_BOOK_PROTO.Packet()
        Packet.ParseFromString(payload)
        Packet = protobuf_to_dict(Packet)
        Frame['payload'] = Packet
        Packet_sid = Packet['sid']
        print(3)
        if 'payload' in Packet:
            payload = Packet['payload']
            PushMessagesRequest = FLY_BOOK_PROTO.PushMessagesRequest()
            PushMessagesRequest.ParseFromString(payload)
            PushMessagesRequest = protobuf_to_dict(PushMessagesRequest)
            Packet['payload'] = PushMessagesRequest
            print(4)
            if 'messages' in PushMessagesRequest:
                messages = PushMessagesRequest['messages']
                for k, v in messages.items():
                    message_type = v['type']
                    fromId = v['fromId']
                    content = v['content']
                    ChatId = v['chatId']
                    if message_type == 4:
                        print(5)
                        TextContent = FLY_BOOK_PROTO.TextContent()
                        TextContent.ParseFromString(content)
                        TextContent = protobuf_to_dict(TextContent)
                        v['content'] = TextContent
                        dictionary = TextContent['richText']['elements']['dictionary']
                        for k, v in dictionary.items():
                            property = v['property']
                            TextProperty = FLY_BOOK_PROTO.TextProperty()
                            TextProperty.ParseFromString(property)
                            TextProperty = protobuf_to_dict(TextProperty)
                            v['property'] = TextProperty
                            ReceiveTextContent += TextProperty['content']
                    print(6)

        return Frame, Packet_sid, fromId, ChatId, ReceiveTextContent


