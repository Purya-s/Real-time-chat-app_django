import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timesince import timesince
from .templatetags.chatextras import initials
from .models import Message, Room
from account.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room__name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room__name}'
        self.user = self.scope['user']

        #join room group
        await self.get_room()
        await self.channel_layer.group_add(
            self.room_group_name ,
            self.channel_name
        )
        await self.accept()

        #Inform user
        if self.user.is_staff:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'users_update',
                }
            )


    async def disconnect(self , close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        if not self.user.is_staff:
            await self.set_room_closed()

    
    async def receive(self, text_data):
        # recieve message from websocket (in front end)
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        message = text_data_json["message"]
        name = text_data_json["name"]
        agent = text_data_json.get("agent", '')

        if type == 'message':

            new_message = await self.create_message(name, message, agent)

            await self.channel_layer.group_send(
            self.room_group_name,{
                "type" : "chat_message" ,
                "message" : message , 
                "name" : name ,
                'agent': agent,
                'initials': initials(name),
                'created_at': timesince(new_message.created_at),
            })
        elif type == 'update':
            print('is update')
            #send update to the room 
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'writing_active',
                    "message" : message , 
                    "name" : name ,
                    'agent': agent,
                    'initials': initials(name),
                }
            )

        
    async def chat_message(self, event):
        #send message to websocket (front end)
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'name': event['name'],
            'agent': event['agent'],
            'initials': event['initials'],
            'created_at': event['created_at'],
        }))


    async def writing_active(self, event):
        #send writing is active to room 
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'name': event['name'],
            'agent': event['agent'],
            'initials': event['initials'],
        }))


    async def users_update(self, event):
        #send information to the websocket (front end)
        await self.send(text_data=json.dumps({
            'type': 'users_update',
        }))
        #now this will be sent to front end telling the user that other user has joined (handeled in onChatMessage)


    @sync_to_async
    def get_room(self):
        self.room = Room.objects.get(uuid=self.room__name)


    @sync_to_async
    def set_room_closed(self):
        self.room = Room.objects.get(uuid=self.room_name)
        self.room.status = Room.CLOSED
        self.room.save()


    @sync_to_async
    def create_message(self, sent_by, message, agent):
        message = Message.objects.create(body=message, sent_by=sent_by)

        if agent:
            message.created_by = User.objects.get(pk=agent)
            message.save()

        self.room.messages.add(message)

        return message                                       

        

    # async def sendMessage(self , event) : 
    #     message = event["message"]
    #     username = event["username"]
    #     await self.send(text_data = json.dumps({"message":message ,"username":username}))