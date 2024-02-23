Shopping Platform Client

This Python code is a client application for interacting with a shopping platform using gRPC. The client allows buyers to register, search for items, buy items, add items to their wishlist, and rate items.

Dependencies:
- grpc
- shopping_platform_pb2
- shopping_platform_pb2_grpc
- uuid
- threading
- queue
- socket
- concurrent.futures
- port (port.py)
- test (test.py)

Usage:
1. Ensure that the necessary dependencies are installed.
2. Run the client script.
3. Enter the marketplace address when prompted.
4. Follow the menu to perform various actions:
   - Search for items
   - Buy items
   - Add items to wishlist
   - Rate items
   - Exit

Note:
- The client utilizes gRPC to communicate with the server.
- Buyer ID is generated automatically using UUID.
- The client runs a server thread to handle incoming notifications.
- Only one buyer is allowed to register from one IP address.
- The client handles user input using a menu system.
- The client supports graceful shutdown using KeyboardInterrupt.

Shopping Platform Server

This Python code serves as a gRPC-based server for a shopping platform. It supports both buyer and seller functionalities, including registration, login, item listing, item search, item updates, item deletion, wishlisting, item rating, and item purchase.

Dependencies:
- grpc
- concurrent.futures
- shopping_platform_pb2
- shopping_platform_pb2_grpc
- socket
- test (test.py)

Usage:
1. Ensure that the necessary dependencies are installed.
2. Run the server script.
3. The server listens on port 50001 by default.
4. Sellers and buyers can connect to the server using gRPC client applications.

Key Features:
- Supports registration and login for sellers and buyers.
- Sellers can list items for sale, update item details, and delete items.
- Buyers can search for items, add items to their wishlist, rate items, and purchase items.
- Notifications are sent to buyers and sellers for relevant events such as item updates and purchases.

Seller Client

This Python code is a client application for sellers to interact with a shopping platform server using gRPC. Sellers can register, login, list items for sale, update item details, delete items, and display their listed items.

Dependencies:
- grpc
- shopping_platform_pb2
- shopping_platform_pb2_grpc
- uuid
- socket
- concurrent.futures
- threading
- port (port.py)
- test (test.py)

Usage:
1. Ensure that the necessary dependencies are installed.
2. Run the client script.
3. Enter the marketplace address when prompted.
4. Choose either to register as a new seller or login if already registered.
5. Perform various actions:
   - Sell Item: List a new item for sale.
   - Update Item: Modify the price or quantity of an existing item.
   - Delete Item: Remove an item from the seller's list.
   - Display Items: View all items listed for sale.
   - Exit

Note:
- Each seller is required to register with a unique UUID.
- Only one seller is allowed to register from one IP address.
- Sellers must provide their UUID during login.
- Item listings are associated with the seller's UUID for identification.
- Sellers can perform various actions on their listed items.
- The client supports graceful shutdown using KeyboardInterrupt.



