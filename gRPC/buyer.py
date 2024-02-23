import grpc
import shopping_platform_pb2
import shopping_platform_pb2_grpc
import uuid
import threading
import queue
import socket
from concurrent import futures
from port import *
from test import *
class BuyerService(shopping_platform_pb2_grpc.BuyerServiceServicer):
    def NotifyBuyer(self, request, context):
        # Process the incoming notification
        # Take appropriate actions based on the notification received
        if request.status=="none":

            print("\n")
            print("="*32)
            # print()
            print("Received Notification: ")
            print(f"ID: {request.item.id}")
            print(f"Name: {request.item.name}")
            print(f"Category: {shopping_platform_pb2.Category.Name(request.item.category)}")
            print(f"Description: {request.item.description}")
            print(f"Price: {request.item.price}")
            print(f"Rating: {request.item.rating} / 5")
            print(f"Quantity: {request.item.quantity}")
            # print()
            print("="*32)
            return shopping_platform_pb2.Empty()  # Respond with an empty message
        else:
            print("\n")
            print("="*20)
            # print()
            print("Received Notification: ")
            print(request.status)
            print("="*20)
            return shopping_platform_pb2.Empty()

class BuyerClient:
    def __init__(self, address, buyer_id,ipaddr):
        self.channel = grpc.insecure_channel(address)
        self.stub = shopping_platform_pb2_grpc.BuyerServiceStub(self.channel)
        self.buyer_id = buyer_id
        self.notification_queue = queue.Queue()
        self.private_ipaddr=ipaddr
        self.server = None

    def start_server(self):
        if self.server is None:
            self.server = grpc.server(futures.ThreadPoolExecutor())
            self.buyer_service = BuyerService()
            shopping_platform_pb2_grpc.add_BuyerServiceServicer_to_server(self.buyer_service, self.server)
            self.server.add_insecure_port(self.private_ipaddr)
            self.server.start()
            self.server.wait_for_termination()

    def Register(self,register_request):
        response=self.stub.RegisterBuyer(register_request)
        return response
        
    def search_item(self, search_request):
        response = self.stub.SearchItem(search_request)
        print("Buyer prints:")
        for item in response.items:
            print("–")
            print(f"Name: {item.name}, Category: {shopping_platform_pb2.Category.Name(item.category)}")
            print(f"Description: {item.description}, Price: {item.price}, Quantity: {item.quantity}")
            print(f"Rating: {item.rating} / 5, Seller: {item.seller_address}")
            print("–")


    def buy_item(self, buy_request):
        response = self.stub.BuyItem(buy_request)
        print("Item purchased:", response.status)

    def add_to_wishlist(self, wishlist_request):
        wishlist_request.buyer_id = self.buyer_id
        response = self.stub.AddToWishlist(wishlist_request)
        print("Item added to wishlist:", response.status)

    def rate_item(self, rate_request):
        response = self.stub.RateItem(rate_request)
        print("Item rated:", response.status)
        
    def stop_server(self):
        if self.server is not None:
            self.server.stop(None)

    def __del__(self):
        self.stop_server()

if __name__ == '__main__':
    buyer_address = input("Enter Market Place address: ")
    buyer_address=buyer_address+":50001"
    buyer_id = str(uuid.uuid1())
    public_ipaddr=get_ipadrress()
    port1=get_new_port()
    public_ipaddr=public_ipaddr+":"+str(port1)
    host=socket.gethostname()
    private_ipaddr=socket.gethostbyname(host)+":"+str(port1)
    # public_ipaddr=private_ipaddr
    buyer_client = BuyerClient(buyer_address, buyer_id,private_ipaddr)
    # print(public_ipaddr)
    buyer_info=shopping_platform_pb2.RegisterBuyerRequest(uuid=buyer_id,address=public_ipaddr)
    response=buyer_client.Register(buyer_info)
    # print(response)
    if(response.status=="FAIL"):
        print("FAIL: Only one buyer allowed to register from 1 ipadress")
    else:
        server_thread = threading.Thread(target=buyer_client.start_server,daemon=True)
        server_thread.start()
        # buyer_client.start()
    # buyer_client.start_notification_processor()
        try:
            while True:
                
                print("-"*32)
                print("1. Search Item")
                print("2. Buy Item")
                print("3. Add to Wishlist")
                print("4. Rate Item")
                print("5. Exit")
                print("-"*32)

                choice = input("Enter your choice: ")

                if choice == '1':
                    item_name = input("Enter item name: ")
                    item_category = input("Enter item category (ELECTRONICS, FASHION, OTHERS): ")
                    search_request = shopping_platform_pb2.SearchItemRequest(
                        name=item_name,
                        category=shopping_platform_pb2.Category.Value(item_category)
                    )
                    buyer_client.search_item(search_request)
                elif choice == '2':
                    item_id = int(input("Enter item ID: "))
                    quantity = int(input("Enter quantity: "))
                    # buyer_address = input("Enter your address (ip:port): ")
                    buy_request = shopping_platform_pb2.BuyItemRequest(
                        item_id=item_id,
                        quantity=quantity,
                        buyer_address=public_ipaddr
                    )
                    buyer_client.buy_item(buy_request)
                elif choice == '3':
                    item_id = int(input("Enter item ID: "))
                    wishlist_request = shopping_platform_pb2.AddToWishlistRequest(
                        item_id=item_id,
                        buyer_address=buyer_address
                    )
                    buyer_client.add_to_wishlist(wishlist_request)
                elif choice == '4':
                    item_id = int(input("Enter item ID: "))
                    rating = int(input("Enter your rating (1-5): "))
                    rate_request = shopping_platform_pb2.RateItemRequest(
                        item_id=item_id,
                        buyer_address=buyer_address,
                        rating=rating
                    )
                    buyer_client.rate_item(rate_request)
                elif choice == '5':
                    break
                else:
                    print("Invalid choice")
        except KeyboardInterrupt:
            del buyer_client
