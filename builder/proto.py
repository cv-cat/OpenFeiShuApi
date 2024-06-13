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
    def decode_receive_msg_proto(message):
        fromId = None
        ChatId = None
        ReceiveTextContent = ''

        Frame = FLY_BOOK_PROTO.Frame()
        Frame.ParseFromString(message)
        Frame = protobuf_to_dict(Frame)

        payload = Frame['payload']
        Packet = FLY_BOOK_PROTO.Packet()
        Packet.ParseFromString(payload)
        Packet = protobuf_to_dict(Packet)
        Frame['payload'] = Packet
        Packet_sid = Packet['sid']
        if 'payload' in Packet:
            payload = Packet['payload']
            PushMessagesRequest = FLY_BOOK_PROTO.PushMessagesRequest()
            PushMessagesRequest.ParseFromString(payload)
            PushMessagesRequest = protobuf_to_dict(PushMessagesRequest)
            Packet['payload'] = PushMessagesRequest
            if 'messages' in PushMessagesRequest:
                messages = PushMessagesRequest['messages']
                for k, v in messages.items():
                    fromId = v['fromId']
                    content = v['content']
                    ChatId = v['chatId']
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

        return Frame, Packet_sid, fromId, ChatId, ReceiveTextContent



